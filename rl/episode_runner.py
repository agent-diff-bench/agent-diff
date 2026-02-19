"""Episode runner for RL-style training loops on Agent-Diff.

This module intentionally keeps the core episode flow explicit so it's easy to
learn and modify:

1. init_env(testId=...)
2. start_run(envId=..., testId=...)
3. policy(prompt, context)
4. evaluate_run(runId=...)
5. get_results_for_run(runId=...)
6. delete_env(envId=...)
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional, cast

from agent_diff import AgentDiff, TestSuiteDetail
from rl.rewards import RewardFn, default_reward_fn
from rl.types import EpisodeContext, EpisodeResult, PolicyFn

class EpisodeRunner:
    """Runs single or multiple training episodes against Agent-Diff."""

    def __init__(
        self,
        client: AgentDiff,
        *,
        policy: Optional[PolicyFn] = None,
        reward_fn: RewardFn = default_reward_fn,
        keep_env_on_error: bool = False,
    ):
        self.client = client
        self.policy = policy
        self.reward_fn = reward_fn
        self.keep_env_on_error = keep_env_on_error

    def _resolve_policy(self, policy: Optional[PolicyFn]) -> PolicyFn:
        active_policy = policy or self.policy
        if active_policy is None:
            raise ValueError(
                "No policy configured. Pass `policy=` to EpisodeRunner(...) or run_episode(...)."
            )
        return active_policy

    @staticmethod
    def _populate_policy_metadata(result: EpisodeResult) -> None:
        if result.policy_output is None:
            return
        trace = result.policy_output.trace
        if not isinstance(trace, dict):
            return

        iterations = trace.get("iterations")
        if isinstance(iterations, int):
            result.policy_iterations = iterations
        else:
            steps = trace.get("steps")
            if isinstance(steps, list):
                result.policy_iterations = len(steps)

        completed = trace.get("completed")
        if isinstance(completed, bool):
            result.policy_completed = completed

        usage = trace.get("usage")
        if isinstance(usage, dict):
            result.policy_usage = usage

    def list_tests(self, *, suite_name: Optional[str] = None, suite_id: Optional[str] = None):
        """Convenience helper to fetch tests from a suite."""
        suites = self.client.list_test_suites(name=suite_name, suiteId=suite_id)
        if not suites.testSuites:
            raise ValueError("No test suites matched the provided filters")

        chosen_suite_id = str(suites.testSuites[0].id)
        detail = cast(
            TestSuiteDetail,
            self.client.get_test_suite(chosen_suite_id, expand=True),
        )
        return detail.tests

    def run_episode(self, test: Any, policy: Optional[PolicyFn] = None) -> EpisodeResult:
        """Run one full episode for one test.

        `test` is expected to have `.id`, `.name`, and `.prompt` attributes
        (the SDK `Test` model does).
        """
        result = EpisodeResult(test_id=str(test.id), test_name=str(test.name))
        active_policy = self._resolve_policy(policy)

        env = None
        run = None
        should_delete_env = True

        try:
            env = self.client.init_env(testId=test.id)
            result.environment_id = env.environmentId

            run = self.client.start_run(envId=env.environmentId, testId=test.id)
            result.run_id = run.runId

            context = EpisodeContext(
                client=self.client,
                environment_id=env.environmentId,
                run_id=run.runId,
                test_id=str(test.id),
            )
            result.policy_output = active_policy(test.prompt, context)
            self._populate_policy_metadata(result)

        except Exception as exc:
            result.policy_error = f"{exc.__class__.__name__}: {exc}"

        # Always attempt evaluation if a run exists, even after policy errors.
        if run is not None:
            try:
                self.client.evaluate_run(runId=run.runId)
                final = self.client.get_results_for_run(runId=run.runId)
                result.raw_result = final
                result.passed = bool(final.passed)
                result.failures = list(final.failures or [])

                score = final.score or {}
                percent = score.get("percent") if isinstance(score, dict) else None
                if isinstance(percent, (int, float)):
                    result.score_percent = float(percent)
                else:
                    result.score_percent = 100.0 if result.passed else 0.0

                result.reward = float(self.reward_fn(result))
            except Exception as exc:
                result.eval_error = f"{exc.__class__.__name__}: {exc}"

        if self.keep_env_on_error and (result.policy_error or result.eval_error):
            should_delete_env = False

        if env is not None and should_delete_env:
            try:
                self.client.delete_env(envId=env.environmentId)
            except Exception:
                # Cleanup failure should not hide the episode outcome.
                pass

        return result

    def run_many(self, tests: list[Any], policy: Optional[PolicyFn] = None) -> list[EpisodeResult]:
        """Run a batch of episodes serially.

        Keep this simple first; parallel rollouts can be added after correctness.
        """
        outputs: list[EpisodeResult] = []
        for test in tests:
            outputs.append(self.run_episode(test, policy=policy))
        return outputs

    async def run_episode_async(
        self,
        test: Any,
        policy: Optional[PolicyFn] = None,
    ) -> EpisodeResult:
        """Async wrapper around run_episode for concurrent rollouts."""
        return await asyncio.to_thread(self.run_episode, test, policy)

    async def run_many_async(
        self,
        tests: list[Any],
        policy: Optional[PolicyFn] = None,
        *,
        max_concurrency: int = 5,
    ) -> list[EpisodeResult]:
        """Run a batch of episodes concurrently with bounded parallelism."""
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")

        semaphore = asyncio.Semaphore(max_concurrency)
        resolved_policy = self._resolve_policy(policy)

        async def _run_one(index: int, test: Any) -> tuple[int, EpisodeResult]:
            async with semaphore:
                episode_result = await asyncio.to_thread(
                    self.run_episode,
                    test,
                    resolved_policy,
                )
                return index, episode_result

        tasks = [_run_one(index, test) for index, test in enumerate(tests)]
        indexed_results = await asyncio.gather(*tasks)
        indexed_results.sort(key=lambda pair: pair[0])
        return [result for _, result in indexed_results]


def print_episode_summary(result: EpisodeResult) -> None:
    """Human-readable summary for quick debugging while learning."""
    print(
        f"test={result.test_name} "
        f"passed={result.passed} "
        f"score={result.score_percent:.1f} "
        f"reward={result.reward:.3f} "
        f"iters={result.policy_iterations} "
        f"run_id={result.run_id}"
    )

    if result.policy_error:
        print(f"policy_error: {result.policy_error}")
    if result.eval_error:
        print(f"eval_error: {result.eval_error}")
    if result.failures:
        print("failures:")
        for f in result.failures:
            print(f"  - {f}")

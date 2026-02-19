"""Policy implementations.

Keep this module as a collection of interchangeable policy functions/factories.
"""
from __future__ import annotations

from typing import Optional

from rl.agent_runners import ReActRunner
from rl.types import EpisodeContext, PolicyOutput


class ReActPolicy:
    """Policy adapter that runs the existing ReActRunner inside EpisodeRunner."""

    def __init__(
        self,
        *,
        runner: Optional[ReActRunner] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        service: str = "slack",
        system_prompt: Optional[str] = None,
        prompt_template: Optional[str] = None,
        max_iterations: Optional[int] = None,
    ):
        if runner is not None:
            if model_name is not None or api_key is not None:
                raise ValueError(
                    "Pass either `runner` or (`model_name`, `api_key`), not both."
                )
            self.runner = runner
        else:
            if not model_name or not api_key:
                raise ValueError(
                    "`model_name` and `api_key` are required when `runner` is not provided."
                )
            self.runner = ReActRunner(
                model_name=model_name,
                api_key=api_key,
                service=service,
                system_prompt=system_prompt,
                prompt_template=prompt_template,
                max_iterations=max_iterations or 25,
            )

        self.system_prompt = system_prompt
        self.max_iterations = max_iterations

    def __call__(self, prompt: str, context: EpisodeContext) -> PolicyOutput:
        bash_executor = context.make_bash_executor()
        trace_raw = self.runner.run_react_agent(
            task_prompt=prompt,
            bash_executor=bash_executor,
            system_prompt=self.system_prompt,
            max_iterations=self.max_iterations,
        )

        trace = trace_raw if isinstance(trace_raw, dict) else {"runner_output": trace_raw}
        return PolicyOutput(trace=trace, raw=trace_raw)

    def run_react_agent(self, prompt: str, context: EpisodeContext) -> PolicyOutput:
        """Compatibility helper while migrating call sites to __call__."""
        return self.__call__(prompt, context)

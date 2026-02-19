import asyncio
import re
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx
from agent_diff import AgentDiff, BashExecutorProxy


class ReActRunner:
    """Class-based ReAct runner for AgentDiff benchmark-style rollouts."""

    SERVICE_CONFIG = {
        "slack": {
            "name": "Slack",
            "base_url": "https://slack.com/api",
            "description": "Slack workspace messaging and collaboration API",
            "extra_context": "",
        },
        "box": {
            "name": "Box",
            "base_url": "https://api.box.com/2.0",
            "description": "Box cloud storage and file management API",
            "extra_context": "",
        },
        "calendar": {
            "name": "Google Calendar",
            "base_url": "https://www.googleapis.com/calendar/v3",
            "description": "Google Calendar scheduling and events API",
            "extra_context": "- **Current Date/Time**: Sunday, June 17, 2018 at 00:01 (midnight), timezone America/Los_Angeles. Use this as the reference point for all relative date/time expressions like 'today', 'tomorrow', 'this Saturday', etc.",
        },
        "linear": {
            "name": "Linear",
            "base_url": "https://api.linear.app/graphql",
            "description": "Linear project management and issue tracking API",
            "extra_context": "",
        },
    }

    DEFAULT_SYSTEM_PROMPT = """You are an AI assistant that completes tasks by interacting with APIs via bash commands.

## Current Session
- **Service**: {service_name}
- **Base URL**: {base_url}
- **Description**: {service_description}
{extra_context}

## Environment
- You are authenticated as a user in the {service_name} workspace/account.
- Authentication is handled automatically via proxy. Use placeholder tokens like `<TOKEN>` where credentials would go.
- You execute bash commands (primarily curl) to interact with the {service_name} API.
- If you are not sure how to use {service_name} API, explore the endpoint, parameters, and learn how it works.
- The environment is stateless between commands - you cannot install packages or persist files.

## Response Format
You must respond using XML tags. Think step-by-step, then execute a command OR declare completion.

**To execute a bash command:**
<thinking>
Your reasoning about what needs to be done and why this command will help.
</thinking>

<action>
Your bash command here (e.g., curl request)
</action>

**When the task is complete:**
<thinking>
Your reasoning confirming the task is done based on API responses.
</thinking>

<done>
Brief summary of what was accomplished.
</done>

## Rules
1. Execute ONE command at a time, then wait for the result.
2. Parse API responses carefully - extract IDs and data needed for subsequent calls.
3. If a command fails, analyze the error and try a different approach.
4. Only use <done> when the task is fully completed (not just when you've gathered information).
"""

    def __init__(
        self,
        *,
        model_name: str,
        api_key: str,
        service: str = "slack",
        system_prompt: Optional[str] = None,
        prompt_template: Optional[str] = None,
        test_timeout_seconds: int = 300,
        max_iterations: int = 25,
        client: Optional[AgentDiff] = None,
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.service = service
        self.prompt_template = prompt_template or self.DEFAULT_SYSTEM_PROMPT
        self.system_prompt = system_prompt or self.build_system_prompt(
            service=self.service,
            prompt_template=self.prompt_template,
        )
        self.test_timeout_seconds = test_timeout_seconds
        self.max_iterations = max_iterations
        self.client = client or AgentDiff()

    @classmethod
    def build_system_prompt(
        cls,
        service: str,
        *,
        prompt_template: Optional[str] = None,
        service_config: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> str:
        """Build service-specific ReAct system prompt."""
        template = prompt_template or cls.DEFAULT_SYSTEM_PROMPT
        config_map = service_config or cls.SERVICE_CONFIG
        config = config_map.get(
            service.lower(),
            {
                "name": service,
                "base_url": "unknown",
                "description": f"{service} API",
                "extra_context": "",
            },
        )
        extra_context = config.get("extra_context", "")
        return template.format(
            service_name=config["name"],
            base_url=config["base_url"],
            service_description=config["description"],
            extra_context=extra_context,
        )

    @staticmethod
    def parse_react_response(response: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Parse ReAct XML response -> (thinking, action, done)."""
        thinking_match = re.search(r"<thinking>(.*?)</thinking>", response, re.DOTALL)
        action_match = re.search(r"<action>(.*?)</action>", response, re.DOTALL)
        done_match = re.search(r"<done>(.*?)</done>", response, re.DOTALL)

        thinking = thinking_match.group(1).strip() if thinking_match else None
        action = action_match.group(1).strip() if action_match else None
        done = done_match.group(1).strip() if done_match else None
        return thinking, action, done

    @staticmethod
    def _new_trace_accumulator() -> Dict[str, Any]:
        return {
            "steps": [],
            "final": None,
            "completed": False,
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
            },
        }

    def call_openrouter(
        self,
        *,
        model: str,
        messages: List[Dict[str, Any]],
        max_retries: int = 3,
        base_delay: float = 2.0,
    ) -> Dict[str, Any]:
        """Call OpenRouter and normalize usage/response fields."""
        import random

        last_error = None

        for attempt in range(max_retries):
            try:
                with httpx.Client(timeout=120) as client:
                    response = client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                        },
                        json={"model": model, "messages": messages},
                    )
                    response.raise_for_status()
                    data = response.json()

                    choice = data["choices"][0]
                    usage = data.get("usage", {})

                    return {
                        "content": choice["message"]["content"],
                        "finish_reason": choice.get("finish_reason"),
                        "usage": {
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "total_tokens": usage.get("total_tokens", 0),
                            "cost": usage.get("cost", 0.0),
                        },
                    }
            except (
                httpx.HTTPStatusError,
                httpx.ConnectError,
                httpx.ReadError,
                httpx.RemoteProtocolError,
            ) as e:
                last_error = e
                should_retry = False
                if isinstance(e, httpx.HTTPStatusError):
                    should_retry = e.response.status_code in (400, 429, 500, 502, 503, 504)
                else:
                    should_retry = True

                if should_retry and attempt < max_retries - 1:
                    delay = base_delay * (2**attempt) + random.uniform(0, 1)
                    print(
                        f"[RETRY] OpenRouter request failed (attempt {attempt + 1}/{max_retries}): "
                        f"{e}. Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)
                    continue
                raise

        raise last_error if last_error is not None else RuntimeError("OpenRouter request failed after retries")

    def run_react_agent(
        self,
        *,
        task_prompt: str,
        bash_executor: BashExecutorProxy,
        system_prompt: Optional[str] = None,
        max_iterations: Optional[int] = None,
        trace_accumulator: Optional[Dict[str, Any]] = None,
        stop_event: Optional["threading.Event"] = None,
    ) -> Dict[str, Any]:
        """Run ReAct XML loop and return benchmark-style trace object."""
        effective_prompt = system_prompt or self.system_prompt
        iteration_limit = max_iterations or self.max_iterations

        messages = [
            {"role": "system", "content": effective_prompt},
            {"role": "user", "content": f"Task: {task_prompt}"},
        ]

        if trace_accumulator is not None:
            steps = trace_accumulator.setdefault("steps", [])
            trace_accumulator["final"] = None
            trace_accumulator["completed"] = False
            trace_accumulator["usage"] = self._new_trace_accumulator()["usage"]
        else:
            steps = []

        final_step = None
        completed = False
        total_usage = self._new_trace_accumulator()["usage"]

        iteration = -1
        for iteration in range(iteration_limit):
            if stop_event and stop_event.is_set():
                break

            try:
                api_response = self.call_openrouter(model=self.model_name, messages=messages)
                response_text = api_response["content"]
                finish_reason = api_response["finish_reason"]
                iter_usage = api_response["usage"]

                total_usage["prompt_tokens"] += iter_usage["prompt_tokens"]
                total_usage["completion_tokens"] += iter_usage["completion_tokens"]
                total_usage["total_tokens"] += iter_usage["total_tokens"]
                total_usage["cost"] += iter_usage["cost"]

                if trace_accumulator is not None:
                    trace_accumulator["usage"] = total_usage.copy()

            except Exception as e:
                steps.append({"iteration": iteration + 1, "error": f"API error: {str(e)}"})
                break

            thinking, action, done = self.parse_react_response(response_text)

            if action:
                try:
                    result = bash_executor.execute(action)
                    if isinstance(result, dict):
                        observation = {
                            "stdout": result.get("stdout", ""),
                            "stderr": result.get("stderr", ""),
                            "exit_code": result.get("exit_code", 0),
                        }
                    else:
                        observation = {
                            "stdout": str(result) if result else "",
                            "stderr": "",
                            "exit_code": 0,
                        }
                except Exception as e:
                    observation = {
                        "stdout": "",
                        "stderr": str(e),
                        "exit_code": 1,
                        "error": str(e),
                    }

                steps.append(
                    {
                        "iteration": iteration + 1,
                        "thinking": thinking,
                        "action": action,
                        "observation": observation,
                        "raw_response": response_text,
                        "finish_reason": finish_reason,
                        "usage": iter_usage,
                    }
                )

                if observation.get("exit_code", 0) != 0:
                    obs_text = (
                        f"{observation['stdout']}\n[stderr]: {observation['stderr']}\n"
                        f"[exit_code]: {observation['exit_code']}"
                    ).strip()
                else:
                    obs_text = observation["stdout"].strip() if observation["stdout"] else "(empty output)"

                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content": f"<observation>\n{obs_text}\n</observation>"})
            elif done:
                final_step = {
                    "iteration": iteration + 1,
                    "thinking": thinking,
                    "summary": done,
                    "raw_response": response_text,
                    "finish_reason": finish_reason,
                    "usage": iter_usage,
                }
                completed = True
                break
            else:
                steps.append(
                    {
                        "iteration": iteration + 1,
                        "thinking": thinking,
                        "warning": "No <action> or <done> tag found",
                        "raw_response": response_text,
                        "finish_reason": finish_reason,
                        "usage": iter_usage,
                    }
                )
                messages.append({"role": "assistant", "content": response_text})
                messages.append(
                    {
                        "role": "user",
                        "content": "Please respond with either an <action> to execute or <done> if the task is complete.",
                    }
                )

        result = {
            "steps": steps,
            "final": final_step,
            "iterations": iteration + 1,
            "completed": completed,
            "usage": total_usage,
        }

        if trace_accumulator is not None:
            trace_accumulator["final"] = final_step
            trace_accumulator["iterations"] = iteration + 1
            trace_accumulator["completed"] = completed
            trace_accumulator["usage"] = total_usage

        return result

    async def run_single_test(
        self,
        test: Any,
        *,
        client: Optional[AgentDiff] = None,
        test_timeout_seconds: Optional[int] = None,
        max_iterations: Optional[int] = None,
    ) -> tuple:
        """Run one benchmark test and return `(test_id, result_dict)`."""
        active_client = client or self.client
        timeout_seconds = test_timeout_seconds or self.test_timeout_seconds
        iteration_limit = max_iterations or self.max_iterations

        test_id = test.id
        prompt = test.prompt
        response = None
        timed_out = False
        env = None
        stop_event = threading.Event()

        try:
            env = active_client.init_env(testId=test_id)
            run = active_client.start_run(envId=env.environmentId, testId=test_id)

            bash_executor = BashExecutorProxy(
                env.environmentId,
                base_url=active_client.base_url,
                api_key=active_client.api_key,
            )

            trace_accumulator = self._new_trace_accumulator()

            start = time.perf_counter()
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.run_react_agent,
                        task_prompt=prompt,
                        bash_executor=bash_executor,
                        max_iterations=iteration_limit,
                        trace_accumulator=trace_accumulator,
                        stop_event=stop_event,
                    ),
                    timeout=timeout_seconds,
                )
            except asyncio.TimeoutError:
                timed_out = True
                stop_event.set()
                await asyncio.sleep(2)
                response = {
                    "steps": trace_accumulator.get("steps", []),
                    "final": trace_accumulator.get("final"),
                    "iterations": len(trace_accumulator.get("steps", [])),
                    "completed": False,
                    "usage": trace_accumulator.get("usage", {}),
                    "timeout_error": f"Test timed out after {timeout_seconds} seconds",
                }
            except Exception as e:
                response = {
                    "steps": trace_accumulator.get("steps", []),
                    "final": trace_accumulator.get("final"),
                    "iterations": len(trace_accumulator.get("steps", [])),
                    "completed": False,
                    "usage": trace_accumulator.get("usage", {}),
                    "error": str(e),
                }
            finally:
                execution_time = time.perf_counter() - start

            active_client.evaluate_run(runId=run.runId)
            run_result = active_client.get_results_for_run(runId=run.runId)

            result = {
                "prompt": prompt,
                "status": "timeout" if timed_out else run_result.status,
                "passed": False if timed_out else run_result.passed,
                "score": 0 if timed_out else run_result.score.get("percent", 0),
                "time": round(execution_time, 2),
                "failures": ["Test timed out"] if timed_out else run_result.failures,
                "runId": run.runId,
                "trace": response,
                "diff": getattr(run_result, "diff", None),
            }

            active_client.delete_env(envId=env.environmentId)
            return test_id, result
        except Exception as e:
            if env:
                try:
                    active_client.delete_env(envId=env.environmentId)
                except Exception:
                    pass
            return test_id, {"passed": False, "score": 0, "status": "error", "error": str(e)}

    def run_single_test_sync(
        self,
        test: Any,
        *,
        client: Optional[AgentDiff] = None,
        test_timeout_seconds: Optional[int] = None,
        max_iterations: Optional[int] = None,
    ) -> tuple:
        """Synchronous helper wrapper for scripts/REPL usage."""
        return asyncio.run(
            self.run_single_test(
                test,
                client=client,
                test_timeout_seconds=test_timeout_seconds,
                max_iterations=max_iterations,
            )
        )

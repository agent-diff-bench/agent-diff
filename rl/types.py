"""Shared types for RL orchestration modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol

from agent_diff import AgentDiff


class PolicyFn(Protocol):
    """Callable policy interface used by EpisodeRunner."""

    def __call__(self, prompt: str, context: "EpisodeContext") -> "PolicyOutput":
        ...


@dataclass(slots=True)
class PolicyOutput:
    """Thin container for policy-returned artifacts (primarily runner trace)."""

    action_count: int = 0
    trace: dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass(slots=True)
class EpisodeContext:
    """Context passed into a policy callback."""

    client: AgentDiff
    environment_id: str
    run_id: str
    test_id: str

    def make_python_executor(self):
        """Create a PythonExecutorProxy bound to this episode environment."""
        from agent_diff import PythonExecutorProxy

        return PythonExecutorProxy(
            self.environment_id,
            base_url=self.client.base_url,
            api_key=self.client.api_key,
        )

    def make_bash_executor(self):
        """Create a BashExecutorProxy bound to this episode environment."""
        from agent_diff import BashExecutorProxy

        return BashExecutorProxy(
            self.environment_id,
            base_url=self.client.base_url,
            api_key=self.client.api_key,
        )


@dataclass(slots=True)
class EpisodeResult:
    """Structured output from one episode rollout."""

    test_id: str
    test_name: str
    environment_id: Optional[str] = None
    run_id: Optional[str] = None
    passed: bool = False
    score_percent: float = 0.0
    reward: float = 0.0
    failures: list[str] = field(default_factory=list)
    policy_output: Optional[PolicyOutput] = None
    policy_iterations: int = 0
    policy_completed: Optional[bool] = None
    policy_usage: dict[str, Any] = field(default_factory=dict)
    policy_error: Optional[str] = None
    eval_error: Optional[str] = None
    raw_result: Any = None


RewardFn = Callable[[EpisodeResult], float]

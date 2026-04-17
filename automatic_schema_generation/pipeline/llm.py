"""LLM client helpers for pipeline.

Thin wrappers around the Claude CLI and the Anthropic SDK. Each
returns a ``Callable[[str], str]`` suitable for passing to
``review_suggestions.review_suggestions(llm_call=...)``.

Both backends are available side-by-side; the caller picks one.

Usage::

    from pipeline.llm import make_llm_call

    llm_call = make_llm_call(backend="claude_code", model="claude-sonnet-4-5")
    # or
    llm_call = make_llm_call(backend="anthropic", model="claude-sonnet-4-5")

    reviewed = review_suggestions(suggestions, spec, config, llm_call)
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable


def make_llm_call(
    *,
    backend: str = "claude_code",
    model: str = "claude-sonnet-4-5",
    timeout: int = 600,
    max_tokens: int = 16000,
) -> Callable[[str], str]:
    """Return a ``prompt → response`` callable for the chosen backend."""
    if backend == "claude_code":
        return _make_claude_code_call(model=model, timeout=timeout)
    if backend == "anthropic":
        return _make_anthropic_call(model=model, max_tokens=max_tokens)
    raise ValueError(
        f"Unknown backend: {backend!r}. Expected 'claude_code' or 'anthropic'."
    )


def _make_claude_code_call(
    *, model: str, timeout: int,
) -> Callable[[str], str]:
    """Claude CLI backend — uses subscription auth, no API key needed."""

    def call(prompt: str) -> str:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        try:
            result = subprocess.run(
                ["claude", "-p", "--model", model],
                input=prompt,
                capture_output=True,
                text=True,
                env=env,
                timeout=timeout,
            )
        except FileNotFoundError:
            raise RuntimeError(
                "claude CLI not found on PATH. Install Claude Code, or "
                "switch to the 'anthropic' backend."
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude -p timed out after {timeout}s")
        if result.returncode != 0:
            raise RuntimeError(
                f"claude -p failed (exit {result.returncode}):\n"
                f"{result.stderr.strip()}"
            )
        return result.stdout.strip()

    return call


def _make_anthropic_call(
    *, model: str, max_tokens: int,
) -> Callable[[str], str]:
    """Anthropic SDK backend — requires ANTHROPIC_API_KEY env var."""

    def call(prompt: str) -> str:
        import anthropic

        client = anthropic.Anthropic()
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        text_parts = []
        for block in message.content:
            if block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts)

    return call

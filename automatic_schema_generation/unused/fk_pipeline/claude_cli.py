"""Thin subprocess wrapper around the ``claude`` CLI.

Mirrors the pattern established in ``pipeline/implementer.py::_call_claude_code``
but with different timeouts and JSON-parsing behavior suited to the
short, structured calls this pipeline makes:

  * Short timeout (60s default) — these are cheap Haiku calls, not
    long implementation prompts. Anything longer than a minute is a
    hang, not legitimate work.

  * Defensive JSON extraction — Claude CLI doesn't expose schema-
    constrained output, so we rely on prompting the model to emit
    JSON-only and parse the result. A single retry fixes the most
    common failure mode (Haiku prefacing the JSON with a short
    explanation despite being told not to).

  * No API key required — same as the existing wrapper, we rely on
    the user's Claude Code subscription auth. ``ANTHROPIC_API_KEY``
    is stripped from the subprocess env to prevent accidental API
    billing when both are present.

This module deliberately knows nothing about what the caller is asking
Claude to do. It's a transport layer. ``vocabulary.py`` owns the prompt,
the schema expectations, and the retry policy for alias-expansion calls.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from typing import Any


class ClaudeCliError(RuntimeError):
    """Any failure in the claude CLI transport layer.

    Carries the raw stdout/stderr so callers can surface a useful
    debugging message without having to re-run.
    """

    def __init__(
        self,
        message: str,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int | None = None,
    ) -> None:
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class ClaudeCliJsonParseError(ClaudeCliError):
    """Raised when the CLI succeeded but the response wasn't parseable JSON.

    Separate from the generic error so callers can distinguish "Claude
    is unreachable" from "Claude responded but mangled the format" and
    implement different retry policies.
    """


# How long a single Haiku call is allowed to take. Haiku typically
# responds in <5 seconds for small prompts, so 60 is generous. Bumped
# only if we start seeing legitimate timeouts in practice.
DEFAULT_TIMEOUT_SECONDS: int = 60


def check_claude_cli_available() -> None:
    """Raise if the ``claude`` binary isn't on PATH.

    Called early by the CLI entry point so users get a helpful message
    instead of a FileNotFoundError deep inside a subprocess call.
    """
    if shutil.which("claude") is None:
        raise ClaudeCliError(
            "claude CLI not found on PATH. Install Claude Code from "
            "https://claude.com/claude-code, or set the ``model`` config "
            "to use a different backend once one is added."
        )


def call_claude_text(
    prompt: str,
    model: str,
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> str:
    """Send a one-shot prompt to the claude CLI and return the text response.

    The prompt is piped via stdin rather than passed as an argument,
    which is safer for long or shell-metacharacter-laden content and
    avoids ARG_MAX limits.

    Raises:
        ClaudeCliError: if the binary is missing, the call times out,
            or the CLI exits with a non-zero status.
    """
    env = os.environ.copy()
    # See pipeline/implementer.py — when ANTHROPIC_API_KEY is set,
    # ``claude -p`` silently uses it (and bills API credits) instead
    # of the Claude Code subscription. Strip it so this pipeline's
    # cost attribution matches user expectations.
    env.pop("ANTHROPIC_API_KEY", None)

    try:
        result = subprocess.run(
            ["claude", "-p", "--model", model],
            input=prompt,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        raise ClaudeCliError(
            "claude CLI not found on PATH. Install Claude Code from "
            "https://claude.com/claude-code."
        )
    except subprocess.TimeoutExpired as e:
        raise ClaudeCliError(
            f"claude -p timed out after {timeout}s",
            stdout=(e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""),
            stderr=(e.stderr or b"").decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or ""),
        )

    if result.returncode != 0:
        raise ClaudeCliError(
            f"claude -p failed (exit {result.returncode}): {result.stderr.strip()}",
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
        )

    return result.stdout.strip()


# Matches a fenced code block with optional language tag, capturing the
# body. Used as a fallback when the whole response isn't valid JSON but
# a JSON block is embedded inside a ```json ... ``` fence.
_FENCED_JSON_RE = re.compile(
    r"```(?:json)?\s*\n?(.*?)\n?```",
    re.DOTALL,
)


def extract_json(response_text: str) -> Any:
    """Extract a JSON value from a Claude response.

    Tried in order:
      1. Parse the whole stripped response as JSON.
      2. Find a fenced ``` ```json ... ``` `` code block and parse its body.
      3. Find the outermost balanced ``{...}`` span via brace matching
         and parse that. Handles the common "Haiku prefaces JSON with
         explanatory text" failure mode.

    Raises ``ClaudeCliJsonParseError`` if none of those succeed. The
    error carries the raw response so the caller can log it to a debug
    file and inspect what Haiku actually produced.
    """
    text = response_text.strip()
    if not text:
        raise ClaudeCliJsonParseError(
            "claude returned empty response where JSON was expected",
            stdout=response_text,
        )

    # Attempt 1: whole response
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Attempt 2: fenced code block
    fence_match = _FENCED_JSON_RE.search(text)
    if fence_match:
        fenced_body = fence_match.group(1).strip()
        try:
            return json.loads(fenced_body)
        except json.JSONDecodeError:
            pass

    # Attempt 3: outermost balanced braces
    span = _find_outermost_json_span(text)
    if span is not None:
        try:
            return json.loads(span)
        except json.JSONDecodeError:
            pass

    raise ClaudeCliJsonParseError(
        "claude response did not contain parseable JSON",
        stdout=response_text,
    )


def _find_outermost_json_span(text: str) -> str | None:
    """Return the outermost balanced ``{...}`` or ``[...]`` substring.

    Walks character-by-character tracking brace/bracket depth, with
    string-literal awareness so braces inside strings don't throw off
    the count. Returns the first balanced span found from left to
    right; if the response contains multiple JSON values, only the
    first is returned (which is what we want — later values are
    usually duplicate explanations).
    """
    start = -1
    depth = 0
    in_string = False
    escape = False
    opener = ""
    closer = ""

    for i, ch in enumerate(text):
        if start == -1:
            if ch in "{[":
                start = i
                opener = ch
                closer = "}" if ch == "{" else "]"
                depth = 1
            continue

        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    return None


def call_claude_json(
    prompt: str,
    model: str,
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = 1,
) -> Any:
    """Call the claude CLI and parse the response as JSON.

    On parse failure (but CLI success), retries up to ``max_retries``
    times with an error-correction prompt appended to the original.
    This handles the most common Haiku failure mode where it wraps
    the JSON in a short explanation despite being asked not to.

    Transport failures (missing CLI, non-zero exit, timeout) are
    propagated immediately without retry — they won't fix themselves.
    """
    attempt = 0
    last_raw = ""

    while True:
        if attempt == 0:
            full_prompt = prompt
        else:
            full_prompt = (
                prompt
                + "\n\n---\n\nIMPORTANT: Your previous response could not "
                + "be parsed as JSON. Respond with ONLY a valid JSON "
                + "object — no prose, no markdown, no code fences, just "
                + "the JSON value itself."
            )

        last_raw = call_claude_text(full_prompt, model, timeout=timeout)
        try:
            return extract_json(last_raw)
        except ClaudeCliJsonParseError:
            if attempt >= max_retries:
                raise ClaudeCliJsonParseError(
                    f"claude JSON parse failed after {attempt + 1} attempt(s). "
                    f"Last response: {last_raw[:500]}",
                    stdout=last_raw,
                )
            attempt += 1

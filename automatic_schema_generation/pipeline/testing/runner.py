"""End-to-end endpoint verification stage.

Groups untested endpoints from ``test_registry.json`` by ``subject``,
chunks each subject into batches of N (default 5), builds a prompt that
hands the LLM full schema metadata + instructions for driving the live
replica via curl, and invokes ``claude -p``. The LLM writes a structured
JSON results file which is parsed back and merged into the registry.

The prompt explicitly allows the LLM to edit replica source files when it
finds bugs, since the dev backend runs uvicorn with ``--reload`` and picks
up edits without a restart. There is no automatic regression check across
batches — see ``run_test_endpoints(force=True)`` to retest everything.
"""

from __future__ import annotations

import json
import os
import subprocess
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

_PROMPT_TEMPLATE = Path(__file__).parent / "test_prompt.md"


def group_by_subject(
    test_entries: list[dict[str, Any]],
    *,
    include_tested: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    """Bucket entries by ``subject`` field, skipping already-tested ones."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in test_entries:
        if not include_tested and entry.get("tested"):
            continue
        subject = entry.get("subject") or "_unknown"
        grouped[subject].append(entry)
    return dict(grouped)


def chunk(entries: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [entries[index:index + batch_size] for index in range(0, len(entries), batch_size)]


def collect_schema_closure(
    endpoints: list[dict[str, Any]],
    implemented_doc: dict[str, Any],
) -> dict[str, Any]:
    """Walk ``$ref`` chains starting from each endpoint's responses + body.

    Refs in ``implemented_endpoints.json`` use the ``#/schemas/<name>``
    prefix (rewritten by the extraction stage), so we resolve against the
    top-level ``schemas`` block. Returns the transitive closure as a dict
    keyed by schema name.
    """
    schemas_block = implemented_doc.get("schemas") or {}
    endpoints_block = implemented_doc.get("endpoints") or {}
    ref_prefix = "#/schemas/"

    seen_refs: set[str] = set()
    frontier: set[str] = set()

    def harvest(node: Any) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith(ref_prefix):
                frontier.add(ref[len(ref_prefix):])
            for value in node.values():
                harvest(value)
        elif isinstance(node, list):
            for item in node:
                harvest(item)

    for endpoint in endpoints:
        key = f"{endpoint['method']} {endpoint['path']}"
        meta = endpoints_block.get(key) or {}
        harvest(meta.get("responses"))
        harvest(meta.get("request_body"))
        harvest(meta.get("parameters"))

    while frontier:
        name = frontier.pop()
        if name in seen_refs:
            continue
        seen_refs.add(name)
        schema = schemas_block.get(name)
        if isinstance(schema, dict):
            harvest(schema)

    return {name: schemas_block[name] for name in sorted(seen_refs) if name in schemas_block}


def _summarize_schema(schema: dict[str, Any]) -> str:
    """Produce a one-line schema hint: ``$ref``, type, or inline JSON snippet."""
    ref = schema.get("$ref")
    if ref:
        return f"`{ref}`"
    schema_type = schema.get("type")
    if schema_type == "array":
        items = schema.get("items") or {}
        return f"array of {_summarize_schema(items)}"
    if schema.get("properties") or schema.get("oneOf") or schema.get("anyOf"):
        return f"inline: {json.dumps(schema, separators=(',', ':'))[:400]}"
    if schema_type:
        return str(schema_type)
    return "unspecified"


def render_endpoints_block(
    endpoints: list[dict[str, Any]],
    implemented_doc: dict[str, Any],
) -> str:
    """Format the per-endpoint section that goes into the prompt body.

    Includes parameters (path + required query) so the LLM knows what input
    each call needs, plus a one-line shape hint for the request body and
    each response code.
    """
    endpoints_block = implemented_doc.get("endpoints") or {}
    out: list[str] = []
    for endpoint in endpoints:
        method = endpoint["method"]
        path = endpoint["path"]
        meta = endpoints_block.get(f"{method} {path}") or {}
        out.append(f"### {method} {path}")
        summary = endpoint.get("summary") or ""
        if summary and summary != endpoint.get("subject"):
            out.append(f"_{summary}_")
        if endpoint.get("needs_seed"):
            out.append("Needs a seeded row before this endpoint can be exercised.")

        # Parameters — separate path from query/header, mark required ones.
        parameters = meta.get("parameters") or []
        path_params: list[str] = []
        query_params: list[str] = []
        for parameter in parameters:
            if not isinstance(parameter, dict):
                continue
            name = parameter.get("name") or "?"
            location = parameter.get("in")
            required = parameter.get("required")
            schema_type = (parameter.get("schema") or {}).get("type", "string")
            tag = " (required)" if required else ""
            if location == "path":
                path_params.append(f"{name}: {schema_type}{tag}")
            elif location == "query":
                query_params.append(f"{name}: {schema_type}{tag}")
        if path_params:
            out.append(f"Path parameters: {', '.join(path_params)}")
        if query_params:
            out.append(f"Query parameters: {', '.join(query_params)}")

        request_body = meta.get("request_body")
        if isinstance(request_body, dict):
            content = request_body.get("content") or {}
            for media_type, media in content.items():
                schema = media.get("schema") or {}
                out.append(f"Request body ({media_type}): {_summarize_schema(schema)}")
                break

        responses = meta.get("responses") or {}
        if responses:
            out.append("Responses:")
            for status_code in sorted(responses, key=lambda code: str(code)):
                response = responses[status_code]
                content = (response.get("content") or {}).get("application/json") or {}
                schema = content.get("schema") or {}
                description = (response.get("description") or "").strip().splitlines()
                desc = description[0] if description else ""
                shape = _summarize_schema(schema) if schema else "no body"
                out.append(f"  - {status_code}: {shape} — {desc}")
        out.append("")
    return "\n".join(out)


def _mount_suffix_for_slug(replicas_yaml: Path, app_slug: str) -> str:
    """Recover the optional path suffix (e.g. ``/api/v1``) from replicas.yaml."""
    if not replicas_yaml.exists():
        return ""
    raw = yaml.safe_load(replicas_yaml.read_text()) or {}
    for entry in raw.get("rest") or []:
        if entry.get("slug") != app_slug:
            continue
        mount_path = entry.get("mount_path", "")
        marker = f"/services/{app_slug}"
        if marker in mount_path:
            return mount_path.split(marker, 1)[1]
    return ""


def _shorten_path(path: Path, anchor: Path) -> str:
    """Render ``path`` relative to ``anchor`` if possible, else return its name."""
    try:
        return str(path.resolve().relative_to(anchor.resolve()))
    except ValueError:
        return path.name


def build_test_prompt(
    *,
    app_name: str,
    app_slug: str,
    target_dir: Path,
    subject: str,
    batch_index: int,
    batch_total: int,
    endpoints: list[dict[str, Any]],
    implemented_doc: dict[str, Any],
    replicas_yaml: Path,
    output_path: Path,
    max_iterations: int,
    repo_root: Path,
) -> str:
    schemas = collect_schema_closure(endpoints, implemented_doc)
    placeholders = {
        "APP_NAME": app_name,
        "APP_SLUG": app_slug,
        "SUBJECT": subject,
        "BATCH_INDEX": str(batch_index),
        "BATCH_TOTAL": str(batch_total),
        "ENDPOINT_COUNT": str(len(endpoints)),
        "TARGET_DIR_RELATIVE": _shorten_path(target_dir, repo_root),
        "MOUNT_SUFFIX_HINT": _mount_suffix_for_slug(replicas_yaml, app_slug),
        "ENDPOINTS_BLOCK": render_endpoints_block(endpoints, implemented_doc),
        "SCHEMAS_JSON": json.dumps(schemas, indent=2),
        "OUTPUT_PATH": _shorten_path(output_path, repo_root),
        "MAX_ITERATIONS": str(max_iterations),
    }
    template = _PROMPT_TEMPLATE.read_text()
    for key, value in placeholders.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def parse_results_file(output_path: Path) -> list[dict[str, Any]]:
    """Read the LLM's structured output. Returns [] on missing/malformed."""
    if not output_path.exists():
        return []
    try:
        payload = json.loads(output_path.read_text())
    except json.JSONDecodeError:
        return []
    results = payload.get("results")
    if not isinstance(results, list):
        return []
    return results


def merge_into_registry(
    registry_path: Path,
    results: list[dict[str, Any]],
) -> int:
    """Mark matching entries as tested + attach the LLM's diagnosis."""
    registry = json.loads(registry_path.read_text())
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for result in results:
        method = (result.get("method") or "").upper()
        path = result.get("path") or ""
        if not method or not path:
            continue
        by_key[(method, path)] = result

    updated_count = 0
    for entry in registry.get("endpoints", []):
        key = (entry["method"], entry["path"])
        result = by_key.get(key)
        if result is None:
            continue
        entry["tested"] = True
        entry["test_result"] = {
            "passed": bool(result.get("passed")),
            "iterations": result.get("iterations"),
            "diagnosis": result.get("diagnosis"),
            "curl_examples": result.get("curl_examples") or [],
            "code_changes": result.get("code_changes") or [],
        }
        updated_count += 1

    registry_path.write_text(json.dumps(registry, indent=2))
    return updated_count


def _invoke_claude(prompt: str, *, model: str, timeout: int) -> tuple[int, str, str]:
    """Run ``claude -p`` with full tool access and return (rc, stdout, stderr)."""
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
    except FileNotFoundError as exc:
        raise RuntimeError("claude CLI not found on PATH") from exc
    except subprocess.TimeoutExpired:
        return (124, "", f"claude -p timed out after {timeout}s")
    return (result.returncode, result.stdout, result.stderr)


def run_test_endpoints(
    *,
    config_path: Path,
    app_name: str,
    app_slug: str,
    target_dir: Path,
    output_dir: Path,
    replicas_yaml: Path,
    repo_root: Path,
    model: str,
    batch_size: int = 7,
    max_iterations: int = 3,
    force: bool = False,
    dry_run: bool = False,
    timeout: int = 1800,
    only_subjects: list[str] | None = None,
    invoke: Callable[[str, str, int], tuple[int, str, str]] | None = None,
) -> dict[str, Any]:
    """Drive the full test stage. Returns a summary dict for logging."""
    registry_path = output_dir / "test_registry.json"
    implemented_path = output_dir / "implemented_endpoints.json"
    if not registry_path.exists() or not implemented_path.exists():
        return {
            "skipped": True,
            "reason": "test_registry.json or implemented_endpoints.json missing — run register_tests first",
        }

    registry = json.loads(registry_path.read_text())
    implemented_doc = json.loads(implemented_path.read_text())

    grouped = group_by_subject(registry.get("endpoints") or [], include_tested=force)
    if only_subjects:
        grouped = {name: items for name, items in grouped.items() if name in set(only_subjects)}

    if not grouped:
        return {"skipped": True, "reason": "nothing to test (all endpoints already tested — pass --force to retest)"}

    prompt_dir = config_path.parent / "pipeline_prompts"
    results_dir = output_dir / "test_results"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "subjects": {},
        "total_batches": 0,
        "endpoints_attempted": 0,
        "endpoints_recorded": 0,
        "endpoints_passed": 0,
    }

    invoke_fn = invoke or (lambda prompt, model, timeout: _invoke_claude(prompt, model=model, timeout=timeout))

    for subject in sorted(grouped):
        endpoints = grouped[subject]
        batches = chunk(endpoints, batch_size)
        summary["total_batches"] += len(batches)
        subject_summary = {"batches": len(batches), "endpoints": len(endpoints), "passed": 0, "recorded": 0}

        for batch_index, batch in enumerate(batches, start=1):
            output_path = results_dir / f"{subject}_batch{batch_index}.json"
            prompt = build_test_prompt(
                app_name=app_name,
                app_slug=app_slug,
                target_dir=target_dir,
                subject=subject,
                batch_index=batch_index,
                batch_total=len(batches),
                endpoints=batch,
                implemented_doc=implemented_doc,
                replicas_yaml=replicas_yaml,
                output_path=output_path,
                max_iterations=max_iterations,
                repo_root=repo_root,
            )
            (prompt_dir / f"test_{subject}_batch{batch_index}.md").write_text(prompt)
            summary["endpoints_attempted"] += len(batch)

            if dry_run:
                print(f"  [dry-run] {subject} batch {batch_index}/{len(batches)} — {len(batch)} endpoints, prompt at pipeline_prompts/test_{subject}_batch{batch_index}.md")
                continue

            print(f"  {subject} batch {batch_index}/{len(batches)} — {len(batch)} endpoints, calling {model} (timeout {timeout}s)...")
            if output_path.exists():
                output_path.unlink()
            return_code, stdout, stderr = invoke_fn(prompt, model, timeout)
            if return_code != 0:
                print(f"    [warn] claude exit {return_code}: {stderr.strip()[:300]}")

            results = parse_results_file(output_path)
            if not results:
                print(f"    [warn] no parseable results at {output_path} — endpoints in this batch stay untested")
                continue
            updated = merge_into_registry(registry_path, results)
            passed = sum(1 for result in results if result.get("passed"))
            summary["endpoints_recorded"] += updated
            summary["endpoints_passed"] += passed
            subject_summary["recorded"] += updated
            subject_summary["passed"] += passed
            print(f"    recorded {updated}/{len(batch)}; {passed} passed")

        summary["subjects"][subject] = subject_summary

    return summary

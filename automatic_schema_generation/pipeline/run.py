"""Pipeline orchestrator — runs all stages end-to-end.

Usage::

    # Full pipeline (init → configure → extract → implement):
    python -m pipeline.run app.yaml

    # Single stage:
    python -m pipeline.run app.yaml --stage init
    python -m pipeline.run app.yaml --stage configure
    python -m pipeline.run app.yaml --stage extract
    python -m pipeline.run app.yaml --stage implement

    # Single resource:
    python -m pipeline.run app.yaml --resource gists

    # Dry run (build prompts, don't call LLM):
    python -m pipeline.run app.yaml --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from pipeline.aliases.apply import _patch_config
from pipeline.aliases.review import review_suggestions
from pipeline.aliases.suggest import suggest_aliases
from pipeline.config import PipelineConfig, auto_configure_resources, load_config
from pipeline.documentation.endpoints import generate_endpoints_document
from pipeline.documentation.resources import generate_resources_document
from pipeline.extraction.schema_bindings import build_schema_bindings
from pipeline.implementation.build_prompt import build_pass1_prompt, build_pass2_prompt
from pipeline.llm import make_llm_call
from pipeline.register_tests import build_test_registry, scan_implemented_routes, write_registry
from pipeline.scaffold import detect_mount_suffix, generate_scaffold

_STAGES = ["init", "configure", "suggest_aliases", "extract", "implement_responses", "implement", "register_tests"]


def run_pipeline(
    config_path: Path,
    stage: str = "all",
    dry_run: bool = False,
    only_resources: list[str] | None = None,
    configure_model: str = "claude-sonnet-4-5",
    implement_model: str = "claude-opus-4-6",
) -> None:
    stages = _STAGES if stage == "all" else [stage]

    # --- Stage: Init ---
    if "init" in stages:
        print("\n=== INIT — scaffold + register replica ===")
        raw = yaml.safe_load(config_path.read_text()) or {}
        target_dir = (config_path.parent / raw.get("target_dir", "out")).resolve()

        # Detect API path prefix for mount path (e.g. /api/v1 for Todoist)
        openapi_path = (config_path.parent / raw.get("openapi_path", "")).resolve()
        mount_suffix = ""
        if openapi_path.exists():
            spec_for_mount = json.load(open(openapi_path))
            mount_suffix = detect_mount_suffix(spec_for_mount)
            if mount_suffix:
                print(f"  Detected API prefix: /{mount_suffix}")

        generate_scaffold(raw["app_name"], raw["app_slug"], target_dir, mount_suffix)
        print(f"  Target: {target_dir}")

    # --- Stage: Configure ---
    if "configure" in stages:
        print("\n=== CONFIGURE — LLM populates aliases and PKs ===")
        config = load_config(config_path)

        resource_names = only_resources or sorted(config.resources.aliases_by_resource.keys())
        if dry_run:
            print(f"  [dry-run] Would call {configure_model} for: {resource_names}")
        else:
            llm_call = make_llm_call(backend="claude_code", model=configure_model)
            auto_configure_resources(config_path, config.openapi_path, resource_names, llm_call)
            print(f"  Configured {len(resource_names)} resources via {configure_model}")

    # --- Stage: Suggest Aliases ---
    if "suggest_aliases" in stages:
        config = load_config(config_path)
        with open(config.openapi_path) as handle:
            spec = json.load(handle)

        print("\n=== SUGGEST ALIASES — find + review + apply schema aliases ===")
        suggestions = suggest_aliases(spec, config)
        total_candidates = sum(len(v) for v in suggestions.values())

        if total_candidates == 0:
            print("  No alias candidates found.")
        elif dry_run:
            print(f"  [dry-run] {total_candidates} candidates across {len(suggestions)} resources")
        else:
            cache_path = config_path.parent / "pipeline_cache" / "alias_review.json"
            review_model = configure_model
            llm_call = make_llm_call(backend="claude_code", model=review_model)
            print(f"  Reviewing {total_candidates} candidates via {review_model}...")
            reviewed = review_suggestions(suggestions, spec, config, llm_call, cache_path=cache_path)

            new_aliases: dict[str, list[str]] = {}
            for resource, entries in reviewed.items():
                existing = config.resources.aliases_by_resource.get(resource, frozenset())
                additions = [
                    entry.suggestion.normalized for entry in entries
                    if entry.verdict == "variant" and entry.suggestion.normalized not in existing
                ]
                if additions:
                    new_aliases[resource] = additions

            if new_aliases:
                total_new = sum(len(v) for v in new_aliases.values())
                print(f"  Applying {total_new} new aliases across {len(new_aliases)} resources...")
                patched = _patch_config(config_path.read_text(), new_aliases)
                config_path.write_text(patched)
                print(f"  Updated {config_path}")
            else:
                print("  No new aliases to apply.")

    # --- Stage: Extract ---
    if "extract" in stages:
        config = load_config(config_path)
        with open(config.openapi_path) as handle:
            spec = json.load(handle)

        print("\n=== EXTRACT — reference extraction + documentation ===")
        endpoints_doc = generate_endpoints_document(spec, config)
        resources_doc = generate_resources_document(spec, config, endpoints_doc)

        output_dir = config_path.parent / "pipeline_out"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "endpoints.json").write_text(json.dumps(endpoints_doc, indent=2))
        (output_dir / "resources.json").write_text(json.dumps(resources_doc, indent=2))

        # Extract component responses referenced by scoped endpoints
        responses_doc = _extract_responses(spec, resources_doc)
        (output_dir / "responses.json").write_text(json.dumps(responses_doc, indent=2))

        bindings = build_schema_bindings(spec, config)
        bound_count = len(bindings)
        endpoint_count = len(endpoints_doc.get("endpoints", {}))
        response_count = len(responses_doc.get("responses", {}))
        print(f"  {endpoint_count} endpoints, {bound_count} schema bindings, {response_count} component responses")
        print(f"  Wrote endpoints.json + resources.json + responses.json to {output_dir}")

    # --- Stage: Implement Responses ---
    if "implement_responses" in stages:
        config = load_config(config_path)
        output_dir = config_path.parent / "pipeline_out"
        responses_path = output_dir / "responses.json"

        if not responses_path.exists():
            print("\n=== IMPLEMENT RESPONSES — skipped (no responses.json, run extract first) ===")
        else:
            responses_doc = json.loads(responses_path.read_text())
            response_count = len(responses_doc.get("responses", {}))

            if response_count == 0:
                print("\n=== IMPLEMENT RESPONSES — skipped (no component responses in spec) ===")
            else:
                print(f"\n=== IMPLEMENT RESPONSES — {response_count} responses ({implement_model}) ===")
                prompt = (
                    f"Read the file `{responses_path.resolve()}`. It contains the "
                    f"response definitions referenced by the resources being "
                    f"implemented from the {config.app_name} API spec, along with "
                    f"their referenced schemas.\n\n"
                    f"Implement the standard HTTP error response handlers in "
                    f"`{config.target_dir}/core/errors.py`. For each standard error "
                    f"response (400 Bad Request, 401 Unauthorized, 403 Forbidden, "
                    f"404 Not Found, 500 Internal Server Error, etc.), create a "
                    f"constructor function that returns the correct response shape "
                    f"matching the schemas in the file.\n\n"
                    f"Skip domain-specific or resource-specific responses — only "
                    f"implement responses that represent standard HTTP error patterns "
                    f"reusable across the endpoints being implemented.\n\n"
                    f"Read the existing `{config.target_dir}/core/errors.py` first "
                    f"and preserve any code already there."
                )

                if dry_run:
                    prompt_dir = config_path.parent / "pipeline_prompts"
                    prompt_dir.mkdir(parents=True, exist_ok=True)
                    (prompt_dir / "implement_responses.md").write_text(prompt)
                    print(f"  [dry-run] Saved prompt to {prompt_dir}/implement_responses.md")
                else:
                    llm_call = make_llm_call(backend="claude_code", model=implement_model, timeout=600)
                    print(f"  Calling {implement_model}...")
                    llm_call(prompt)
                    print(f"  Done.")

            # Scan errors.py for implemented constructors
            constructors = _scan_error_constructors(config.target_dir / "core" / "errors.py")
            (output_dir / "implemented_responses.json").write_text(
                json.dumps({"constructors": constructors}, indent=2)
            )
            print(f"  Found {len(constructors)} error constructors: {constructors}")

    # --- Stage: Implement ---
    if "implement" in stages:
        config = load_config(config_path)
        with open(config.openapi_path) as handle:
            spec = json.load(handle)

        output_dir = config_path.parent / "pipeline_out"
        endpoints_doc = json.loads((output_dir / "endpoints.json").read_text())
        resources_doc = json.loads((output_dir / "resources.json").read_text())

        # Load implemented error constructors if available
        impl_responses_path = output_dir / "implemented_responses.json"
        implemented_constructors = []
        if impl_responses_path.exists():
            implemented_constructors = json.loads(
                impl_responses_path.read_text()
            ).get("constructors", [])

        print(f"\n=== IMPLEMENT — LLM builds entities ({implement_model}) ===")
        resource_names = only_resources or sorted(resources_doc["resources"].keys())
        order = _dependency_order(resource_names, resources_doc)
        print(f"  Order: {' → '.join(order)}")

        for index, resource_name in enumerate(order, 1):
            print(f"\n  [{index}/{len(order)}] {resource_name}")

            prompt_p1 = build_pass1_prompt(resource_name, resources_doc, endpoints_doc, config, spec=spec, implemented_constructors=implemented_constructors)
            prompt_p2 = build_pass2_prompt(resource_name, resources_doc, endpoints_doc, config, spec=spec)

            if dry_run:
                prompt_dir = config_path.parent / "pipeline_prompts"
                prompt_dir.mkdir(parents=True, exist_ok=True)
                (prompt_dir / f"{resource_name}_pass1.md").write_text(prompt_p1)
                (prompt_dir / f"{resource_name}_pass2.md").write_text(prompt_p2)
                print(f"    [dry-run] Saved prompts to {prompt_dir}")
                continue

            llm_call = make_llm_call(backend="claude_code", model=implement_model, timeout=900)

            print(f"    Pass 1 — base model ({len(prompt_p1):,} chars)...")
            llm_call(prompt_p1)

            print(f"    Pass 2 — relationships ({len(prompt_p2):,} chars)...")
            llm_call(prompt_p2)

            print(f"    Done.")

    # --- Stage: Register Tests ---
    if "register_tests" in stages:
        config = load_config(config_path)
        output_dir = config_path.parent / "pipeline_out"
        endpoints_path = output_dir / "endpoints.json"

        if not endpoints_path.exists():
            print("\n=== REGISTER TESTS — skipped (run extract first) ===")
        else:
            print("\n=== REGISTER TESTS — scanning implemented routes ===")
            # Pre-import sqlalchemy before adding backend/src to sys.path,
            # because backend has a local `platform/` package that shadows
            # the stdlib `platform` module that sqlalchemy needs.
            import sqlalchemy as _sa  # noqa: F811
            import sys
            backend_src = str(config.target_dir.parent.parent)
            if backend_src not in sys.path:
                sys.path.insert(0, backend_src)
            routes_module = f"services.{config.app_slug}.api.routes"
            try:
                implemented = scan_implemented_routes(routes_module)
                endpoints_doc = json.loads(endpoints_path.read_text())
                registry = build_test_registry(implemented, endpoints_doc, config.app_slug)

                # Build implemented_endpoints doc (subset of endpoints.json)
                endpoints_block = endpoints_doc.get("endpoints") or {}
                matched = {}
                for route in implemented:
                    key = f"{route['method']} {route['path']}"
                    if key in endpoints_block:
                        matched[key] = endpoints_block[key]

                impl_doc = {
                    "endpoints": matched,
                    "schemas": endpoints_doc.get("schemas") or {},
                }

                write_registry(output_dir, impl_doc, registry)
                print(f"  {registry['implemented_count']} implemented, "
                      f"{registry['unimplemented_count']} unimplemented "
                      f"(of {registry['total_spec_endpoints']} total)")
                print(f"  Wrote implemented_endpoints.json + test_registry.json to {output_dir}")
            except Exception as exc:
                print(f"  [error] Could not scan routes: {exc}")

    print("\nPipeline complete.")


def _scan_error_constructors(errors_path: Path) -> list[str]:
    """Extract function names from core/errors.py."""
    import re
    if not errors_path.exists():
        return []
    content = errors_path.read_text()
    return re.findall(r"^def (\w+)", content, re.MULTILINE)


def _dependency_order(
    resource_names: list[str],
    resources_doc: dict,
) -> list[str]:
    """Topological sort by outgoing references — deps first."""
    resources = resources_doc.get("resources") or {}
    name_set = set(resource_names)

    in_degree: dict[str, int] = {name: 0 for name in resource_names}
    dependents: dict[str, list[str]] = defaultdict(list)

    for name in resource_names:
        outgoing = (resources.get(name) or {}).get("outgoing_references") or {}
        for target in outgoing:
            if target in name_set and target != name:
                in_degree[name] += 1
                dependents[target].append(name)

    queue = sorted([name for name in resource_names if in_degree[name] == 0])
    order: list[str] = []
    while queue:
        current = queue.pop(0)
        order.append(current)
        for dependent in sorted(dependents.get(current, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Cycle fallback — append remaining alphabetically
    remaining = [name for name in resource_names if name not in order]
    order.extend(sorted(remaining))
    return order


def _extract_responses(spec: dict, resources_doc: dict) -> dict:
    """Extract components/responses referenced by scoped resource endpoints."""
    import copy

    component_responses = (spec.get("components") or {}).get("responses") or {}
    component_schemas = (spec.get("components") or {}).get("schemas") or {}

    # Collect which component response names are used by scoped endpoints.
    # The endpoints are already dereferenced, so match by description.
    used_names: set[str] = set()
    # Also check the raw spec paths for direct $ref matches
    for path, path_item in (spec.get("paths") or {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "patch", "delete", "head", "options"):
                continue
            for code, resp in (operation.get("responses") or {}).items():
                ref = resp.get("$ref", "")
                if ref.startswith("#/components/responses/"):
                    used_names.add(ref.split("/")[-1])

    # Filter to only responses used by scoped resource endpoints
    scoped_endpoints: set[str] = set()
    for resource in (resources_doc.get("resources") or {}).values():
        scoped_endpoints.update(resource.get("endpoint_keys") or [])

    scoped_response_names: set[str] = set()
    for path, path_item in (spec.get("paths") or {}).items():
        for method, operation in path_item.items():
            key = f"{method.upper()} {path}"
            if key not in scoped_endpoints:
                continue
            for code, resp in (operation.get("responses") or {}).items():
                ref = resp.get("$ref", "")
                if ref.startswith("#/components/responses/"):
                    scoped_response_names.add(ref.split("/")[-1])

    responses: dict[str, Any] = {}
    referenced_schemas: dict[str, Any] = {}

    for name in sorted(scoped_response_names):
        body = component_responses.get(name)
        if body is None:
            continue
        responses[name] = copy.deepcopy(body)
        content = body.get("content") or {}
        for media_type, media in content.items():
            schema = media.get("schema") or {}
            ref = schema.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
                schema_name = ref[len("#/components/schemas/"):]
                if schema_name in component_schemas:
                    referenced_schemas[schema_name] = copy.deepcopy(component_schemas[schema_name])

    return {
        "responses": responses,
        "schemas": referenced_schemas,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the pipeline orchestrator.")
    parser.add_argument("config", type=Path, help="Path to app.yaml")
    parser.add_argument("--stage", choices=_STAGES + ["all"], default="all")
    parser.add_argument("--resource", nargs="+", metavar="NAME", help="Restrict to specific resources")
    parser.add_argument("--dry-run", action="store_true", help="Build prompts without calling LLM")
    parser.add_argument("--configure-model", default="claude-sonnet-4-5", help="Model for alias/PK inference")
    parser.add_argument("--implement-model", default="claude-opus-4-6", help="Model for entity implementation")
    args = parser.parse_args(argv)

    run_pipeline(
        config_path=args.config,
        stage=args.stage,
        dry_run=args.dry_run,
        only_resources=args.resource,
        configure_model=args.configure_model,
        implement_model=args.implement_model,
    )


if __name__ == "__main__":
    main()

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
import subprocess
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
from pipeline.testing.runner import run_test_endpoints

_STAGES = [
    "init",
    "configure",
    "suggest_aliases",
    "extract",
    "implement_responses",
    "implement",
    "register_tests",
    "seed_template",
    "test_endpoints",
]

# Backend repo root, used to locate replicas.yaml when wiring the test stage.
_REPO_ROOT = Path(__file__).parent.parent.parent
_REPLICAS_YAML = _REPO_ROOT / "backend" / "src" / "services" / "replicas.yaml"
_COMPOSE_FILE = _REPO_ROOT / "ops" / "docker-compose.yml"


def run_pipeline(
    config_path: Path,
    stage: str = "all",
    dry_run: bool = False,
    only_resources: list[str] | None = None,
    configure_model: str = "claude-sonnet-4-5",
    implement_model: str = "claude-opus-4-6",
    test_model: str = "claude-opus-4-6",
    test_batch_size: int = 7,
    test_max_iterations: int = 3,
    test_force_retest: bool = False,
    test_timeout: int = 1800,
) -> None:
    if stage == "all":
        stages = _STAGES
    elif stage.startswith("up_to:"):
        target = stage.split(":", 1)[1]
        if target not in _STAGES:
            raise ValueError(f"Unknown up-to stage: {target}")
        stages = _STAGES[: _STAGES.index(target) + 1]
    else:
        stages = [stage]

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

    # --- Stage: Seed Template ---
    # Drops the postgres template schema for this app and re-runs the
    # replica's seed command via ``docker compose exec``. Required after
    # ``implement`` regenerates ``database/schema.py``: the old template
    # schema is shaped against the previous tables, so cloning a runtime
    # environment from it would mismatch the new ORM models. Also bounces
    # the backend container so uvicorn picks up newly-mounted replicas.
    if "seed_template" in stages:
        config = load_config(config_path)
        print(f"\n=== SEED TEMPLATE — drop & reseed {config.app_slug}_base ===")

        if dry_run:
            print(f"  [dry-run] Would drop {config.app_slug}_base, reseed, and restart backend")
        elif not _COMPOSE_FILE.exists():
            print(f"  [skip] docker-compose.yml not found at {_COMPOSE_FILE}")
        else:
            drop_command = [
                "docker", "compose", "-f", str(_COMPOSE_FILE),
                "exec", "-T", "postgres",
                "psql", "-U", "postgres", "-d", "diff_the_universe",
                "-c", f"DROP SCHEMA IF EXISTS {config.app_slug}_base CASCADE;",
            ]
            drop_result = subprocess.run(drop_command, capture_output=True, text=True)
            if drop_result.returncode != 0:
                print(f"  [warn] drop schema failed: {drop_result.stderr.strip()[:300]}")
            else:
                print(f"  Dropped schema {config.app_slug}_base")

            seed_command = [
                "docker", "compose", "-f", str(_COMPOSE_FILE),
                "exec", "-T", "backend",
                "python", "utils/seed_template.py", "--app", config.app_slug,
            ]
            seed_result = subprocess.run(seed_command, capture_output=True, text=True)
            if seed_result.returncode != 0:
                print(f"  [error] seed failed (rc={seed_result.returncode})")
                print(f"    stdout: {seed_result.stdout.strip()[:500]}")
                print(f"    stderr: {seed_result.stderr.strip()[:500]}")
            else:
                tail_lines = [line for line in seed_result.stdout.split("\n") if line.strip()][-6:]
                for line in tail_lines:
                    print(f"    {line}")

            # Touch main.py so uvicorn --reload re-imports REST_REPLICAS and
            # mounts any newly-registered replica routes. Without this, an
            # app added to replicas.yaml during this run stays unmounted.
            touch_command = [
                "docker", "compose", "-f", str(_COMPOSE_FILE),
                "exec", "-T", "backend",
                "touch", "/app/src/platform/api/main.py",
            ]
            subprocess.run(touch_command, capture_output=True, text=True)
            print(f"  Triggered uvicorn reload")

    # --- Stage: Test Endpoints ---
    if "test_endpoints" in stages:
        config = load_config(config_path)
        output_dir = config_path.parent / "pipeline_out"

        print(f"\n=== TEST ENDPOINTS — drive replica via curl, fix bugs in place ({test_model}) ===")
        if test_force_retest:
            print("  [force] retesting endpoints already marked tested=true")

        summary = run_test_endpoints(
            config_path=config_path,
            app_name=config.app_name,
            app_slug=config.app_slug,
            target_dir=config.target_dir,
            output_dir=output_dir,
            replicas_yaml=_REPLICAS_YAML,
            repo_root=_REPO_ROOT,
            model=test_model,
            batch_size=test_batch_size,
            max_iterations=test_max_iterations,
            force=test_force_retest,
            dry_run=dry_run,
            timeout=test_timeout,
            only_subjects=only_resources,
        )
        if summary.get("skipped"):
            print(f"  [skip] {summary.get('reason')}")
        else:
            print(
                f"  Done. Batches: {summary['total_batches']}, "
                f"recorded {summary['endpoints_recorded']}/{summary['endpoints_attempted']}, "
                f"passed {summary['endpoints_passed']}"
            )
            for subject, subject_summary in summary.get("subjects", {}).items():
                print(
                    f"    {subject}: {subject_summary['passed']}/{subject_summary['recorded']} passed "
                    f"across {subject_summary['batches']} batch(es)"
                )

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
    parser.add_argument(
        "--stage",
        choices=_STAGES + ["all"],
        default="all",
        help="Run a single stage (or 'all' for the full pipeline)",
    )
    parser.add_argument(
        "--up-to-stage",
        choices=_STAGES,
        default=None,
        help="Run every stage from the start through this one (inclusive); overrides --stage",
    )
    parser.add_argument("--resource", nargs="+", metavar="NAME", help="Restrict to specific resources")
    parser.add_argument("--dry-run", action="store_true", help="Build prompts without calling LLM")
    parser.add_argument("--configure-model", default="claude-sonnet-4-5", help="Model for alias/PK inference")
    parser.add_argument("--implement-model", default="claude-opus-4-6", help="Model for entity implementation")
    parser.add_argument("--test-model", default="claude-opus-4-6", help="Model for test_endpoints stage")
    parser.add_argument("--test-batch-size", type=int, default=7, help="Endpoints per LLM call in test_endpoints")
    parser.add_argument("--test-max-iterations", type=int, default=3, help="Fix-and-retry budget per endpoint")
    parser.add_argument("--test-timeout", type=int, default=1800, help="Per-batch claude -p timeout in seconds")
    parser.add_argument(
        "--force-retest",
        action="store_true",
        help="Test endpoints already marked tested=true (regression sweep)",
    )
    args = parser.parse_args(argv)

    selected_stage = args.stage
    if args.up_to_stage:
        # Compose a synthetic pseudo-stage marker that run_pipeline expands
        # into the prefix of _STAGES up to and including the named one.
        selected_stage = f"up_to:{args.up_to_stage}"

    run_pipeline(
        config_path=args.config,
        stage=selected_stage,
        dry_run=args.dry_run,
        only_resources=args.resource,
        configure_model=args.configure_model,
        implement_model=args.implement_model,
        test_model=args.test_model,
        test_batch_size=args.test_batch_size,
        test_max_iterations=args.test_max_iterations,
        test_force_retest=args.force_retest,
        test_timeout=args.test_timeout,
    )


if __name__ == "__main__":
    main()

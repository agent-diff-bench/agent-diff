"""End-to-end alias suggestion runner.

Usage::

    # Deterministic only — print raw suggestions for manual review:
    python -m pipeline.run_suggest_aliases app.yaml --raw

    # With LLM review (Claude CLI, default model):
    python -m pipeline.run_suggest_aliases app.yaml

    # With LLM review, specific backend + model:
    python -m pipeline.run_suggest_aliases app.yaml \
        --backend anthropic --model claude-sonnet-4-5

    # Include uncertain verdicts in the output:
    python -m pipeline.run_suggest_aliases app.yaml --include-uncertain

Cache is written to ``<config_dir>/pipeline_cache/alias_review.json``
so re-runs with the same spec + config skip the LLM call.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pipeline.config import load_config
from pipeline.llm import make_llm_call
from pipeline.aliases.review import (
    format_approved_aliases_yaml,
    review_suggestions,
)
from pipeline.aliases.suggest import format_suggestions_yaml, suggest_aliases


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Suggest alias additions for pipeline config.",
    )
    parser.add_argument("config", type=Path, help="Path to app.yaml config file")
    parser.add_argument(
        "--raw", action="store_true",
        help="Print raw suggestions without LLM review",
    )
    parser.add_argument(
        "--backend", default="claude_code", choices=["claude_code", "anthropic"],
        help="LLM backend (default: claude_code)",
    )
    parser.add_argument(
        "--model", default="claude-sonnet-4-5",
        help="Model name (default: claude-sonnet-4-5)",
    )
    parser.add_argument(
        "--include-uncertain", action="store_true",
        help="Include uncertain verdicts (commented out) in the LLM-reviewed output",
    )
    args = parser.parse_args(argv)

    config = load_config(args.config)
    spec_path = config.openapi_path
    print(f"Loading spec: {spec_path}", file=sys.stderr)
    with open(spec_path) as f:
        spec = json.load(f)

    print("Running suggest_aliases...", file=sys.stderr)
    suggestions = suggest_aliases(spec, config)
    total = sum(len(v) for v in suggestions.values())
    print(f"Found {total} candidates across {len(suggestions)} resources.", file=sys.stderr)

    if args.raw:
        print(format_suggestions_yaml(suggestions))
        return

    print(f"Running LLM review (backend={args.backend}, model={args.model})...", file=sys.stderr)
    llm_call = make_llm_call(backend=args.backend, model=args.model)
    cache_path = args.config.parent / "pipeline_cache" / "alias_review.json"
    reviewed = review_suggestions(
        suggestions, spec, config, llm_call, cache_path=cache_path,
    )
    approved = sum(
        1 for entries in reviewed.values()
        for entry in entries if entry.verdict == "variant"
    )
    distinct = sum(
        1 for entries in reviewed.values()
        for entry in entries if entry.verdict == "distinct"
    )
    uncertain = sum(
        1 for entries in reviewed.values()
        for entry in entries if entry.verdict == "uncertain"
    )
    print(
        f"Verdicts: {approved} variant, {distinct} distinct, {uncertain} uncertain.",
        file=sys.stderr,
    )
    print(format_approved_aliases_yaml(reviewed, include_uncertain=args.include_uncertain))


if __name__ == "__main__":
    main()

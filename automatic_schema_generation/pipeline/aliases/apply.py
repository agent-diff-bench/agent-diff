"""Apply LLM-reviewed variant aliases to the pipeline config.

Usage::

    python -m pipeline.apply_aliases app.yaml --dry-run
    python -m pipeline.apply_aliases app.yaml
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from pipeline.config import load_config
from pipeline.aliases.review import review_suggestions
from pipeline.aliases.suggest import suggest_aliases


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Apply reviewed alias suggestions.")
    parser.add_argument("config", type=Path, help="Path to app.yaml")
    parser.add_argument("--cache", type=Path, default=None, help="Override cache path")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    with open(config.openapi_path) as f:
        spec = json.load(f)

    suggestions = suggest_aliases(spec, config)
    if not suggestions:
        print("No suggestions found.", file=sys.stderr)
        return

    cache_path = args.cache or args.config.parent / "pipeline_cache" / "alias_review.json"
    if not cache_path.exists():
        print(f"Cache not found: {cache_path}. Run review first.", file=sys.stderr)
        sys.exit(1)

    def no_llm(prompt: str) -> str:
        raise RuntimeError("Cache miss — run the review step first")

    reviewed = review_suggestions(suggestions, spec, config, no_llm, cache_path=cache_path)

    new_aliases: dict[str, list[str]] = {}
    for resource, entries in reviewed.items():
        existing = config.resources.aliases_by_resource.get(resource, frozenset())
        additions = [entry.suggestion.normalized for entry in entries
                     if entry.verdict == "variant" and entry.suggestion.normalized not in existing]
        if additions:
            new_aliases[resource] = additions

    if not new_aliases:
        print("All variants already in config.", file=sys.stderr)
        return

    total = sum(len(aliases) for aliases in new_aliases.values())
    print(f"Adding {total} aliases across {len(new_aliases)} resources:", file=sys.stderr)
    for resource, aliases in sorted(new_aliases.items()):
        print(f"  {resource}: {', '.join(sorted(aliases))}", file=sys.stderr)

    patched = _patch_config(args.config.read_text(), new_aliases)
    if args.dry_run:
        print(patched)
    else:
        args.config.write_text(patched)
        print(f"\nWrote {args.config}", file=sys.stderr)


def _patch_config(text: str, new_aliases: dict[str, list[str]]) -> str:
    """Insert new aliases into raw YAML text, preserving comments.

    Detects indentation dynamically so it works with both hand-written
    configs (6-space alias entries) and yaml.safe_dump output (4-space).
    """
    # Detect the indent used for resource names under "resources:"
    resource_indent = ""
    for line in text.split("\n"):
        if re.match(r"^resources:\s*$", line):
            continue
        resource_match = re.match(r"^(\s+)(\w+):\s*$", line)
        if resource_match and resource_match.group(2) not in ("aliases", "primary_key", "self_id_fields"):
            resource_indent = resource_match.group(1)
            break

    lines = text.split("\n")
    insert_after: dict[str, tuple[int, str]] = {}
    current_resource: str | None = None
    in_aliases = False

    for index, line in enumerate(lines):
        resource_match = re.match(rf"^{resource_indent}(\w+):\s*$", line)
        if resource_match and resource_match.group(1) not in ("aliases", "primary_key", "self_id_fields"):
            current_resource = resource_match.group(1) if resource_match.group(1) in new_aliases else None
            in_aliases = False
            continue
        if current_resource is None:
            continue
        if re.match(r"^\s+aliases:\s*$", line):
            in_aliases = True
            continue
        if in_aliases and re.match(r"^(\s+)- ", line):
            alias_indent = re.match(r"^(\s*)", line).group(1)
            insert_after[current_resource] = (index, alias_indent)
            continue
        if in_aliases and (re.match(r"^\s+#", line) or not line.strip()):
            continue
        if in_aliases:
            in_aliases = False

    for resource in sorted(insert_after, key=lambda r: insert_after[r][0], reverse=True):
        idx, indent = insert_after[resource]
        new_lines = [f"{indent}- {alias}" for alias in sorted(new_aliases[resource])]
        lines[idx + 1 : idx + 1] = new_lines

    return "\n".join(lines)


if __name__ == "__main__":
    main()

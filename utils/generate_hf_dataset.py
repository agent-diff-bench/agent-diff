#!/usr/bin/env python3
"""
Generate a HuggingFace-compatible dataset from the agent-diff test suites.

Combines all 4 service benchmarks (Linear, Slack, Box, Calendar) into a single
dataset with the schema expected by the prime-environments verifiers framework.

Output: a Parquet file (and optionally pushes to HuggingFace Hub).

Usage:
    python utils/generate_hf_dataset.py                          # save locally
    python utils/generate_hf_dataset.py --push hubertmarek/agent-diff-bench  # push to HF
"""

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent

BENCHMARKS: list[tuple[str, Path]] = [
    ("linear", REPO_ROOT / "examples/linear/testsuites/linear_bench.json"),
    ("slack", REPO_ROOT / "examples/slack/testsuites/slack_bench_v2.json"),
    ("box", REPO_ROOT / "examples/box/testsuites/box_bench.json"),
    ("calendar", REPO_ROOT / "examples/calendar/testsuites/calendar_bench.json"),
]

# Metadata keys to promote to top-level columns (must exist in test.metadata).
PROMOTED_METADATA_KEYS = [
    "task_horizon",
    "operation_type",
    "entity_scope",
    "information_availability",
    "prompt_ambiguity",
]

# Keys to include in the info column (runtime metadata for the environment).
INFO_KEYS = [
    "seed_template",
    "impersonate_user_id",
    "eval_type",
    "tools_required",
]


def build_answer(test: dict[str, Any], ignore_fields: dict[str, Any]) -> str:
    """Build the JSON-encoded answer string from a test's assertions.

    The answer is the full expectedOutput spec sent to the AgentDiff evaluation
    engine. It must include both assertions and ignore_fields at the top level,
    since the assertion engine reads ignore_fields from the spec root to know
    which fields to exclude when computing diffs.
    """
    spec: dict[str, Any] = {"assertions": test["assertions"]}
    if ignore_fields:
        spec["ignore_fields"] = ignore_fields
    return json.dumps(spec, separators=(",", ":"))


def build_info(test: dict[str, Any], service: str = "") -> dict[str, Any]:
    """Build the info dict containing runtime metadata for the environment."""
    metadata = test.get("metadata", {})
    return {
        "service": service,
        "seed_template": test.get("seed_template", ""),
        "impersonate_user_id": test.get("impersonate_user_id", ""),
        "eval_type": test.get("type", "actionEval"),
        "tools_required": metadata.get("tools_required", []),
    }


def load_suite(path: Path) -> dict[str, Any]:
    """Load and validate a test suite JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "tests" not in data:
        raise ValueError(f"No 'tests' key in {path}")
    return data


def generate_rows() -> list[dict[str, Any]]:
    """Generate all dataset rows from the 4 service benchmarks."""
    rows: list[dict[str, Any]] = []
    global_id = 0

    for service, suite_path in BENCHMARKS:
        if not suite_path.exists():
            print(f"WARNING: {suite_path} not found, skipping {service}")
            continue

        suite = load_suite(suite_path)
        ignore_fields = suite.get("ignore_fields", {})
        tests = suite["tests"]

        for test in tests:
            metadata = test.get("metadata", {})

            row = {
                # Core columns (required by verifiers)
                "question": test["prompt"],
                "answer": build_answer(test, ignore_fields),
                # Identity
                "test_id": f"{service}_{global_id}",
                "test_name": test.get("name", ""),
                "service": service,
                # Promoted taxonomy metadata
                "task_horizon": metadata.get("task_horizon", 0),
                "operation_type": metadata.get("operation_type", ""),
                "entity_scope": metadata.get("entity_scope", ""),
                "information_availability": metadata.get(
                    "information_availability", ""
                ),
                "prompt_ambiguity": metadata.get("prompt_ambiguity", ""),
                # Runtime metadata (JSON blob)
                "info": build_info(test, service=service),
            }
            rows.append(row)
            global_id += 1

    return rows


def print_summary(rows: list[dict[str, Any]]) -> None:
    """Print a summary of the generated dataset."""
    from collections import Counter

    services = Counter(r["service"] for r in rows)
    print(f"\nGenerated {len(rows)} rows:")
    for svc, count in sorted(services.items()):
        print(f"  {svc}: {count} tests")

    # ID range check
    ids = [r["test_id"] for r in rows]
    print(f"\nTest IDs: {ids[0]} ... {ids[-1]}")
    assert len(ids) == len(set(ids)), "Duplicate test_id detected!"
    print("All test_ids are unique.")

    # Column overview
    print(f"\nColumns: {list(rows[0].keys())}")


def split_rows(
    rows: list[dict[str, Any]], test_fraction: float = 0.2, seed: int = 42
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Stratified 80/20 split by service. Returns (train, test)."""
    import random

    rng = random.Random(seed)
    by_service: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_service.setdefault(row["service"], []).append(row)

    train, test = [], []
    for service, svc_rows in sorted(by_service.items()):
        shuffled = list(svc_rows)
        rng.shuffle(shuffled)
        n_test = max(1, round(len(shuffled) * test_fraction))
        test.extend(shuffled[:n_test])
        train.extend(shuffled[n_test:])

    print(f"\nSplit: {len(train)} train, {len(test)} test")
    for service in sorted(by_service):
        n_train = sum(1 for r in train if r["service"] == service)
        n_test = sum(1 for r in test if r["service"] == service)
        print(f"  {service}: {n_train} train, {n_test} test")

    return train, test


def _prepare_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert info dicts to JSON strings for storage."""
    for row in rows:
        if isinstance(row["info"], dict):
            row["info"] = json.dumps(row["info"], separators=(",", ":"))
    return rows


def save_dataset(
    train_rows: list[dict[str, Any]],
    test_rows: list[dict[str, Any]],
    output_dir: Path,
) -> None:
    """Save train/test splits as Parquet."""
    from datasets import Dataset

    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, split_rows in [("train", train_rows), ("test", test_rows)]:
        ds = Dataset.from_list(_prepare_rows(split_rows))
        parquet_path = output_dir / f"{split_name}.parquet"
        ds.to_parquet(str(parquet_path))
        print(f"Saved {split_name} ({len(split_rows)} rows) to {parquet_path}")

        jsonl_path = output_dir / f"{split_name}.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for row in split_rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")


def push_to_hub(
    train_rows: list[dict[str, Any]],
    test_rows: list[dict[str, Any]],
    repo_id: str,
) -> None:
    """Push train/test splits to HuggingFace Hub."""
    from datasets import Dataset

    for split_name, split_rows in [("train", train_rows), ("test", test_rows)]:
        ds = Dataset.from_list(_prepare_rows(list(split_rows)))
        ds.push_to_hub(repo_id, split=split_name)
        print(f"Pushed {split_name} ({len(split_rows)} rows) to {repo_id}")

    print(f"\nDataset: https://huggingface.co/datasets/{repo_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate HuggingFace dataset from agent-diff test suites"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "datasets" / "agent-diff-bench",
        help="Output directory for local files (default: datasets/agent-diff-bench/)",
    )
    parser.add_argument(
        "--push",
        type=str,
        default=None,
        metavar="REPO_ID",
        help="Push to HuggingFace Hub (e.g. hubertmarek/agent-diff-bench)",
    )
    parser.add_argument(
        "--test-fraction",
        type=float,
        default=0.2,
        help="Fraction of data for test split (default: 0.2)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for split (default: 42)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate and summarize without saving",
    )
    args = parser.parse_args()

    rows = generate_rows()
    print_summary(rows)
    train_rows, test_rows = split_rows(rows, args.test_fraction, args.seed)

    if args.dry_run:
        sample = dict(train_rows[0])
        sample["question"] = sample["question"][:100] + "..."
        sample["answer"] = sample["answer"][:100] + "..."
        print(f"\nSample row:\n{json.dumps(sample, indent=2)}")
        return

    save_dataset(train_rows, test_rows, args.output_dir)

    if args.push:
        # Re-generate (save_dataset mutates info to string)
        rows = generate_rows()
        train_rows, test_rows = split_rows(rows, args.test_fraction, args.seed)
        push_to_hub(train_rows, test_rows, args.push)


if __name__ == "__main__":
    main()

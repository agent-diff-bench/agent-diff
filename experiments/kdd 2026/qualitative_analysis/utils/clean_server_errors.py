"""
Clean merged results by removing runs affected by server errors.
"""

import json
import os
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm
from typing import Optional

# Import the unified error classifier
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unified_error_classifier import classify_response


def has_server_error(run: dict) -> bool:
    """
    Check if a run contains any server errors.

    Args:
        run: Raw run dict from merged results

    Returns:
        True if the run has at least one server error, False otherwise
    """
    service = run.get('service', '')
    trace = run.get('trace', {})
    steps = trace.get('steps', []) if isinstance(trace, dict) else []

    for step in steps:
        observation = step.get('observation', {})

        # Get stdout from observation
        if isinstance(observation, dict):
            stdout = observation.get('stdout', '')
        else:
            stdout = str(observation) if observation else ''

        # Classify the response
        try:
            classification = classify_response(stdout, service)
            if classification.get("error_type") == "server_error":
                return True
        except ValueError:
            # Unknown service - skip
            pass

    return False


def clean_merged_results(
    merged_results_path: str,
    output_folder: Optional[str] = None,
    output_filename: Optional[str] = None,
    verbose: bool = True
) -> tuple[list, str]:
    """
    Clean merged results by removing runs with server errors.

    Args:
        merged_results_path: Path to the merged results JSON file
        output_folder: Folder to save cleaned results. Defaults to same folder as input.
        output_filename: Custom output filename. Defaults to 'cleaned_<original_name>.json'
        verbose: Whether to print progress and statistics

    Returns:
        Tuple of (cleaned_runs list, output_filepath)
    """
    # Load merged results
    with open(merged_results_path, 'r') as f:
        runs = json.load(f)

    if verbose:
        print(f"Loaded {len(runs)} runs from {merged_results_path}")

    # Filter out runs with server errors
    cleaned_runs = []
    removed_count = 0

    for run in tqdm(runs, desc="Checking for server errors", disable=not verbose):
        if has_server_error(run):
            removed_count += 1
        else:
            cleaned_runs.append(run)

    if verbose:
        print(f"\nRemoved {removed_count} runs with server errors ({100*removed_count/len(runs):.1f}%)")
        print(f"Cleaned runs: {len(cleaned_runs)}")

        # Show breakdown by service
        print("\n--- Breakdown by Service ---")
        service_counts = defaultdict(lambda: {"original": 0, "cleaned": 0})

        for run in runs:
            svc = run.get("service", "unknown")
            service_counts[svc]["original"] += 1

        for run in cleaned_runs:
            svc = run.get("service", "unknown")
            service_counts[svc]["cleaned"] += 1

        for svc, counts in sorted(service_counts.items()):
            removed = counts["original"] - counts["cleaned"]
            pct_removed = 100 * removed / counts["original"] if counts["original"] > 0 else 0
            print(f"  {svc.upper()}: {counts['original']} -> {counts['cleaned']} (removed {removed}, {pct_removed:.1f}%)")

    # Determine output path
    if output_folder is None:
        output_folder = os.path.dirname(merged_results_path)

    if output_filename is None:
        base_name = os.path.basename(merged_results_path)
        output_filename = f"cleaned_{base_name}"

    output_filepath = os.path.join(output_folder, output_filename)

    # Save cleaned results
    with open(output_filepath, 'w') as f:
        json.dump(cleaned_runs, f, indent=2)

    if verbose:
        print(f"\nSaved cleaned dataset to: {output_filepath}")
        print(f"Original size: {len(json.dumps(runs)) / 1024 / 1024:.2f} MB")
        print(f"Cleaned size: {len(json.dumps(cleaned_runs)) / 1024 / 1024:.2f} MB")

    return cleaned_runs, output_filepath


def get_or_create_cleaned_results(
    merged_results_path: str,
    output_folder: Optional[str] = None,
    output_filename: Optional[str] = None,
    force_recreate: bool = False
) -> tuple[list, str]:
    """
    Get cleaned results from cache or create them if they don't exist.

    Args:
        merged_results_path: Path to the merged results JSON file
        output_folder: Folder to save/load cleaned results
        output_filename: Custom output filename
        force_recreate: If True, recreate even if cached file exists

    Returns:
        Tuple of (cleaned_runs list, output_filepath)
    """
    # Determine expected output path
    if output_folder is None:
        output_folder = os.path.dirname(merged_results_path)

    if output_filename is None:
        base_name = os.path.basename(merged_results_path)
        output_filename = f"cleaned_{base_name}"

    output_filepath = os.path.join(output_folder, output_filename)

    # Check if cached file exists
    if not force_recreate and os.path.exists(output_filepath):
        print(f"Loading existing cleaned results from: {output_filepath}")
        with open(output_filepath, 'r') as f:
            cleaned_runs = json.load(f)
        print(f"Loaded {len(cleaned_runs)} cleaned runs")
        return cleaned_runs, output_filepath

    # Create cleaned results
    return clean_merged_results(
        merged_results_path=merged_results_path,
        output_folder=output_folder,
        output_filename=output_filename
    )


if __name__ == "__main__":
    # Example usage
    MERGED_RESULTS_FILE = "merged_results_20260204_221118.json"

    cleaned_runs, output_path = get_or_create_cleaned_results(MERGED_RESULTS_FILE)
    print(f"\nDone! {len(cleaned_runs)} runs saved to {output_path}")

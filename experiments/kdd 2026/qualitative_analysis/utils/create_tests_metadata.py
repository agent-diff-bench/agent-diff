"""
Create tests metadata from test suites and merged results.

This module provides a function to create a metadata file that maps runtime_test_ids
to test information, avoiding the need to recompute this mapping repeatedly.
"""

import json
import os
import glob
from collections import defaultdict
from typing import Dict, List, Optional, Any


def load_test_suites(test_suites_folder: str) -> List[Dict[str, Any]]:
    """
    Load all test suite JSON files from a folder.

    Args:
        test_suites_folder: Path to folder containing test suite JSON files

    Returns:
        List of test suite dictionaries
    """
    test_suite_files = glob.glob(os.path.join(test_suites_folder, "*.json"))

    test_suites = []
    for filepath in test_suite_files:
        with open(filepath, 'r') as f:
            test_suite = json.load(f)
            test_suites.append(test_suite)
        print(f"Loaded: {os.path.basename(filepath)}")

    print(f"\nTotal test suites loaded: {len(test_suites)}")
    return test_suites


def build_test_lookup(test_suites: List[Dict[str, Any]]) -> Dict[tuple, Dict[str, Any]]:
    """
    Build a lookup dictionary from test suites.

    Maps (test_suite_name, test_name, prompt) -> test info

    Args:
        test_suites: List of test suite dictionaries

    Returns:
        Dictionary mapping test keys to test data
    """
    test_lookup = defaultdict(dict)

    for test_suite in test_suites:
        test_suite_name = test_suite["name"]
        # Normalize "Slack Bench v2 (Combined)" to "Slack Bench v2"
        test_suite_name = "Slack Bench v2" if test_suite_name == "Slack Bench v2 (Combined)" else test_suite_name

        for test in test_suite["tests"]:
            key = (test_suite_name, test["name"], test["prompt"])
            if key in test_lookup and test_lookup[key]:
                print(f"WARNING: Duplicate test '{test['name']}' with prompt '{test['prompt'][:50]}...' from '{test_suite_name}'")
            test_lookup[key]["test_suite_name"] = test_suite_name
            test_lookup[key]["test_suite_test_id"] = test["id"]

    print(f"Built lookup for {len(test_lookup)} tests")
    return test_lookup


def create_tests_metadata(
    merged_results_path: str,
    test_suites: Optional[List[Dict[str, Any]]] = None,
    test_suites_folder: Optional[str] = None,
    output_folder: str = "tests_metadata",
    force: bool = False
) -> Optional[str]:
    """
    Create a metadata file mapping runtime_test_ids to test information.

    Args:
        merged_results_path: Path to the merged_results JSON file
        test_suites: List of test suite dictionaries (optional if test_suites_folder provided)
        test_suites_folder: Path to folder containing test suite JSON files
                           (optional if test_suites provided)
        output_folder: Folder to save metadata file (default: "tests_metadata")
        force: If True, recreate metadata even if it already exists

    Returns:
        Path to the created metadata file, or None if already exists and force=False

    Raises:
        ValueError: If neither test_suites nor test_suites_folder is provided
    """
    # Determine output filename based on input filename
    input_filename = os.path.basename(merged_results_path)
    base_name = input_filename.rsplit('.json', 1)[0]
    output_filename = f"{base_name}_tests_metadata.json"

    # Create output folder if needed
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)

    # Check if metadata already exists
    if os.path.exists(output_path) and not force:
        print(f"Tests metadata already exists: {output_path}")
        print("Use force=True to regenerate.")
        return None

    # Load test suites if not provided
    if test_suites is None:
        if test_suites_folder is None:
            raise ValueError("Either test_suites or test_suites_folder must be provided")
        test_suites = load_test_suites(test_suites_folder)

    # Build test lookup
    test_lookup = build_test_lookup(test_suites)

    # Load merged results
    print(f"\nLoading merged results from: {merged_results_path}")
    with open(merged_results_path, 'r') as f:
        runs = json.load(f)
    print(f"Loaded {len(runs)} runs")

    # Create metadata mapping (runtime_test_id -> test info)
    metadata = {}
    missing_count = 0

    for run in runs:
        runtime_test_id = run.get("test_id")
        if not runtime_test_id:
            continue

        # Skip if already processed
        if runtime_test_id in metadata:
            continue

        test_suite_name = run.get("test_suite_name", "")
        # Normalize test suite name
        test_suite_name = "Slack Bench v2" if test_suite_name == "Slack Bench v2 (Combined)" else test_suite_name

        test_name = run.get("test_name", "")
        prompt = run.get("prompt", "")

        # Look up test info
        key = (test_suite_name, test_name, prompt)
        test_info = test_lookup.get(key, {})

        if not test_info:
            missing_count += 1
            if missing_count <= 5:
                print(f"WARNING: No test info found for test {runtime_test_id}: {test_suite_name} / {test_name[:30]}...")

        metadata[runtime_test_id] = {
            "test_suite_name": test_info.get("test_suite_name", test_suite_name),
            "test_suite_test_id": test_info.get("test_suite_test_id")
        }

    if missing_count > 5:
        print(f"... and {missing_count - 5} more tests with missing test info")

    # Save metadata
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved metadata for {len(metadata)} tests to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")

    return output_path


def load_tests_metadata(merged_results_path: str, output_folder: str = "tests_metadata") -> Optional[Dict[str, Dict]]:
    """
    Load existing tests metadata for a merged_results file.

    Args:
        merged_results_path: Path to the merged_results JSON file
        output_folder: Folder where metadata files are stored

    Returns:
        Metadata dictionary or None if not found
    """
    input_filename = os.path.basename(merged_results_path)
    base_name = input_filename.rsplit('.json', 1)[0]
    output_filename = f"{base_name}_tests_metadata.json"
    metadata_path = os.path.join(output_folder, output_filename)

    if not os.path.exists(metadata_path):
        return None

    with open(metadata_path, 'r') as f:
        return json.load(f)


def get_or_create_tests_metadata(
    merged_results_path: str,
    test_suites_folder: str = "test_suites",
    output_folder: str = "tests_metadata"
) -> Dict[str, Dict]:
    """
    Get existing tests metadata or create it if it doesn't exist.

    This is the main entry point for getting test metadata.

    Args:
        merged_results_path: Path to the merged_results JSON file
        test_suites_folder: Path to folder containing test suite JSON files
        output_folder: Folder to save/load metadata files

    Returns:
        Metadata dictionary mapping runtime_test_id to test information
    """
    # Try to load existing metadata
    metadata = load_tests_metadata(merged_results_path, output_folder)
    if metadata is not None:
        print(f"Loaded existing tests metadata with {len(metadata)} tests")
        return metadata

    # Create new metadata
    create_tests_metadata(
        merged_results_path=merged_results_path,
        test_suites_folder=test_suites_folder,
        output_folder=output_folder
    )

    # Load and return the newly created metadata (must exist after create)
    result = load_tests_metadata(merged_results_path, output_folder)
    assert result is not None, "Metadata file should exist after create_tests_metadata"
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create tests metadata from merged results")
    parser.add_argument("merged_results", help="Path to merged_results JSON file")
    parser.add_argument("--test-suites", default="test_suites", help="Path to test suites folder")
    parser.add_argument("--output", default="tests_metadata", help="Output folder for metadata")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if exists")

    args = parser.parse_args()

    create_tests_metadata(
        merged_results_path=args.merged_results,
        test_suites_folder=args.test_suites,
        output_folder=args.output,
        force=args.force
    )

"""Bayesian bootstrap utilities for statistical inference."""

import json
import os
import uuid
from datetime import datetime
from typing import Callable

import numpy as np


def bayes_bootstrap_single(
    runs: list[dict],
    statistic: Callable,
    n_draws: int = 10000,
    seed: int = 0,
    compare_to: float = 0.0
) -> dict | None:
    """
    Bayesian bootstrap for a single-group statistic.

    Args:
        runs: List of observation dicts
        statistic: Callable that takes (runs, weights) -> float
        n_draws: Number of bootstrap samples
        seed: Random seed
        compare_to: Threshold for probability comparison (default 0)

    Returns:
        dict with mean, median, lo, hi (95% CI), p_lt (P < compare_to), p_gt (P > compare_to),
        or None when runs is empty.
    """
    rng = np.random.default_rng(seed)
    n = len(runs)

    if n == 0:
        return None

    # Generate Dirichlet weights
    W = rng.dirichlet(np.ones(n), size=n_draws)

    # Compute statistic for each bootstrap sample
    stats = np.array([statistic(runs, w) for w in W])

    lo, hi = np.percentile(stats, [2.5, 97.5])

    return {
        'mean': float(stats.mean()),
        'median': float(np.median(stats)),
        'lo': float(lo),
        'hi': float(hi),
        'p_lt': float((stats < compare_to).mean()),
        'p_gt': float((stats > compare_to).mean()),
        'compare_to': compare_to
    }


def bayes_bootstrap_delta(
    group_a: list[dict],
    group_b: list[dict],
    statistic: Callable,
    n_draws: int = 10000,
    seed: int = 0
) -> dict | None:
    """
    Bayesian bootstrap for Δ = statistic(group_a) - statistic(group_b).

    Uses Dirichlet reweighting to generate a posterior distribution over the
    difference between two groups, allowing uncertainty quantification.

    Args:
        group_a: List of observation dicts for condition A
        group_b: List of observation dicts for condition B
        statistic: Callable that takes (observations: list[dict], weights: np.ndarray) -> float
                   The weights array sums to 1 and has same length as observations.
        n_draws: Number of bootstrap samples
        seed: Random seed for reproducibility

    Returns:
        dict with keys:
            - mean: Expected value of Δ (point estimate)
            - median: Median of Δ (robust point estimate)
            - lo: 2.5th percentile of Δ (lower bound of 95% CI)
            - hi: 97.5th percentile of Δ (upper bound of 95% CI)
            - p_gt_0: P(Δ > 0), probability that group A > group B
            - p_lt_0: P(Δ < 0), probability that group B > group A

    Example statistic functions:
        # Weighted mean of 'score' field
        def weighted_mean_score(obs, weights):
            scores = np.array([o['score'] for o in obs])
            return np.sum(weights * scores)

        # Weighted success rate (score == 100)
        def weighted_success_rate(obs, weights):
            successes = np.array([o['score'] == 100 for o in obs])
            return np.sum(weights * successes)
    """
    rng = np.random.default_rng(seed)

    n_a = len(group_a)
    n_b = len(group_b)

    if n_a == 0 or n_b == 0:
        return None

    # Generate Dirichlet weights for each group
    W_a = rng.dirichlet(np.ones(n_a), size=n_draws)  # Shape: (n_draws, n_a)
    W_b = rng.dirichlet(np.ones(n_b), size=n_draws)  # Shape: (n_draws, n_b)

    # Compute statistic for each bootstrap sample
    stats_a = np.array([statistic(group_a, w) for w in W_a])
    stats_b = np.array([statistic(group_b, w) for w in W_b])

    delta = stats_a - stats_b

    lo, hi = np.percentile(delta, [2.5, 97.5])
    return {
        'mean': float(delta.mean()),
        'median': float(np.median(delta)),
        'lo': float(lo),
        'hi': float(hi),
        'p_gt_0': float((delta > 0).mean()),
        'p_lt_0': float((delta < 0).mean())
    }


def bayes_bootstrap_delta_clustered(
    group_a: list[dict],
    group_b: list[dict],
    statistic: Callable,
    cluster_key: str = "test_id",
    n_draws: int = 10000,
    seed: int = 0
) -> dict | None:
    """
    Bayesian bootstrap for Δ = statistic(group_a) - statistic(group_b) with test-level clustering.

    Unlike bayes_bootstrap_delta, this function assigns the SAME weight to observations
    with the same cluster_key value across both groups. This is appropriate for paired
    comparisons where the same test should have equal importance in both conditions.

    Only observations with cluster_key values present in BOTH groups are included.

    Args:
        group_a: List of observation dicts for condition A
        group_b: List of observation dicts for condition B
        statistic: Callable that takes (observations: list[dict], weights: np.ndarray) -> float
                   The weights array sums to 1 and has same length as observations.
        cluster_key: Field name to cluster on (e.g., "test_id"). Same cluster value
                     gets the same weight in both groups.
        n_draws: Number of bootstrap samples
        seed: Random seed for reproducibility

    Returns:
        dict with keys:
            - mean: Expected value of Δ (point estimate)
            - median: Median of Δ (robust point estimate)
            - lo: 2.5th percentile of Δ (lower bound of 95% CI)
            - hi: 97.5th percentile of Δ (upper bound of 95% CI)
            - p_gt_0: P(Δ > 0), probability that group A > group B
            - p_lt_0: P(Δ < 0), probability that group B > group A
            - n_clusters: Number of shared clusters used in comparison
            - n_a: Number of observations in group_a after filtering
            - n_b: Number of observations in group_b after filtering
        Returns None if no shared clusters exist.
    """
    rng = np.random.default_rng(seed)

    # Extract cluster values from both groups
    clusters_a = set(obs[cluster_key] for obs in group_a)
    clusters_b = set(obs[cluster_key] for obs in group_b)

    # Find shared clusters (must exist in both groups for paired comparison)
    shared_clusters = clusters_a & clusters_b

    if len(shared_clusters) == 0:
        return None

    # Create ordered list of shared clusters and mapping to index
    shared_clusters_list = sorted(shared_clusters)
    cluster_to_idx = {c: i for i, c in enumerate(shared_clusters_list)}
    n_clusters = len(shared_clusters_list)

    # Filter groups to only include observations with shared clusters
    group_a_filtered = [obs for obs in group_a if obs[cluster_key] in shared_clusters]
    group_b_filtered = [obs for obs in group_b if obs[cluster_key] in shared_clusters]

    n_a = len(group_a_filtered)
    n_b = len(group_b_filtered)

    if n_a == 0 or n_b == 0:
        return None

    # Count observations per shared cluster in each group
    cluster_sizes_a = np.zeros(n_clusters)
    for obs in group_a_filtered:
        cluster_sizes_a[cluster_to_idx[obs[cluster_key]]] += 1

    cluster_sizes_b = np.zeros(n_clusters)
    for obs in group_b_filtered:
        cluster_sizes_b[cluster_to_idx[obs[cluster_key]]] += 1

    # Generate ONE set of Dirichlet weights per shared cluster
    # Shape: (n_draws, n_clusters)
    W_clusters = rng.dirichlet(np.ones(n_clusters), size=n_draws)

    # Map cluster weights to observations and divide by within-group cluster size.
    # This preserves paired cluster weights across groups even when cluster sizes differ.
    idx_a = np.array([cluster_to_idx[obs[cluster_key]] for obs in group_a_filtered])
    idx_b = np.array([cluster_to_idx[obs[cluster_key]] for obs in group_b_filtered])
    W_a = W_clusters[:, idx_a] / cluster_sizes_a[idx_a]
    W_b = W_clusters[:, idx_b] / cluster_sizes_b[idx_b]

    # Re-normalize for numerical stability.
    W_a = W_a / W_a.sum(axis=1, keepdims=True)
    W_b = W_b / W_b.sum(axis=1, keepdims=True)

    # Compute statistic for each bootstrap sample
    stats_a = np.array([statistic(group_a_filtered, w) for w in W_a])
    stats_b = np.array([statistic(group_b_filtered, w) for w in W_b])

    delta = stats_a - stats_b

    lo, hi = np.percentile(delta, [2.5, 97.5])
    return {
        'mean': float(delta.mean()),
        'median': float(np.median(delta)),
        'lo': float(lo),
        'hi': float(hi),
        'p_gt_0': float((delta > 0).mean()),
        'p_lt_0': float((delta < 0).mean()),
        'n_clusters': n_clusters,
        'n_a': n_a,
        'n_b': n_b
    }


def bayes_bootstrap_delta_internal_clustering(
    group_a: list[dict],
    group_b: list[dict],
    statistic: Callable,
    cluster_key: str = "test_id",
    n_draws: int = 10000,
    seed: int = 0
) -> dict | None:
    """
    Bayesian bootstrap delta with internal clustering (no shared clusters required).

    Each group is clustered independently by cluster_key. Observations within a cluster
    share the cluster's weight (divided by cluster size), so each unique cluster
    contributes equally regardless of how many observations it has.

    Example:
        Cluster A has 3 obs (values 1,2,3), Cluster B has 1 obs (value 10)
        Dirichlet weights: [0.6, 0.4]

        Wrong approach: assign 0.6 to each of A's obs -> A gets 3x weight
        Correct approach: assign 0.6/3=0.2 to each of A's obs -> equal cluster weight

        Result: 1*0.2 + 2*0.2 + 3*0.2 + 10*0.4 = 5.2
        (equivalent to: mean(A)*0.6 + mean(B)*0.4 = 2*0.6 + 10*0.4 = 5.2)
    """
    rng = np.random.default_rng(seed)

    # Get clusters for each group
    clusters_a = sorted(set(obs[cluster_key] for obs in group_a))
    clusters_b = sorted(set(obs[cluster_key] for obs in group_b))

    if not clusters_a or not clusters_b:
        return None

    n_clusters_a = len(clusters_a)
    n_clusters_b = len(clusters_b)

    # Create cluster index mappings
    cluster_to_idx_a = {c: i for i, c in enumerate(clusters_a)}
    cluster_to_idx_b = {c: i for i, c in enumerate(clusters_b)}

    # Count observations per cluster
    cluster_sizes_a = np.zeros(n_clusters_a)
    for obs in group_a:
        cluster_sizes_a[cluster_to_idx_a[obs[cluster_key]]] += 1

    cluster_sizes_b = np.zeros(n_clusters_b)
    for obs in group_b:
        cluster_sizes_b[cluster_to_idx_b[obs[cluster_key]]] += 1

    # Map observations to their cluster indices
    idx_a = np.array([cluster_to_idx_a[obs[cluster_key]] for obs in group_a])
    idx_b = np.array([cluster_to_idx_b[obs[cluster_key]] for obs in group_b])

    # Generate independent Dirichlet weights for each group's clusters
    W_clusters_a = rng.dirichlet(np.ones(n_clusters_a), size=n_draws)
    W_clusters_b = rng.dirichlet(np.ones(n_clusters_b), size=n_draws)

    # Map cluster weights to observations, DIVIDED BY CLUSTER SIZE
    # This ensures each cluster contributes equally regardless of # observations
    W_a = W_clusters_a[:, idx_a] / cluster_sizes_a[idx_a]
    W_b = W_clusters_b[:, idx_b] / cluster_sizes_b[idx_b]

    # Normalize weights within each group to sum to 1
    W_a = W_a / W_a.sum(axis=1, keepdims=True)
    W_b = W_b / W_b.sum(axis=1, keepdims=True)

    # Compute statistics
    stats_a = np.array([statistic(group_a, w) for w in W_a])
    stats_b = np.array([statistic(group_b, w) for w in W_b])
    delta = stats_a - stats_b

    lo, hi = np.percentile(delta, [2.5, 97.5])
    return {
        'mean': float(delta.mean()),
        'median': float(np.median(delta)),
        'lo': float(lo),
        'hi': float(hi),
        'p_gt_0': float((delta > 0).mean()),
        'p_lt_0': float((delta < 0).mean()),
        'n_clusters_a': n_clusters_a,
        'n_clusters_b': n_clusters_b,
        'n_a': len(group_a),
        'n_b': len(group_b)
    }


def bayes_bootstrap_delta_paired_clustered(
    group_a: list[dict],
    group_b: list[dict],
    statistic: Callable,
    cluster_key: str = "test_id",
    n_draws: int = 10000,
    seed: int = 0
) -> dict | None:
    """
    Bayesian bootstrap for paired comparison with proper cluster weighting.

    This is a hybrid of delta_clustered and internal_clustering:
    - Shared clusters get the SAME Dirichlet weight in both groups (paired design)
    - Within each group, observations in the same cluster share weight equally
      (divided by cluster size, so each cluster contributes equally)

    This is appropriate when:
    - Both groups share the same experimental units (e.g., same test cases)
    - You want to control for unit-level confounds (e.g., task difficulty)
    - Each unit has multiple observations per group (e.g., multiple models)

    Statistically, this computes a weighted average of paired differences:
        Δ = Σ_c w_c · (mean_A(c) - mean_B(c))
    where w_c ~ Dirichlet(1,...,1) and mean_A(c) is the average within cluster c in group A.

    Args:
        group_a: List of observation dicts for condition A
        group_b: List of observation dicts for condition B
        statistic: Callable that takes (observations, weights) -> float
        cluster_key: Field name to cluster on (e.g., "test_id" or composite key)
        n_draws: Number of bootstrap samples
        seed: Random seed for reproducibility

    Returns:
        dict with mean, median, 95% CI, directional probabilities, and counts
        Returns None if no shared clusters exist.
    """
    rng = np.random.default_rng(seed)

    # Find shared clusters
    clusters_a = set(obs[cluster_key] for obs in group_a)
    clusters_b = set(obs[cluster_key] for obs in group_b)
    shared_clusters = sorted(clusters_a & clusters_b)

    if not shared_clusters:
        return None

    n_clusters = len(shared_clusters)
    cluster_to_idx = {c: i for i, c in enumerate(shared_clusters)}

    # Filter to shared clusters only
    group_a_filtered = [obs for obs in group_a if obs[cluster_key] in shared_clusters]
    group_b_filtered = [obs for obs in group_b if obs[cluster_key] in shared_clusters]

    n_a = len(group_a_filtered)
    n_b = len(group_b_filtered)

    if n_a == 0 or n_b == 0:
        return None

    # Count observations per cluster in each group
    cluster_sizes_a = np.zeros(n_clusters)
    for obs in group_a_filtered:
        cluster_sizes_a[cluster_to_idx[obs[cluster_key]]] += 1

    cluster_sizes_b = np.zeros(n_clusters)
    for obs in group_b_filtered:
        cluster_sizes_b[cluster_to_idx[obs[cluster_key]]] += 1

    # Map observations to cluster indices
    idx_a = np.array([cluster_to_idx[obs[cluster_key]] for obs in group_a_filtered])
    idx_b = np.array([cluster_to_idx[obs[cluster_key]] for obs in group_b_filtered])

    # Generate ONE set of Dirichlet weights for shared clusters
    # This is the key: same cluster gets same weight in both groups
    W_clusters = rng.dirichlet(np.ones(n_clusters), size=n_draws)

    # Map cluster weights to observations, DIVIDED BY CLUSTER SIZE
    # This ensures each cluster contributes equally within each group
    W_a = W_clusters[:, idx_a] / cluster_sizes_a[idx_a]
    W_b = W_clusters[:, idx_b] / cluster_sizes_b[idx_b]

    # Normalize weights within each group
    W_a = W_a / W_a.sum(axis=1, keepdims=True)
    W_b = W_b / W_b.sum(axis=1, keepdims=True)

    # Compute statistics
    stats_a = np.array([statistic(group_a_filtered, w) for w in W_a])
    stats_b = np.array([statistic(group_b_filtered, w) for w in W_b])
    delta = stats_a - stats_b

    lo, hi = np.percentile(delta, [2.5, 97.5])
    return {
        'mean': float(delta.mean()),
        'median': float(np.median(delta)),
        'lo': float(lo),
        'hi': float(hi),
        'p_gt_0': float((delta > 0).mean()),
        'p_lt_0': float((delta < 0).mean()),
        'n_clusters': n_clusters,
        'n_a': n_a,
        'n_b': n_b
    }


def bayes_bootstrap_single_internal_clustering(
    runs: list[dict],
    statistic: Callable,
    cluster_key: str = "test_id",
    n_draws: int = 10000,
    seed: int = 0,
    compare_to: float = 0.0
) -> dict | None:
    """
    Bayesian bootstrap for a single-group statistic with internal clustering.

    Observations are clustered by cluster_key. Each cluster gets a Dirichlet weight,
    which is then divided among observations in that cluster. This ensures each unique
    cluster contributes equally regardless of how many observations it contains.

    Use case: When pooling across doc_levels where the same test_id appears multiple
    times (once per doc_level). We want to weight by test, not by observation.

    Args:
        runs: List of observation dicts
        statistic: Callable that takes (runs, weights) -> float
        cluster_key: Field name to cluster on (e.g., "test_id")
        n_draws: Number of bootstrap samples
        seed: Random seed
        compare_to: Threshold for probability comparison (default 0)

    Returns:
        dict with mean, median, lo, hi (95% CI), p_lt, p_gt, n_clusters, n_obs
    """
    rng = np.random.default_rng(seed)

    if not runs:
        return None

    # Get unique clusters
    clusters = sorted(set(obs[cluster_key] for obs in runs))
    n_clusters = len(clusters)

    if n_clusters == 0:
        return None

    # Create cluster index mapping
    cluster_to_idx = {c: i for i, c in enumerate(clusters)}

    # Count observations per cluster
    cluster_sizes = np.zeros(n_clusters)
    for obs in runs:
        cluster_sizes[cluster_to_idx[obs[cluster_key]]] += 1

    # Map observations to their cluster indices
    idx = np.array([cluster_to_idx[obs[cluster_key]] for obs in runs])

    # Generate Dirichlet weights for clusters
    W_clusters = rng.dirichlet(np.ones(n_clusters), size=n_draws)

    # Map cluster weights to observations, DIVIDED BY CLUSTER SIZE
    # This ensures each cluster contributes equally regardless of # observations
    W = W_clusters[:, idx] / cluster_sizes[idx]

    # Normalize weights to sum to 1
    W = W / W.sum(axis=1, keepdims=True)

    # Compute statistic for each bootstrap sample
    stats = np.array([statistic(runs, w) for w in W])

    lo, hi = np.percentile(stats, [2.5, 97.5])

    return {
        'mean': float(stats.mean()),
        'median': float(np.median(stats)),
        'lo': float(lo),
        'hi': float(hi),
        'p_lt': float((stats < compare_to).mean()),
        'p_gt': float((stats > compare_to).mean()),
        'compare_to': compare_to,
        'n_clusters': n_clusters,
        'n_obs': len(runs)
    }


# =============================================================================
# Results Storage
# =============================================================================

DEFAULT_BOOTSTRAP_RESULTS_FILE = "bayesian_bootstrapping_results.json"


def load_bootstrap_results(filepath: str = DEFAULT_BOOTSTRAP_RESULTS_FILE) -> dict:
    """Load existing bootstrap results from file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {"runs": []}


def save_bootstrap_run(
    description: str,
    results: dict,
    metadata: dict | None = None,
    filepath: str = DEFAULT_BOOTSTRAP_RESULTS_FILE
) -> str:
    """
    Save a bootstrap run to the results file.

    Args:
        description: Manual description of what this run tests/analyzes
        results: The bootstrapping results dict (from analysis)
        metadata: Optional additional metadata (e.g., parameters used)
        filepath: Path to the results file

    Returns:
        The generated run_id
    """
    data = load_bootstrap_results(filepath)

    run_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    run_entry = {
        "run_id": run_id,
        "timestamp": timestamp,
        "description": description,
        "metadata": metadata or {},
        "results": results
    }

    data["runs"].append(run_entry)

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Saved bootstrap run: {run_id}")
    print(f"  Description: {description}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Total runs in file: {len(data['runs'])}")

    return run_id


def get_bootstrap_run(
    run_id: str,
    filepath: str = DEFAULT_BOOTSTRAP_RESULTS_FILE
) -> dict | None:
    """Retrieve a specific bootstrap run by ID."""
    data = load_bootstrap_results(filepath)
    for run in data["runs"]:
        if run["run_id"] == run_id:
            return run
    return None


def list_bootstrap_runs(
    filepath: str = DEFAULT_BOOTSTRAP_RESULTS_FILE
) -> list[dict]:
    """List all bootstrap runs (summary only, without full results)."""
    data = load_bootstrap_results(filepath)
    summaries = []
    for run in data["runs"]:
        summaries.append({
            "run_id": run["run_id"],
            "timestamp": run["timestamp"],
            "description": run["description"],
            "metadata": run.get("metadata", {})
        })
    return summaries

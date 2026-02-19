from rl.types import EpisodeResult, RewardFn

def default_reward_fn(result: EpisodeResult) -> float:
    """Simple dense reward to get started.

    - Base: normalized score [0, 1]
    - Bonus: +1 for fully passed tasks
    """
    reward = result.score_percent / 100.0
    if result.passed:
        reward += 1.0
    return reward

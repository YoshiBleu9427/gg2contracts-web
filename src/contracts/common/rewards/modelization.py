from contracts.common.models import Reward, User

from .all_rewards import ALL_REWARDS


def reward_by_name(name: str) -> Reward | None:
    for r in ALL_REWARDS:
        if r.name == name:
            return r
    return None


def to_reward_indices(rewards: list[Reward]) -> list[int]:
    return [ALL_REWARDS.index(r) for r in rewards]


def to_reward_names(rewards: list[Reward]) -> list[str]:
    return [r.name for r in rewards]


def user_reward_names(user: User) -> list[str]:
    if not user.reward_indices:
        return []
    return [
        ALL_REWARDS[index].name
        for index in user.reward_indices
        if index < len(ALL_REWARDS)
    ]

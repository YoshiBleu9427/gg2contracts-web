from contracts.common.models import Reward, User

from .modelization import reward_by_name, to_reward_indices

MEDAL_MAX_COUNT = 2


class InsufficientFunds(Exception):
    pass


class TooManyMedals(Exception):
    pass


def _can_buy(rewards: list[Reward], budget: int) -> bool:
    total = sum(r.price for r in rewards)
    return budget >= total


def _is_medal(reward_name: str) -> bool:
    return reward_name.startswith("Cnt_medal_")


def _medal_count(reward_names: list[str]) -> int:
    cnt = 0
    for name in reward_names:
        if _is_medal(name):
            cnt += 1
    return cnt


def grant_from_names(user: User, names: list[str], for_free: bool = False):
    if _medal_count(names) > MEDAL_MAX_COUNT:
        raise TooManyMedals
    requested_rewards = [r for name in names if (r := reward_by_name(name))]
    if not for_free and not _can_buy(requested_rewards, user.points):
        raise InsufficientFunds
    user.reward_indices = to_reward_indices(requested_rewards)

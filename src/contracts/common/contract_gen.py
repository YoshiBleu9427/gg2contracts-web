import random

from contracts.common.enums import ContractType
from contracts.common.models import Contract, GameClass, User

# TODO test assert all enum options are here

VALUES_BY_TYPE: dict[ContractType, list[int]] = {
    ContractType.DEBUG: [0],
    ContractType.KILLS: [5, 15, 25],
    ContractType.KILLS_AS_CLASS: [3, 5, 10],
    ContractType.KILLS_ON_CLASS: [2, 4, 10],
    ContractType.HEALING: [3, 5, 7],
    ContractType.UBERS: [2, 5],
    ContractType.ROUNDS_PLAYED: [2, 3, 5],
    ContractType.ROUNDS_WON: [1, 2, 3],
}

POINTS_BY_TYPE: dict[ContractType, list[int]] = {
    ContractType.DEBUG: [0],
    ContractType.KILLS: [10, 30, 50],
    ContractType.KILLS_AS_CLASS: [9, 15, 30],
    ContractType.KILLS_ON_CLASS: [8, 16, 40],
    ContractType.HEALING: [6, 10, 14],
    ContractType.UBERS: [6, 15],
    ContractType.ROUNDS_PLAYED: [2, 3, 5],
    ContractType.ROUNDS_WON: [2, 4, 6],
}


def _generate_gameclass(for_user: User) -> GameClass:
    if random.random() < 0.6:
        return for_user.main_class
    return random.choice(list(GameClass))


def _generate_contract_type(for_class: GameClass) -> ContractType:
    rng = random.random()
    choices: list[ContractType]
    if rng < 0.75:
        # COMMON
        choices = [
            ContractType.KILLS,
            ContractType.KILLS_ON_CLASS,
            ContractType.ROUNDS_PLAYED,
            ContractType.ROUNDS_WON,
        ]
    else:
        # CLASS-SPECIFIC
        if for_class == GameClass.HEALER:
            choices = [ContractType.UBERS, ContractType.HEALING]
        else:
            choices = [ContractType.KILLS_AS_CLASS]

    return random.choice(choices)


def generate_contract(for_user: User) -> Contract:
    game_class = _generate_gameclass(for_user)
    contract_type = _generate_contract_type(game_class)
    possible_values = VALUES_BY_TYPE[contract_type]
    random_index = random.randint(0, len(possible_values) - 1)
    return Contract(
        contract_type=contract_type,
        value=0,
        target_value=possible_values[random_index],
        game_class=game_class,
        points=POINTS_BY_TYPE[contract_type][random_index],
        user=for_user,
    )

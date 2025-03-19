import random
from contracts.common.enums import ContractType
from contracts.common.models import Contract, User, GameClass

# TODO test assert all enum options are here

VALUES_BY_TYPE: dict[ContractType: list[int]] = {
    ContractType.DEBUG: [0],
    ContractType.KILLS: [5],
    ContractType.KILLS_AS_CLASS: [3],
    ContractType.KILLS_ON_CLASS: [2],
    ContractType.HEALING: [500],
    ContractType.UBERS: [2],
    ContractType.ROUNDS_PLAYED: [3],
    ContractType.ROUNDS_WON: [3],
}

POINTS_BY_TYPE: dict[ContractType: list[int]] = {
    ContractType.DEBUG: [0],
    ContractType.KILLS: [5],
    ContractType.KILLS_AS_CLASS: [5],
    ContractType.KILLS_ON_CLASS: [5],
    ContractType.HEALING: [5],
    ContractType.UBERS: [2],
    ContractType.ROUNDS_PLAYED: [3],
    ContractType.ROUNDS_WON: [3],
}

def _generate_gameclass(for_user: User, contract_type: ContractType) -> GameClass:
    match contract_type:
        case ContractType.KILLS_AS_CLASS:
            return for_user.main_class
        case ContractType.KILLS_ON_CLASS:
            if random.random() < 0.8:
                return for_user.main_class
            return random.choice(list(GameClass))
        case _:
            return GameClass.RUNNER


def generate_contract(for_user: User) -> Contract:
    contract_type: ContractType = random.choice(list(ContractType))
    possible_values = VALUES_BY_TYPE[contract_type]
    random_index = random.randint(0, len(possible_values) - 1)
    return Contract(
        contract_type=contract_type,
        value=0,
        target_value=possible_values[random_index],
        game_class=_generate_gameclass(for_user, contract_type),
        points=POINTS_BY_TYPE[contract_type][random_index],
        user=for_user,
    )

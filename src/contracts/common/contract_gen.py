import random

from contracts.common.enums import ContractType
from contracts.common.models import Contract, GameClass, User

# TODO test assert all enum options are here

COMMON_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.KILLS: [(5, 10), (15, 35), (25, 60)],
    ContractType.ROUNDS_PLAYED: [(2, 2), (3, 4), (5, 7)],
    ContractType.ROUNDS_WON: [(1, 4), (2, 10), (3, 16)],
    ContractType.CAPTURES: [(3, 10), (7, 25), (12, 50)],
}
RARE_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.KILLS_ON_CLASS: [(2, 8), (4, 16), (6, 24)],
    ContractType.DOMINATIONS: [(2, 10), (3, 16), (5, 30)],
    ContractType.UBERED_KILLS: [(3, 10), (10, 40)],
    ContractType.KILL_STREAK: [(5, 15), (7, 30), (10, 50)],
    ContractType.UBERED_STREAK: [(2, 15), (3, 25)],
}
CLASS_CONTRACTS: dict[GameClass, dict[ContractType, list[tuple[int, int]]]] = {
    GameClass.RUNNER: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.CAPTURES: [(5, 20), (30, 150)],
    },
    GameClass.FIREBUG: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.BURN_DURATION: [(4, 3), (6, 6), (10, 12), (15, 20)],
        ContractType.FLARE_KILLS: [(1, 8), (2, 18), (3, 30)],
    },
    GameClass.ROCKETMAN: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.DOMINATIONS: [(2, 10), (3, 16), (5, 30)],
        ContractType.DAMAGE_TAKEN: [(5, 4), (8, 8), (12, 20), (15, 50)],
    },
    GameClass.OVERWEIGHT: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.DOMINATIONS: [(2, 10), (3, 16), (5, 30)],
        ContractType.DAMAGE_TAKEN: [(5, 4), (8, 8), (12, 20), (15, 50)],
    },
    GameClass.DETONATOR: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.CAPTURES: [(5, 20), (30, 150)],
        ContractType.KILL_STREAK: [(3, 10), (5, 15), (7, 30)],
    },
    GameClass.HEALER: {
        ContractType.HEALING: [(3, 6), (5, 12), (7, 18), (20, 55)],
        ContractType.UBERS: [(2, 6), (5, 15)],
        ContractType.HEAL_STREAK: [(3, 6), (7, 25), (10, 50), (20, 200)],
        ContractType.UBERED_KILLS: [(3, 10), (10, 40), (20, 90)],
        ContractType.UBERED_STREAK: [(2, 15), (3, 25)],
    },
    GameClass.CONSTRUCTOR: {
        ContractType.AUTOGUN_KILLS: [(3, 7), (6, 15), (10, 30)],
        ContractType.AUTOGUN_STREAK: [(2, 10), (3, 20), (4, 30)],
        ContractType.GUN_KILLS: [(2, 8), (5, 25), (10, 60)],
    },
    GameClass.RIFLEMAN: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.DOMINATIONS: [(2, 10), (3, 16), (5, 30)],
    },
    GameClass.INFILTRATOR: {
        ContractType.STABS: [(2, 10), (3, 15), (5, 25)],
        ContractType.GUN_KILLS: [(2, 10), (5, 25), (10, 60)],
        ContractType.CAPTURES: [(3, 12), (5, 20)],
    },
    GameClass.QUOTE: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 15), (10, 30)],
        ContractType.DAMAGE_TAKEN: [(5, 4), (8, 8), (12, 20), (15, 50)],
        ContractType.CAPTURES: [(3, 12), (5, 20)],
    },
}


def _generate_gameclass(for_user: User) -> GameClass:
    if random.random() < 0.6:
        return for_user.main_class
    return random.choice(list(GameClass))


def generate_contract(for_user: User, active_contracts: list[Contract]) -> Contract:
    game_class = _generate_gameclass(for_user)

    has_common_contract = False
    has_rare_contract = False
    for contract in active_contracts:
        if contract.contract_type in COMMON_CONTRACTS:
            has_common_contract = True
        elif contract.contract_type in RARE_CONTRACTS:
            has_rare_contract = True

    if not has_common_contract:
        choosables = COMMON_CONTRACTS
    elif not has_rare_contract:
        choosables = RARE_CONTRACTS
    else:
        choosables = CLASS_CONTRACTS[game_class]

    chooseable_types = list(choosables.keys())
    contract_type = random.choice(chooseable_types)
    possible_values = choosables[contract_type]
    chosen_target, chosen_points = random.choice(possible_values)

    return Contract(
        contract_type=contract_type,
        value=0,
        target_value=chosen_target,
        game_class=game_class,
        points=chosen_points,
        user=for_user,
    )

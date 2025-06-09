import random

from contracts.common.enums import ContractType
from contracts.common.models import Contract, GameClass, User

# TODO test assert all enum options are here

COMMON_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.KILLS: [(5, 12), (15, 40), (25, 75)],
    ContractType.ROUNDS_PLAYED: [(2, 5), (3, 10), (5, 16)],
    ContractType.ROUNDS_WON: [(1, 5), (2, 11), (3, 18)],
}
RARE_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.CAPTURES: [(3, 15), (7, 30), (12, 60)],
    ContractType.DOMINATIONS: [(2, 20), (3, 35), (5, 60)],
    ContractType.KILL_STREAK: [(3, 20), (4, 30), (5, 50)],
}
CLASS_CONTRACTS: dict[GameClass, dict[ContractType, list[tuple[int, int]]]] = {
    GameClass.RUNNER: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.KILLS_ON_CLASS: [(2, 12), (3, 20), (4, 30)],
        ContractType.CAPTURES: [(3, 15), (5, 20), (7, 30), (12, 60)],
    },
    GameClass.FIREBUG: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.KILLS_ON_CLASS: [(2, 12), (3, 20), (4, 30)],
        ContractType.BURN_DURATION: [(4, 3), (6, 6), (10, 12), (15, 20)],
        ContractType.FLARE_KILLS: [(1, 8), (2, 18), (3, 30)],
    },
    GameClass.ROCKETMAN: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.KILLS_ON_CLASS: [(2, 12), (3, 20), (4, 30)],
        ContractType.DAMAGE_TAKEN: [(3, 4), (5, 10), (7, 20), (9, 50)],
    },
    GameClass.OVERWEIGHT: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.KILLS_ON_CLASS: [(2, 12), (3, 20), (4, 30)],
        ContractType.DAMAGE_TAKEN: [(3, 4), (5, 10), (7, 20), (9, 50)],
    },
    GameClass.DETONATOR: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.FLYING_STICKY: [(2, 12), (3, 20), (4, 30)],
    },
    GameClass.HEALER: {
        ContractType.HEALING: [(12, 6), (18, 12), (25, 18), (100, 70)],
        ContractType.UBERS: [(2, 6), (5, 15)],
        ContractType.HEAL_STREAK: [(5, 6), (8, 18), (10, 30), (12, 60)],
        ContractType.UBERED_KILLS: [(2, 20), (3, 35), (4, 50), (5, 75)],
        ContractType.UBERED_STREAK: [(2, 35)],
    },
    GameClass.CONSTRUCTOR: {
        ContractType.AUTOGUN_KILLS: [(3, 10), (6, 22), (10, 40)],
        ContractType.AUTOGUN_STREAK: [(2, 15)],
        ContractType.GUN_KILLS: [(2, 8), (5, 25), (10, 60)],
    },
    GameClass.RIFLEMAN: {
        ContractType.NOSCOPE_KILLS: [(3, 12), (5, 22), (10, 45)],
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.DOMINATIONS: [(2, 20), (3, 35), (5, 60)],
        ContractType.KILL_STREAK: [(3, 20), (4, 30), (5, 50)],
    },
    GameClass.INFILTRATOR: {
        ContractType.KILLS_AS_CLASS: [(3, 9), (5, 16), (10, 35)],
        ContractType.STABS: [(2, 14), (3, 20), (5, 36)],
        ContractType.GUN_KILLS: [(2, 10), (5, 25), (10, 60)],
        ContractType.CAPTURES: [(3, 15), (10, 50)],
        ContractType.KILL_STREAK: [(2, 15), (3, 20), (4, 30)],
    },
    GameClass.QUOTE: {
        ContractType.KILLS_AS_CLASS: [(2, 9), (3, 15), (5, 30)],
        ContractType.BUBBLE_SHIELD: [(3, 6), (5, 10), (7, 16), (10, 25)],
        ContractType.CAPTURES: [(3, 15), (10, 50)],
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

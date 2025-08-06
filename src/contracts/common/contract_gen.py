import random

from contracts.common.enums import ContractType
from contracts.common.models import Contract, GameClass, User

# TODO test assert all enum options are here

COMMON_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.KILLS: [(5, 12), (12, 40), (20, 75)],
    ContractType.ROUNDS_PLAYED: [(1, 5), (2, 10), (3, 16)],
    ContractType.ROUNDS_WON: [(1, 10), (2, 20), (3, 35)],
}
RARE_CONTRACTS: dict[ContractType, list[tuple[int, int]]] = {
    ContractType.CAPTURES: [(3, 20), (5, 40), (8, 75)],
    ContractType.DOMINATIONS: [(1, 20), (2, 35), (4, 60)],
    ContractType.KILL_STREAK: [(2, 20), (3, 30), (4, 50)],
}
CLASS_CONTRACTS: dict[GameClass, dict[ContractType, list[tuple[int, int]]]] = {
    GameClass.RUNNER: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.KILLS_ON_CLASS: [(2, 20), (3, 32), (4, 45)],
        ContractType.CAPTURES: [(3, 20), (5, 40), (8, 75), (12, 120)],
    },
    GameClass.FIREBUG: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.KILLS_ON_CLASS: [(2, 20), (3, 32), (4, 45)],
        ContractType.BURN_DURATION: [(4, 6), (6, 12), (10, 24), (15, 40)],
        ContractType.FLARE_KILLS: [(1, 20), (2, 50), (3, 80)],
    },
    GameClass.ROCKETMAN: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.KILLS_ON_CLASS: [(2, 20), (3, 32), (4, 45)],
        ContractType.DAMAGE_TAKEN: [(3, 5), (5, 15), (6, 30), (7, 80)],
    },
    GameClass.OVERWEIGHT: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.KILLS_ON_CLASS: [(2, 20), (3, 32), (4, 45)],
        ContractType.DAMAGE_TAKEN: [(3, 5), (5, 15), (6, 30), (7, 80)],
    },
    GameClass.DETONATOR: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.FLYING_STICKY: [(2, 12), (3, 20), (4, 30)],
    },
    GameClass.HEALER: {
        ContractType.HEALING: [(12, 10), (18, 20), (30, 30)],
        ContractType.UBERS: [(2, 9), (5, 25)],
        ContractType.HEAL_STREAK: [(5, 6), (8, 18), (10, 30), (12, 60)],
        ContractType.UBERED_KILLS: [(2, 20), (3, 35), (4, 50)],
    },
    GameClass.CONSTRUCTOR: {
        ContractType.AUTOGUN_KILLS: [(3, 15), (5, 30), (7, 45)],
        ContractType.AUTOGUN_STREAK: [(2, 15)],
        ContractType.GUN_KILLS: [(2, 15), (3, 25), (5, 45)],
    },
    GameClass.RIFLEMAN: {
        ContractType.NOSCOPE_KILLS: [(3, 18), (5, 35), (7, 50)],
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.DOMINATIONS: [(1, 20), (2, 35), (4, 60)],
        ContractType.KILL_STREAK: [(2, 20), (3, 30), (4, 50)],
    },
    GameClass.INFILTRATOR: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.STABS: [(2, 14), (3, 20), (5, 36)],
        ContractType.GUN_KILLS: [(2, 10), (5, 25), (10, 60)],
        ContractType.KILL_STREAK: [(2, 20), (3, 30), (4, 50)],
    },
    GameClass.QUOTE: {
        ContractType.KILLS_AS_CLASS: [(3, 15), (5, 30)],
        ContractType.BUBBLE_SHIELD: [(3, 10), (5, 20), (7, 30)],
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

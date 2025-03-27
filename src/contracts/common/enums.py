from enum import IntEnum


class ContractType(IntEnum):
    KILLS = 1
    KILLS_ON_CLASS = 2
    KILLS_AS_CLASS = 3
    HEALING = 4
    UBERS = 5
    ROUNDS_PLAYED = 6
    ROUNDS_WON = 7
    DOMINATIONS = 8
    CAPTURES = 9
    STABS = 10
    BURN_DURATION = 11
    AUTOGUN_KILLS = 12
    UBERED_KILLS = 13
    DAMAGE_TAKEN = 14
    KILL_STREAK = 15
    HEAL_STREAK = 16
    AUTOGUN_STREAK = 17
    FLARE_KILLS = 18
    GUN_KILLS = 19
    UBERED_STREAK = 20

    DEBUG = 69


class GameClass(IntEnum):
    RUNNER = 0
    FIREBUG = 8
    ROCKETMAN = 1
    OVERWEIGHT = 6
    DETONATOR = 3
    HEALER = 4
    CONSTRUCTOR = 5
    RIFLEMAN = 2
    INFILTRATOR = 7
    QUOTE = 9

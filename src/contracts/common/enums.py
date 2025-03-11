from enum import IntEnum


class ContractType(IntEnum):
    KILLS = 1
    KILLS_ON_CLASS = 2
    KILLS_AS_CLASS = 3
    HEALING = 4
    UBERS = 5
    ROUNDS_PLAYED = 6
    ROUNDS_WON = 7

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

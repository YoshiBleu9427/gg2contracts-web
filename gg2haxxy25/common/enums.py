from enum import IntEnum, auto


class ContractType(IntEnum):
    KILLS = 1
    KILLS_ON_CLASS = 2
    KILLS_AS_CLASS = 3
    HEALING = 4
    UBERS = 5
    ROUNDS = 6


class GameClass(IntEnum):
    # TODO match those to the gg2 constants
    RUNNER = auto()
    FIREBUG = auto()
    ROCKETMAN = auto()
    OVERWEIGHT = auto()
    DETONATOR = auto()
    HEALER = auto()
    CONSTRUCTOR = auto()
    RIFLEMAN = auto()
    INFILTRATOR = auto()
    QUOTE = auto()

from enum import IntEnum


class ClientMessageHeader(IntEnum):
    HELLO = 0
    LOGIN = 1
    NEW_ACCOUNT = 2
    SET_ACCOUNT_USERNAME = 3
    SEND_GAME_RESULTS = 4
    GET_CONTRACTS = 5


class ServerMessageHeader(IntEnum):
    HELLO = 0
    SUCCESS = 1
    FAIL = 2

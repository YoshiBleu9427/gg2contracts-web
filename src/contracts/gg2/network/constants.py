from enum import IntEnum
from uuid import UUID

MAGIC_HELLO = UUID("ca3db0d5429eb179b1cdb08af534787a")


class RequestMessageHeader(IntEnum):
    HELLO = 0
    LOGIN = 1
    NEW_ACCOUNT = 2
    SET_ACCOUNT_USERNAME = 3
    JOIN_SERVER = 4
    GET_CONTRACTS = 5

    REGISTER_SERVER = 100
    SERVER_RECEIVES_CLIENT = 101
    GAME_DATA = 102


class ResponseMessageHeader(IntEnum):
    HELLO = 0
    SUCCESS = 1
    FAIL = 2

    SESSION_TOKEN = 10
    PLAYER_CONTRACTS = 11
    UPDATE_CONTRACTS = 12

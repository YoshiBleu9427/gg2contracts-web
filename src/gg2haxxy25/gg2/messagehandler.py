import struct
from io import BytesIO
from typing import Callable

from sqlmodel import select

from gg2haxxy25.common.db.engine import get_session
from gg2haxxy25.common.models.user import User
from gg2haxxy25.gg2.gg2 import MAGIC_HELLO
from gg2haxxy25.gg2.network import read, write
from gg2haxxy25.gg2.network.constants import ClientMessageHeader, ServerMessageHeader


class FailedInteraction(Exception):
    pass


class MessageHandler:
    def __init__(self):
        self.expecting_data = True
        self.user: User | None = None

    def handle_data(self, buffer: BytesIO) -> bytes:
        header_byte = struct.unpack("<B", buffer.read(1))[0]
        header = ClientMessageHeader(header_byte)

        func = REQUEST_MESSAGE_CONTENT_BY_TYPE[header]

        try:
            result = func(self, buffer)
        except FailedInteraction:
            self.expecting_data = False
            result = write.uchar(ServerMessageHeader.FAIL)

        return result

    def on_hello(self, data: BytesIO) -> bytes:
        given_magic = read.uuid(data)
        if given_magic != MAGIC_HELLO:
            raise FailedInteraction

        return write.uchar(ServerMessageHeader.HELLO)

    def on_login(self, data: BytesIO) -> bytes:
        given_token = read.uuid(data)
        db = next(get_session())
        user = db.exec(select(User).where(User.game_token == given_token)).one_or_none()
        db.close()
        if not user:
            raise FailedInteraction

        self.user = user
        return write.uchar(ServerMessageHeader.SUCCESS)

    def on_new_account(self, data: BytesIO) -> bytes:
        given_username = read.short_string(data)
        given_class = read.uchar(data)

        new_user = User(username=given_username, main_class=given_class)

        db = next(get_session())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()

        self.user = new_user
        return write.uuid(new_user.game_token)

    def on_set_username(self, data: BytesIO) -> bytes:
        given_string = read.short_string(data)
        # find user
        # update user data
        raise FailedInteraction

    def on_game_results(self, data: BytesIO) -> bytes:
        # TODO tbd
        raise FailedInteraction

    def on_request_contracts(self, data: BytesIO) -> bytes:
        given_string = read.short_string(data)
        # find user
        # get contracts
        # if < 3, generate new contract
        # serialize contracts
        # send
        raise FailedInteraction


REQUEST_MESSAGE_CONTENT_BY_TYPE: dict[
    ClientMessageHeader, Callable[[MessageHandler, BytesIO], bytes]
] = {
    ClientMessageHeader.HELLO: MessageHandler.on_hello,
    ClientMessageHeader.LOGIN: MessageHandler.on_login,
    ClientMessageHeader.NEW_ACCOUNT: MessageHandler.on_new_account,
    ClientMessageHeader.SET_ACCOUNT_USERNAME: MessageHandler.on_set_username,
    ClientMessageHeader.SEND_GAME_RESULTS: MessageHandler.on_game_results,
    ClientMessageHeader.GET_CONTRACTS: MessageHandler.on_request_contracts,
}

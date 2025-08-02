import socket
from socketserver import StreamRequestHandler
from typing import Callable
from uuid import UUID, uuid4

from contracts.common.contract_gen import generate_contract
from contracts.common.db import queries
from contracts.common.db.engine import get_session
from contracts.common.logging import logger
from contracts.common.models import Contract, GameServer, User
from contracts.common.settings import settings
from contracts.gg2.network import read, write
from contracts.gg2.network.constants import (
    MAGIC_HELLO,
    RequestMessageHeader,
    ResponseMessageHeader,
)
from contracts.gg2.schemas import inschemas, outschemas


class FailedInteraction(Exception):
    pass


class MessageHandler(StreamRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        self.session = next(get_session())
        self.expecting_data = True
        self.got_hello = False
        self.user: User | None = None

        self.request: socket.socket
        super().__init__(*args, **kwargs)

    def handle(self) -> None:
        logger.info(f"[{self.request.getpeername()}] New connexion")

        try:
            while self.expecting_data:
                logger.debug(f"[{self.request.getpeername()}]  Awaiting header")
                try:
                    header_byte = read.uchar(self.request)
                except TimeoutError:
                    logger.info(f"[{self.request.getpeername()}]  Timeout")
                    self.expecting_data = False
                    return

                try:
                    header = RequestMessageHeader(header_byte)
                except ValueError:
                    logger.info(
                        f"[{self.request.getpeername()}]  Bad header {header_byte}"
                    )
                    self.expecting_data = False
                    self.request.send(write.uchar(ResponseMessageHeader.FAIL))
                    return

                func = REQUEST_MESSAGE_CONTENT_BY_TYPE[header]
                logger.info(f"[{self.request.getpeername()}]  {func.__name__}")

                try:
                    result = func(self)
                except FailedInteraction:
                    logger.info(
                        f"[{self.request.getpeername()}]  FailedInteraction {header}"
                    )
                    self.expecting_data = False
                    self.session.rollback()
                    self.request.send(write.uchar(ResponseMessageHeader.FAIL))
                    return
                except TimeoutError:
                    logger.info(f"[{self.request.getpeername()}]  Timeout")
                    self.expecting_data = False
                    self.session.rollback()
                    return
                except BaseException as e:
                    logger.error(f"[{self.request.getpeername()}]  Error: {e}")
                    self.expecting_data = False
                    self.session.rollback()
                    self.request.close()
                    raise e
                # TODO probably a better way to handle the exception chain

                logger.debug(
                    f"[{self.request.getpeername()}]  Sent response: {result!r}"
                )
                self.request.send(result)
        finally:
            self.session.close()

        logger.info(f"[{self.request.getpeername()}] Closed connexion")

    def on_hello(self) -> bytes:
        if self.got_hello:
            raise FailedInteraction

        given_magic = read.uuid(self.request)
        if given_magic != MAGIC_HELLO:
            raise FailedInteraction

        self.got_hello = True
        logger.debug("  got hello!")

        return write.uchar(ResponseMessageHeader.HELLO)

    def on_login(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        given_token = read.uuid(self.request)
        logger.debug(f"  Key {given_token}")
        user = queries.get_user(self.session, by__key_token=given_token)
        if not user:
            raise FailedInteraction

        self.user = user
        return write.uchar(ResponseMessageHeader.SUCCESS)

    def on_new_account(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        given_username = read.short_string(self.request)
        given_class = read.uchar(self.request)

        logger.debug(f"  {given_username} [{given_class}]")

        new_user = User(username=given_username, main_class=given_class)

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        self.user = new_user
        return write.uuid(new_user.key_token)

    def on_set_username(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        if not self.user:
            raise FailedInteraction

        given_string = read.short_string(self.request)
        logger.debug(f"  {given_string}")
        self.user.username = given_string
        self.session.add(self.user)
        self.session.commit()

        self.expecting_data = False
        return write.uchar(ResponseMessageHeader.SUCCESS)

    def on_player_joins_server(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        if not self.user:
            raise FailedInteraction

        given_server_id = read.uuid(self.request)
        logger.debug(f"  server id {given_server_id}")

        found_server = queries.get_game_server(self.session, given_server_id)
        if not found_server:
            raise FailedInteraction

        # Generate session
        if self.user.last_joined_server != given_server_id:
            self.user.last_joined_server = given_server_id
            self.user.session_token = uuid4()

        assert self.user.session_token  # assert not None, for typing

        # Generate contracts
        existing_contracts = queries.get_contracts(
            self.session, by__user_identifier=self.user.identifier, by__completed=False
        )
        existing_contracts_as_list = list(existing_contracts)

        to_create_count = settings.active_contracts_per_user - len(existing_contracts)
        new_contracts: list[Contract] = []
        for _ in range(to_create_count):
            new_contract = generate_contract(
                self.user, existing_contracts_as_list + new_contracts
            )
            self.session.add(new_contract)
            new_contracts.append(new_contract)

        self.session.commit()

        # Serialize
        contract_bytes = bytearray()
        contract_bytes += write.uchar(len(existing_contracts) + len(new_contracts))
        for contract in existing_contracts:
            self.session.refresh(contract)  # TODO why do I need to do that???
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()
        for contract in new_contracts:
            self.session.refresh(contract)
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()

        self.expecting_data = False
        return (
            write.uuid(self.user.session_token)
            + write.uint(self.user.points)
            + bytes(contract_bytes)
        )

    def on_request_contracts(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        if not self.user:
            raise FailedInteraction

        active_contracts = queries.get_contracts(
            self.session, by__user_identifier=self.user.identifier, by__completed=False
        )

        # Serialize
        contract_bytes = bytearray()
        contract_bytes += write.uchar(len(active_contracts))
        for contract in active_contracts:
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()

        self.expecting_data = False
        return bytes(contract_bytes)

    def on_server_register(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        given_name = read.short_string(self.request)

        new_server = GameServer(registered_server_name=given_name)
        self.session.add(new_server)
        self.session.commit()
        self.session.refresh(new_server)

        logger.debug(f"  Giving {new_server.identifier}")

        self.expecting_data = False
        return write.uuid(new_server.identifier) + write.uuid(
            new_server.validation_token
        )

    def on_server_receives_client(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        server_id = read.uuid(self.request)
        session_token = read.uuid(self.request)
        logger.debug(f"  server id {server_id}")
        logger.debug(f"  session {session_token}")

        found_user = queries.get_user(self.session, by__session_token=session_token)
        if not found_user:
            logger.warning("  user not found")
            raise FailedInteraction

        found_server = queries.get_game_server(self.session, by__identifier=server_id)
        if not found_server:
            logger.warning("  server not found")
            raise FailedInteraction

        if found_user.last_joined_server != server_id:
            found_user.last_joined_server = None
            self.session.add(found_user)
            self.session.commit()
            logger.warning("  user-server match failed")
            raise FailedInteraction

        found_user.server_validated_session = True
        self.session.add(found_user)
        self.session.commit()

        logger.debug("  session validated")

        active_contracts = queries.get_contracts(
            self.session, by__user_identifier=found_user.identifier, by__completed=False
        )

        # Serialize
        contract_bytes = bytearray()
        contract_bytes += write.uchar(len(active_contracts))
        for contract in active_contracts:
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()

        contract_bytes += outschemas.GG2OutRewards(
            rewards=found_user.rewards
        ).to_bytes()

        self.expecting_data = False
        return write.uchar(ResponseMessageHeader.SUCCESS) + contract_bytes

    def on_server_sends_game_data(self) -> bytes:
        if not self.got_hello:
            raise FailedInteraction

        server_id = read.uuid(self.request)
        logger.debug(f"  server id {server_id}")
        found_server = queries.get_game_server(self.session, by__identifier=server_id)
        if not found_server:
            raise FailedInteraction

        # consume validation token
        server_validation_token = read.uuid(self.request)
        logger.debug(f"  token {server_validation_token}")
        if found_server.validation_token != server_validation_token:
            raise FailedInteraction

        found_server.validation_token = uuid4()
        logger.debug("  validated token")

        # find users that we know have played on this server
        server_users = queries.get_users(
            self.session, by__server_id=server_id, by__server_validated=True
        )
        logger.debug(f"  server has {len(server_users)} known users")

        users_by_session = {
            user.session_token: user for user in server_users if user.session_token
        }

        pre_update_data = []

        # deserialize data
        item_count = read.uchar(self.request)
        logger.debug(f"  reading {item_count} items")
        for _ in range(item_count):
            deserialized_data = inschemas.InPlayerRoundEndData.from_bytes(self.request)
            user = users_by_session.get(deserialized_data.session_token)
            if not user:
                logger.debug(
                    f"    ignoring unknown session {deserialized_data.session_token}"
                )
                # ignore data if player moved to another server ig
                # TODO think about this more
                # because otherwise gameserver needs to keep track of
                # players reconnecting
                continue

            user_contracts_by_id = {con.identifier: con for con in user.contracts}
            user_active_contracts = [con for con in user.contracts if not con.completed]
            logger.debug(f"    user {user.identifier} has {len(user.contracts)}")

            completed_ids: list[UUID] = []
            new_contracts = []
            for con_data in deserialized_data.contracts:
                contract = user_contracts_by_id[con_data.contract_id]
                contract.update_value(con_data.value_modifier)
                if contract.completed:
                    if contract not in user_active_contracts:
                        continue

                    user_active_contracts.remove(contract)

                    contract.validated_by_identifier = server_id
                    completed_ids.append(contract.identifier)

                    new_contract = generate_contract(user, user_active_contracts)

                    self.session.add(new_contract)

                    new_contracts.append(new_contract)
                    user_active_contracts.append(new_contract)

            logger.debug(f"    generated {len(new_contracts)} new contracts")

            # TODO refactor because this is stupid
            pre_update_data.append(
                {
                    "session_token": deserialized_data.session_token,
                    "completed_contract_ids": completed_ids,
                    "new_contracts": new_contracts,
                }
            )

        # TODO see if this can be moved to the bottom, so that the validation
        # token isnt overwritten if something goes wrong here
        self.session.commit()

        update_data: list[outschemas.GG2OutContractUpdateData] = []
        for item in pre_update_data:
            for new_contract in item["new_contracts"]:
                self.session.refresh(new_contract)

            update_data_for_user = outschemas.GG2OutContractUpdateData(
                session_token=item["session_token"],
                completed_contract_ids=item["completed_contract_ids"],
                new_contracts=[
                    outschemas.GG2OutNewContract.from_contract(new_contract)
                    for new_contract in item["new_contracts"]
                ],
            )
            update_data.append(update_data_for_user)

        serialized_data = bytearray()
        serialized_data += write.uuid(found_server.validation_token)
        serialized_data += write.uchar(len(update_data))
        for update_item in update_data:
            serialized_data += update_item.to_bytes()

        self.expecting_data = False
        return bytes(serialized_data)


REQUEST_MESSAGE_CONTENT_BY_TYPE: dict[
    RequestMessageHeader, Callable[[MessageHandler], bytes]
] = {
    RequestMessageHeader.HELLO: MessageHandler.on_hello,
    RequestMessageHeader.LOGIN: MessageHandler.on_login,
    RequestMessageHeader.NEW_ACCOUNT: MessageHandler.on_new_account,
    RequestMessageHeader.SET_ACCOUNT_USERNAME: MessageHandler.on_set_username,
    RequestMessageHeader.JOIN_SERVER: MessageHandler.on_player_joins_server,
    RequestMessageHeader.GET_CONTRACTS: MessageHandler.on_request_contracts,
    RequestMessageHeader.REGISTER_SERVER: MessageHandler.on_server_register,
    RequestMessageHeader.SERVER_RECEIVES_CLIENT: MessageHandler.on_server_receives_client,
    RequestMessageHeader.GAME_DATA: MessageHandler.on_server_sends_game_data,
    # TODO "endpoint" for server to invalidate their previous validation token and request a new one
    # TODO "endpoint" for client to invalidate a contract and regenerate a new one instead
}

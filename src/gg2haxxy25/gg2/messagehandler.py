from io import BytesIO
from typing import Callable
from uuid import UUID, uuid4

from gg2haxxy25.common.contract_gen import generate_contract
from gg2haxxy25.common.db import queries
from gg2haxxy25.common.db.engine import get_session
from gg2haxxy25.common.models import GameServer, User
from gg2haxxy25.gg2.network import read, write
from gg2haxxy25.gg2.network.constants import (
    MAGIC_HELLO,
    RequestMessageHeader,
    ResponseMessageHeader,
)
from gg2haxxy25.gg2.schemas import inschemas, outschemas

# TODO replace print with logger


class FailedInteraction(Exception):
    pass


class MessageHandler:
    def __init__(self) -> None:
        self.session = next(get_session())
        self.expecting_data = True
        self.user: User | None = None

    def handle_data(self, buffer: BytesIO) -> bytes:
        header_byte = read.uchar(buffer)
        try:
            header = RequestMessageHeader(header_byte)
        except ValueError:
            print(f"  Bad header {header_byte}")
            self.expecting_data = False
            return write.uchar(ResponseMessageHeader.FAIL)

        func = REQUEST_MESSAGE_CONTENT_BY_TYPE[header]

        try:
            result = func(self, buffer)
        except FailedInteraction:
            print(f"  FailedInteraction {header}")
            self.expecting_data = False
            return write.uchar(ResponseMessageHeader.FAIL)

        return result

    def on_hello(self, data: BytesIO) -> bytes:
        print("  Hello")
        given_magic = read.uuid(data)
        if given_magic != MAGIC_HELLO:
            raise FailedInteraction

        return write.uchar(ResponseMessageHeader.HELLO)

    def on_login(self, data: BytesIO) -> bytes:
        print("  Login")
        given_token = read.uuid(data)
        print(f"  Key {given_token}")
        user = queries.get_user(self.session, by__key_token=given_token)
        if not user:
            raise FailedInteraction

        self.user = user
        return write.uchar(ResponseMessageHeader.SUCCESS)

    def on_new_account(self, data: BytesIO) -> bytes:
        print("  New account")
        given_username = read.short_string(data)
        given_class = read.uchar(data)

        print(f"  {given_username} [{given_class}]")

        new_user = User(username=given_username, main_class=given_class)

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        self.user = new_user
        return write.uuid(new_user.key_token)

    def on_set_username(self, data: BytesIO) -> bytes:
        print("  Set username")
        if not self.user:
            raise FailedInteraction

        given_string = read.short_string(data)
        print(f"  {given_string}")
        self.user.username = given_string
        self.session.add(self.user)
        self.session.commit()

        return write.uchar(ResponseMessageHeader.SUCCESS)

    def on_player_joins_server(self, data: BytesIO) -> bytes:
        print("  Player joins")
        if not self.user:
            raise FailedInteraction

        given_server_id = read.uuid(data)
        print(f"  server id {given_server_id}")

        # TODO fail if server does not exist

        self.user.last_joined_server = given_server_id
        self.user.challenge_token = uuid4()
        self.session.add(self.user)

        # TODO generate contracts?
        new_contract = generate_contract(self.user)
        self.session.add(new_contract)
        self.session.commit()

        contracts = queries.get_contracts(
            self.session, by__user_identifier=self.user.identifier, by__completed=False
        )

        contract_bytes = bytearray()
        contract_bytes += write.uchar(len(contracts))
        for contract in contracts:
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()

        return (
            write.uchar(ResponseMessageHeader.CHALLENGE_TOKEN)
            + write.uuid(self.user.challenge_token)
            + write.uchar(ResponseMessageHeader.PLAYER_CONTRACTS)
            + bytes(contract_bytes)
        )

    def on_request_contracts(self, data: BytesIO) -> bytes:
        print("  Get contracts")
        if not self.user:
            raise FailedInteraction

        active_contracts = queries.get_contracts(
            self.session, by__user_identifier=self.user.identifier, by__completed=False
        )

        # serialize contracts
        contract_bytes = bytearray()
        contract_bytes += write.uchar(len(active_contracts))
        for contract in active_contracts:
            serialized_contract = outschemas.GG2OutContract.from_contract(contract)
            contract_bytes += serialized_contract.to_bytes()

        # send
        return write.uchar(ResponseMessageHeader.PLAYER_CONTRACTS) + bytes(
            contract_bytes
        )

    def on_server_register(self, data: BytesIO) -> bytes:
        print("  Server register")
        new_server = GameServer()
        self.session.add(new_server)
        self.session.commit()
        self.session.refresh(new_server)

        print(f"  Giving {new_server.identifier}")

        return write.uuid(new_server.identifier)

    def on_server_receives_client(self, data: BytesIO) -> bytes:
        print("  Server receives client")
        server_id = read.uuid(data)
        challenge_token = read.uuid(data)
        print(f"  server id {server_id}")
        print(f"  challenge {challenge_token}")

        found_user = queries.get_user(self.session, by__challenge=challenge_token)
        if not found_user:
            raise FailedInteraction

        found_server = queries.get_game_server(self.session, by__identifier=server_id)
        if not found_server:
            raise FailedInteraction

        if found_user.last_joined_server != server_id:
            found_user.last_joined_server = None
            self.session.add(found_user)
            self.session.commit()
            raise FailedInteraction

        found_user.server_validated_challenge = True
        self.session.add(found_user)
        self.session.commit()

        print("  challenge validated")
        return write.uchar(ResponseMessageHeader.SUCCESS)

    def on_server_sends_game_data(self, data: BytesIO) -> bytes:
        print("  server sends game data")
        server_id = read.uuid(data)
        found_server = queries.get_game_server(self.session, by__identifier=server_id)
        if not found_server:
            raise FailedInteraction

        print(f"  server id {server_id}")

        # find users that we know have played on this server
        server_users = queries.get_users(
            self.session, by__server_id=server_id, by__server_validated=True
        )
        print(f"  server has {len(server_users)} known users")

        users_by_challenge = {
            user.challenge_token: user for user in server_users if user.challenge_token
        }

        pre_update_data = []

        # deserialize data
        item_count = read.uchar(data)
        print(f"  reading {item_count} items")
        for _ in range(item_count):
            deserialized_data = inschemas.InPlayerRoundEndData.from_bytes(data)
            user = users_by_challenge.get(deserialized_data.challenge_token)
            if not user:
                print(
                    f"    ignoring unknown challenge {deserialized_data.challenge_token}"
                )
                # ignore data if player moved to another server ig
                # TODO think about this more
                # because otherwise gameserver needs to keep track of
                # players reconnecting
                continue

            user_contracts_by_id = {con.identifier: con for con in user.contracts}
            print(f"    user {user.identifier} has {len(user.contracts)}")

            completed_ids: list[UUID] = []
            new_contracts = []
            for con_data in deserialized_data.contracts:
                contract = user_contracts_by_id[con_data.contract_id]
                contract.update_value(con_data.value_modifier)
                if contract.completed:
                    completed_ids.append(contract.identifier)
                    new_contract = generate_contract(user)
                    self.session.add(new_contract)
                    new_contracts.append(new_contract)

            print(f"    generated {len(new_contracts)} new contracts")

            # TODO refactor because this is stupid
            pre_update_data.append(
                {
                    "challenge_token": deserialized_data.challenge_token,
                    "completed_contract_ids": completed_ids,
                    "new_contracts": new_contracts,
                }
            )

        self.session.commit()

        update_data: list[outschemas.GG2OutContractUpdateData] = []
        for item in pre_update_data:
            for new_contract in item["new_contracts"]:
                self.session.refresh(new_contract)

            update_data_for_user = outschemas.GG2OutContractUpdateData(
                challenge_token=item["challenge_token"],
                completed_contract_ids=item["completed_contract_ids"],
                new_contracts=[
                    outschemas.GG2OutNewContract.from_contract(new_contract)
                    for new_contract in item["new_contracts"]
                ],
            )
            update_data.append(update_data_for_user)

        serialized_data = bytearray()
        serialized_data += write.uchar(len(update_data))
        for item in update_data:
            serialized_data += item.to_bytes()

        return write.uchar(ResponseMessageHeader.UPDATE_CONTRACTS) + bytes(
            serialized_data
        )


REQUEST_MESSAGE_CONTENT_BY_TYPE: dict[
    RequestMessageHeader, Callable[[MessageHandler, BytesIO], bytes]
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
}

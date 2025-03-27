from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_user
from contracts.common.enums import ContractType, GameClass
from contracts.common.models import Contract, User


@click.command()
@click.argument("user")
@click.argument("contract_type")
@click.argument("game_class")
@click.option("--value", default=0)
@click.option("--target_value", default=0)
@click.option("--points", default=0)
def generate(
    user: str,
    contract_type: str,
    game_class: str,
    value: int,
    target_value: int,
    points: int,
):
    session = next(get_session())

    found_user: User | None = None
    try:
        user_uuid = UUID(user)
        found_user = get_user(session, by__identifier=user_uuid)
    except ValueError:
        found_user = get_user(session, by__username=user)

    if not found_user:
        click.echo("Couldn't find given user")
        return

    try:
        contract_type_int = int(contract_type)
        found_contract_type = ContractType(contract_type_int)
    except ValueError:
        found_contract_type = ContractType[contract_type]

    try:
        game_class_int = int(game_class)
        found_game_class = GameClass(game_class_int)
    except ValueError:
        found_game_class = GameClass[game_class]

    new_contract = Contract(
        contract_type=found_contract_type,
        value=value,
        target_value=target_value,
        game_class=found_game_class,
        points=points,
        user=found_user,
    )

    try:
        session.add(new_contract)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.close()

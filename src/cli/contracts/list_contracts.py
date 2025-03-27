from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_contracts, get_user
from contracts.common.models import User


@click.command("list")
@click.option("--all", is_flag=True, help="list inactive contracts")
@click.option(
    "--user",
    default=None,
    help="list only contracts for given user (UUID or username)",
)
def list_contracts(all: bool, user: str | None):
    kwargs: dict = {}
    count = 0

    session = next(get_session())

    if not all:
        kwargs["by__completed"] = False

    if user:
        found_user: User | None = None
        try:
            user_uuid = UUID(user)
            found_user = get_user(session, by__identifier=user_uuid)
        except ValueError:
            found_user = get_user(session, by__username=user)

        if not found_user:
            click.echo("Couldn't find given user")
            return

        kwargs["by__user_identifier"] = found_user.identifier

    contracts = get_contracts(session, **kwargs)
    for contract in contracts:
        click.echo(
            f"{contract.user.username}: {contract.identifier} - {contract.contract_type.name} [{contract.value}/{contract.target_value}] +{contract.points}"
        )
        count += 1

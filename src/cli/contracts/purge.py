from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_contracts, get_user
from contracts.common.models import User


@click.command()
@click.option("--all", is_flag=True, help="purge all contracts")
@click.option(
    "--user",
    default=None,
    help="purge given contracts for given user (UUID or username)",
)
def purge(all: bool, user: str | None):
    click.echo("Purging contracts!")
    kwargs: dict = {}
    count = 0

    session = next(get_session())

    if not all:
        kwargs["by__completed"] = True

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

    try:
        contracts = get_contracts(session, **kwargs)
        for contract in contracts:
            session.delete(contract)
            count += 1

        session.commit()
        click.echo(f"Successfully purged {count} contracts.")
    except BaseException:
        click.echo(f"Failed to purge after {count}. Cancelling")
        session.rollback()

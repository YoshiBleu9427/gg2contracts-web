from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_user
from contracts.common.models import User
from contracts.common.rewards import grant_from_names


@click.command("grant")
@click.argument("user_identifier")
@click.option("--for-free", default=False)
@click.argument("reward_names", nargs=-1)
def grant(
    user_identifier: str,
    for_free: bool,
    reward_names: tuple[str, ...],
):
    session = next(get_session())

    found_user: User | None = None
    try:
        user_uuid = UUID(user_identifier)
    except ValueError:
        click.echo("Bad user ID")
        raise

    found_user = get_user(session, by__identifier=user_uuid)
    if not found_user:
        click.echo("User not found")
        session.rollback()
        raise

    reward_names_list = list(reward_names)

    try:
        grant_from_names(found_user, reward_names_list, for_free)
        session.add(found_user)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

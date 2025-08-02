from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_reward
from contracts.common.models import Reward


@click.command("delete")
@click.argument("identifier")
def delete(identifier: str):
    session = next(get_session())

    found_reward: Reward | None = None
    try:
        reward_uuid = UUID(identifier)
    except ValueError:
        click.echo("Bad ID")
        raise

    found_reward = get_reward(session, by__identifier=reward_uuid)

    try:
        session.delete(found_reward)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

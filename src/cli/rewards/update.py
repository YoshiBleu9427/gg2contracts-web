from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_reward
from contracts.common.models import Reward


@click.command("update")
@click.argument("identifier")
@click.option("--name")
@click.option("--description")
@click.option("--image_name")
@click.option("--price")
def update(
    identifier: str,
    name: str | None,
    description: str | None,
    image_name: str | None,
    price: int | None,
):
    session = next(get_session())

    found_reward: Reward | None = None
    try:
        reward_uuid = UUID(identifier)
    except ValueError:
        click.echo("Bad ID")
        raise

    found_reward = get_reward(session, by__identifier=reward_uuid)
    if not found_reward:
        click.echo("Reward not found")
        session.rollback()
        raise

    try:
        if name:
            found_reward.name = name

        if description:
            found_reward.description = description

        if image_name:
            found_reward.image_name = image_name

        if price:
            found_reward.price = price

        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

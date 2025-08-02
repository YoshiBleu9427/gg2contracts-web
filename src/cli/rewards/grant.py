from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_reward, get_user
from contracts.common.models import Reward, User


@click.command("grant")
@click.argument("reward_identifier")
@click.argument("user_identifier")
@click.option("--for-free", default=False)
def grant(
    reward_identifier: str,
    user_identifier: str,
    for_free: bool,
):
    session = next(get_session())

    found_reward: Reward | None = None
    try:
        reward_uuid = UUID(reward_identifier)
    except ValueError:
        click.echo("Bad reward ID")
        raise

    found_user: User | None = None
    try:
        user_uuid = UUID(user_identifier)
    except ValueError:
        click.echo("Bad user ID")
        raise

    found_reward = get_reward(session, by__identifier=reward_uuid)
    found_user = get_user(session, by__identifier=user_uuid)

    if not found_reward:
        click.echo("Reward not found")
        session.rollback()
        raise
    if not found_user:
        click.echo("User not found")
        session.rollback()
        raise

    try:
        if not for_free:
            if found_user.points < found_reward.price:
                click.echo("Insufficient funds.")
                session.rollback()
                return

            found_user.points -= found_reward.price

        found_user.rewards.append(found_reward)
        session.add(found_user)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

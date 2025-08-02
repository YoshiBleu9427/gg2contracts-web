import click

from contracts.common.db.engine import get_session
from contracts.common.models import Reward


@click.command()
@click.argument("name")
@click.argument("description")
@click.argument("image_name")
@click.argument("price", default=0)
def create(
    name: str,
    description: str,
    image_name: str,
    price: int,
):
    session = next(get_session())

    try:
        new_reward = Reward(
            name=name,
            description=description,
            image_name=image_name,
            price=price,
        )
        session.add(new_reward)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

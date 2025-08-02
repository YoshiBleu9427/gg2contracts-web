import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_rewards


@click.command("list")
@click.option(
    "--name",
    default=None,
    help="find rewards by name",
)
def list_rewards(name: str | None = None):
    session = next(get_session())

    kwargs = {}
    if name:
        kwargs["by__username"] = name

    rewards = get_rewards(session, **kwargs)  # type: ignore
    for reward in rewards:
        click.echo(reward.model_dump_json(exclude={"users"}))

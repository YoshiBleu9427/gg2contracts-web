import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_users


@click.command("list")
@click.option(
    "--name",
    default=None,
    help="find users by name",
)
def list_users(name: str | None = None):
    session = next(get_session())

    kwargs = {}
    if name:
        kwargs["by__username"] = name

    users = get_users(session, **kwargs)  # type: ignore
    for user in users:
        click.echo(user.model_dump_json())

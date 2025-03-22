import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_users


@click.command("list")
def list_users():
    session = next(get_session())
    users = get_users(session)
    for user in users:
        click.echo(user.model_dump_json())

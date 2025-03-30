from uuid import UUID

import click

from contracts.common.db.engine import get_session
from contracts.common.db.queries import get_user


@click.command()
@click.argument("identifier")
def delete(identifier: str):
    session = next(get_session())

    as_uuid = UUID(identifier)

    try:
        found_user = get_user(session, by__identifier=as_uuid)
        session.delete(found_user)
        session.commit()
        click.echo("Success.")
    except BaseException:
        click.echo("Failed")
        session.rollback()
        raise

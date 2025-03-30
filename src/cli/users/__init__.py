import click

from cli.users import delete, list_users


@click.group()
def users():
    pass


users.add_command(list_users.list_users)
users.add_command(delete.delete)

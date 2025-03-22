import click

from cli.users import list_users


@click.group()
def users():
    pass


users.add_command(list_users.list_users)

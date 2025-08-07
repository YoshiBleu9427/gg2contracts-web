import click

from cli.contracts import contracts
from cli.rewards import rewards
from cli.users import users


@click.group()
def main():
    pass


main.add_command(contracts)
main.add_command(rewards)
main.add_command(users)

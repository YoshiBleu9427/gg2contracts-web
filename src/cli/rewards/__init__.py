import click

from cli.rewards import grant


@click.group()
def rewards():
    pass


rewards.add_command(grant.grant)

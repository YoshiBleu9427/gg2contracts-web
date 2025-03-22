import click

from cli.contracts import purge


@click.group("contracts")
def contracts():
    pass


contracts.add_command(purge.purge)

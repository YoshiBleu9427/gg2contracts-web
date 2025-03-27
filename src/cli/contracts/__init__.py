import click

from cli.contracts import delete, generate, list_contracts, purge


@click.group("contracts")
def contracts():
    pass


contracts.add_command(generate.generate)
contracts.add_command(list_contracts.list_contracts)
contracts.add_command(delete.delete)
contracts.add_command(purge.purge)

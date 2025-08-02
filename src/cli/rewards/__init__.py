import click

from cli.rewards import create, delete, grant, list_rewards, update


@click.group()
def rewards():
    pass


rewards.add_command(create.create)
rewards.add_command(delete.delete)
rewards.add_command(grant.grant)
rewards.add_command(list_rewards.list_rewards)
rewards.add_command(update.update)

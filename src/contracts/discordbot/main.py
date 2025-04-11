from nextcord import Intents
from nextcord.ext import commands

from contracts.common.logging import logger
from contracts.common.settings import settings
from contracts.discordbot.commands import contract as contract_cmd
from contracts.discordbot.commands import lobby as lobby_cmd
from contracts.discordbot.commands import map as map_cmd


def main():
    logger.info("Starting up...")

    intents = Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="gg2", intents=intents)

    bot.intents

    logger.info("Loading commands")
    bot.add_command(map_cmd.map)
    bot.add_command(lobby_cmd.lobby)
    bot.add_command(contract_cmd.contract)

    logger.info("Running")
    bot.run(settings.discord_token)

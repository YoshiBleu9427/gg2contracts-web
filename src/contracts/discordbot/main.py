from nextcord.ext import commands

from contracts.common.logging import logger
from contracts.common.settings import settings
from contracts.discordbot.bot import make_bot
from contracts.discordbot.cogs.contract import ContractsCommandCog
from contracts.discordbot.cogs.itemserver import ItemserverCommandCog
from contracts.discordbot.cogs.lobby import LobbyCommandCog
from contracts.discordbot.cogs.map import MapCommandCog


async def handle_error(_, ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        if ctx.command:
            await ctx.send_help(ctx.command.full_parent_name)
        else:
            await ctx.send_help()
    else:
        logger.exception(error)
        await ctx.send("Internal error")


def main():
    logger.info("Starting up...")
    bot = make_bot()
    logger.info(f"Bot listens to prefix '{settings.discord_prefix}'")

    logger.info("Loading commands")

    # TODO better error handling
    ContractsCommandCog.top.error(handle_error)
    ContractsCommandCog.me.error(handle_error)
    LobbyCommandCog.lobby.error(handle_error)
    MapCommandCog.map.error(handle_error)

    # TODO autodiscover?
    bot.add_cog(ContractsCommandCog(bot))
    bot.add_cog(ItemserverCommandCog(bot))
    bot.add_cog(LobbyCommandCog(bot))
    bot.add_cog(MapCommandCog(bot))

    logger.info("Running")
    bot.run(settings.discord_token)

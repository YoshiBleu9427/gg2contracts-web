import nextcord
from nextcord.application_command import SlashOption
from nextcord.ext import commands

from contracts.common.logging import logger
from contracts.discordbot.modules import map as map_module


class MapCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="map")
    async def map_slash_command(
        self,
        interaction: nextcord.Interaction,
        map_name: str | None = SlashOption(
            description="Name of a map to fetch. If empty, returns a random map"
        ),
    ):
        """
        Returns a gg2 map

        Fetches a map by name from Derpduck's map archive on github,
        or returns a random one.
        """
        logger.debug("slashcmd map")
        result = map_module.map(map_name)
        await result.send_to_ctx(interaction)

    @commands.command()
    async def map(self, ctx: commands.Context, map_name: str | None):
        """
        Returns a gg2 map

        Fetches a map by name from Derpduck's map archive on github,
        or returns a random one.
        """
        logger.debug(f"cmd map {map_name}")
        result = map_module.map(map_name)
        await result.send_to_ctx(ctx)


async def map_error(ctx: commands.Context, error):
    logger.exception(error)
    await ctx.send("Internal error")


MapCommandCog.map.error(map_error)

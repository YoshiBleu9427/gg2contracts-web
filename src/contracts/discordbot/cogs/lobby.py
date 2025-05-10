import nextcord
from nextcord.ext import commands

from contracts.common.logging import logger
from contracts.discordbot.modules import lobby as lobby_module


class LobbyCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="lobby")
    async def lobby_slash_command(self, interaction: nextcord.Interaction):
        """
        Get gg2 lobby status
        """
        logger.debug("slashcmd lobby")
        result = lobby_module.lobby()
        await result.send_to_ctx(interaction)

    @commands.command()
    async def lobby(self, ctx: commands.Context):
        """
        Get lobby status
        """
        logger.debug("cmd lobby")
        result = lobby_module.lobby()
        await result.send_to_ctx(ctx)

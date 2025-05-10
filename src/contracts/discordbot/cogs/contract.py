import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context

from contracts.common.logging import logger
from contracts.discordbot.modules import contract as contract_module


class ContractsCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: "Context", error: Exception) -> None:
        if isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.invoked_with)
        else:
            logger.exception(error)
            await ctx.send("Internal error")

    @nextcord.slash_command(name="contracts")
    async def contracts_slash_command(
        self, interaction: nextcord.Interaction, limit: int = 3
    ):
        """
        Show contracts leaderboard
        """
        logger.debug(f"slashcmd contracts top limit={limit}")
        result = contract_module.top(limit)
        await result.send_to_ctx(interaction)

    @contracts_slash_command.subcommand(name="top")
    async def top_slash_command(
        self, interaction: nextcord.Interaction, limit: int = 3
    ):
        """
        Show contracts leaderboard
        """
        logger.debug(f"slashcmd contracts top limit={limit}")
        result = contract_module.top(limit)
        await result.send_to_ctx(interaction)

    @contracts_slash_command.subcommand(name="me")
    async def me_slash_command(self, interaction: nextcord.Interaction):
        """
        Show contracts leaderboard
        """
        logger.debug("slashcmd contracts me")

        assert interaction.user
        result = contract_module.me(interaction.user.name)

        await result.send_to_ctx(interaction)

    @contracts_slash_command.subcommand(name="link")
    async def link_slash_command(self, interaction: nextcord.Interaction):
        """
        Link discord account with contracts account.
        """
        logger.debug("slashcmd contracts link")

        assert interaction.user
        result = contract_module.link(interaction.user.name)

        await result.send_to_ctx(interaction)

    @contracts_slash_command.subcommand(name="unlink")
    async def unlink_slash_command(self, interaction: nextcord.Interaction):
        """
        Unlink any contracts account linked to your discord account.
        """
        logger.debug("slashcmd contracts unlink")

        assert interaction.user
        result = contract_module.unlink(interaction.user.name)

        await result.send_to_ctx(interaction)

    @commands.group(invoke_without_command=True)
    async def contracts(self, ctx: commands.Context):
        """Contracts leaderboard and user management"""
        logger.debug("cmd contracts <null>")
        await ctx.send_help("contracts")

    @contracts.command()
    async def top(self, ctx: commands.Context, limit: int = 3):
        """
        Show contracts leaderboard
        """
        logger.debug(f"cmd contracts top limit={limit}")
        result = contract_module.top(limit)
        await result.send_to_ctx(ctx)

    @contracts.command()
    async def me(self, ctx: commands.Context):
        """
        Show my current active contracts and stats
        """
        logger.debug("cmd contracts me")
        result = contract_module.me(ctx.author.name)
        await result.send_to_ctx(ctx)

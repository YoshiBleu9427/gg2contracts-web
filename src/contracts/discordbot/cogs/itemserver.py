from nextcord.ext import commands


class ItemserverCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def itemserver(self, ctx: commands.Context, *args: str):
        """???"""
        await ctx.send("It's gone, " + ctx.author.display_name)

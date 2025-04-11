from nextcord.ext import commands


@commands.command()
async def itemserver(ctx: commands.Context, *args: str):
    """???"""
    await ctx.send("It's gone, " + ctx.author.display_name)

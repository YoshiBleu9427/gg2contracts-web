from nextcord import Embed
from nextcord.ext import commands


@commands.command()
async def lobby(ctx: commands.Context):
    """
    Get lobby status
    """
    player_count = 42069  # TODO

    embed = Embed(
        title="Gang Garrison 2 Lobby Status",
        description=f"There are **{player_count}** players online.",
        url="https://www.ganggarrison.com/lobby/status",
        color=int.from_bytes(bytes.fromhex("A55420")),
    )
    embed.set_thumbnail(
        "https://cdn.discordapp.com/icons/699590084218847282/be805b3d3557a9cc2bf98ae19c5ae27c.webp?size=256"
    )

    # TODO pydantic model
    # TODO read from lobby
    servers = [{}, {}]

    for server in servers:
        embed.add_field(name="name", value="value", inline=False)

    await ctx.send(embed=embed)

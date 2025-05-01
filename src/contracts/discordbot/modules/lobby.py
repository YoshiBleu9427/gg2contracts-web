from nextcord import Embed

from contracts.common.logging import logger
from contracts.discordbot.sendable import Sendable
from contracts.gg2 import lobby as gg2lobby


def lobby() -> Sendable:
    """
    Get lobby status
    """
    logger.debug("cmd lobby")

    player_count = 0
    data = gg2lobby.get_lobby_data()
    for server in data.servers:
        player_count += server.players

    embed = Embed(
        title="Gang Garrison 2 Lobby Status",
        description=f"There are **{player_count}** players online.",
        url="https://www.ganggarrison.com/lobby/status",
        color=int.from_bytes(bytes.fromhex("A55420")),
    )
    embed.set_thumbnail(
        "https://cdn.discordapp.com/icons/699590084218847282/be805b3d3557a9cc2bf98ae19c5ae27c.webp?size=256"
    )

    for server in data.servers:
        desc = f"[{server.players}/{server.slots}] {server.info.get('map', '')}"
        # TODO also use game_short and game_ver

        embed.add_field(name=server.info.get("name", ""), value=desc, inline=False)

    return Sendable(embed=embed)

from datetime import datetime

from nextcord import Embed

from contracts.common.db.engine import get_session
from contracts.common.db.queries import (
    get_contracts,
    get_contracts_count,
    get_user,
    get_users,
)
from contracts.common.logging import logger
from contracts.discordbot.sendable import Sendable


def top(limit: int) -> Sendable:
    """
    Show contracts leaderboard
    """
    logger.debug(f"cmd contracts top limit={limit}")

    if limit > 20:
        logger.debug("limit too high")
        return Sendable(content="Limit must be 20 or less")
    if limit <= 0:
        logger.debug("limit too low")
        return Sendable(content="Limit must be greater than 0")

    session = next(get_session())

    users = get_users(session, limit=limit, order_by__points=True)

    session.close()

    if len(users) == 0:
        return Sendable(content="There are no users")

    embed = Embed(
        title=f"Contracts Top {limit} Leaderboard",
        description=f"**{users[0].username}** currently has made the most Canadium!",
        url="https://gg2.ybot.fr/users",
        color=int.from_bytes(bytes.fromhex("A55420")),
        timestamp=datetime.now(),
    )
    embed.set_thumbnail("https://gg2.ybot.fr/static/assets/favicon.png")

    for index, user in enumerate(users):
        embed.add_field(
            name=f"{index + 1}: {user.username}", value=f"{user.points} C$", inline=True
        )

    return Sendable(embed=embed)


def me(discord_username: str) -> Sendable:
    """
    Show my current active contracts and stats
    """
    logger.debug("cmd contracts me")

    session = next(get_session())
    user = get_user(session, by__discord_username=discord_username)

    if not user:
        session.close()
        return Sendable(
            content=f"I don't know who you are, {discord_username}. "
            "Did you sign up and update your profile with your discord username?"
        )

    contract_count = get_contracts_count(session, by__user_identifier=user.identifier)

    desc = (
        f"Contractor since <t:{int(user.created_at.timestamp())}>\n"
        f"Contracts completed: {contract_count}\n"
        f"Canadium earned: **{user.points}**\n\n"
        f"Active contracts:"
    )

    embed = Embed(
        title=f"Contract stats for: **{user.username}**",
        description=desc,
        color=int.from_bytes(bytes.fromhex("A55420")),
        timestamp=datetime.now(),
    )
    embed.set_thumbnail("https://gg2.ybot.fr/static/assets/favicon.png")

    contracts = get_contracts(
        session, by__user_identifier=user.identifier, by__completed=False
    )
    for contract in contracts:
        embed.add_field(
            name=contract.contract_type.name,
            value=f"`({contract.value}/{contract.target_value})` [{contract.points} C$]",
            inline=True,
        )

    session.close()

    return Sendable(embed=embed)

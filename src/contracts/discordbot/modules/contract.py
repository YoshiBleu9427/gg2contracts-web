from datetime import datetime
from uuid import UUID

import nextcord
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
            content="Sorry, I don't know who you are. "
            "Did you sign up and /link your profile to your discord account?"
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


def link(discord_username: str) -> Sendable:
    session = next(get_session())
    found_user = get_user(session, by__discord_username=discord_username)
    session.close()

    if found_user:
        return Sendable(content="Already associated")
    else:
        return Sendable(modal=AccountAssociationModal())


def unlink(discord_username: str) -> Sendable:
    session = next(get_session())

    found_user = get_user(session, by__discord_username=discord_username)

    if found_user:
        found_user.discord_username = None
        session.commit()
        session.close()
        return Sendable(content="Unlinked contracts account")
    else:
        session.close()
        return Sendable(content="No associated contracts account")


class AccountAssociationModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Associate contracts with discord account",
            timeout=5 * 60,  # 5 minutes
        )

        self.user_key = nextcord.ui.TextInput(
            label="user_key (find it in `gg2.ini`)",
            placeholder="1234567890abcdef1234567890abcdef",
            min_length=32,
            max_length=32,
        )
        self.add_item(self.user_key)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        assert interaction.user

        user_key_as_uuid = UUID(hex=self.user_key.value)

        session = next(get_session())
        found_user = get_user(session, by__key_token=user_key_as_uuid)

        if found_user:
            if found_user.discord_username:
                if found_user.discord_username == interaction.user.name:
                    response = "Accounts already associated. You're good to go!"
                else:
                    logger.warning(
                        f"Discord user {interaction.user.name} tried to associate using key {self.user_key.value} "
                        f"which is already associated with user {found_user.discord_username}"
                    )
                    response = "The given key is already associated with a different discord account."
            else:
                found_user.discord_username = interaction.user.name
                session.commit()
                response = f"Success! Your discord account is now associated to contracts account `{found_user.username}`."
        else:
            response = "Failed to associate: no user found with the given user key"

        session.close()

        await interaction.send(response, ephemeral=True)

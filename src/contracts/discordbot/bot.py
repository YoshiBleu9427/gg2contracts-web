from nextcord import Intents
from nextcord.ext.commands import Bot

from contracts.common.settings import settings
from contracts.discordbot.help_command import CustomHelpCommand


def make_bot() -> Bot:
    intents = Intents.default()
    intents.message_content = True

    bot_kwargs = {
        "command_prefix": settings.discord_prefix,
        "intents": intents,
        "help_command": CustomHelpCommand(),
    }

    if settings.discord_test_guild:
        bot_kwargs["default_guild_ids"] = [settings.discord_test_guild]

    bot = Bot(**bot_kwargs)  # type: ignore[arg-type]

    return bot

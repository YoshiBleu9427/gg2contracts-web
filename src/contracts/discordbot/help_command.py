from nextcord.ext.commands import Bot
from nextcord.ext.commands.help import DefaultHelpCommand


class CustomHelpCommand(DefaultHelpCommand):
    async def send_bot_help(self, _) -> None:
        ctx = self.context
        bot: Bot = ctx.bot

        if bot.description:
            self.paginator.add_line(bot.description, empty=True)

        filtered = await self.filter_commands(bot.commands)
        max_size = self.get_max_size(filtered)

        commands = sorted(filtered, key=lambda c: c.name)
        self.add_indented_commands(commands, heading="Commands:", max_size=max_size)

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()

    def get_ending_note(self) -> str:
        command_name = self.invoked_with
        return f"Type {self.context.clean_prefix}{command_name} command for more info on a command."

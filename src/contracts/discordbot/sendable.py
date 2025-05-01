import dataclasses

import nextcord
import nextcord.ext.commands.context


@dataclasses.dataclass
class Sendable:
    embed: nextcord.Embed | None = None
    content: str | None = None

    async def send_to_ctx(
        self, ctx: nextcord.ext.commands.context.Context | nextcord.Interaction
    ):
        if self.embed:
            await ctx.send(self.content, embed=self.embed)
        else:
            await ctx.send(self.content)

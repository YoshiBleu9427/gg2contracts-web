import dataclasses

import nextcord
import nextcord.ext.commands.context


@dataclasses.dataclass
class Sendable:
    modal: nextcord.ui.Modal | None = None
    embed: nextcord.Embed | None = None
    content: str | None = None

    async def send_to_ctx(
        self, ctx: nextcord.ext.commands.context.Context | nextcord.Interaction
    ):
        if self.modal:
            if isinstance(ctx, nextcord.Interaction):
                await ctx.response.send_modal(self.modal)
            else:
                raise NotImplementedError
        elif self.embed:
            await ctx.send(self.content, embed=self.embed)
        else:
            await ctx.send(self.content)

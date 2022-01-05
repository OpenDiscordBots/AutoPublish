from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog, slash_command

from src.bot import Bot


class Ping(Cog):
    """A simple ping command."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="ping")
    async def ping(self, ctx: ApplicationCommandInteraction) -> None:
        """Get the gateway latency of the bot."""

        await ctx.send(f"Pong! {self.bot.latency*1000:.2f}ms", ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))

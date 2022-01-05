from disnake import ApplicationCommandInteraction, NewsChannel, Message, ChannelType
from disnake.ext.commands import Cog, Param, slash_command, has_guild_permissions

from src.bot import Bot
from src.models import AutoPublishConfig


class Publish(Cog):
    """The code logic for AutoPublish."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self._cache: dict[int, AutoPublishConfig] = {}

    async def get_config(self, guild_id: int) -> AutoPublishConfig:
        if guild_id in self._cache:
            return self._cache[guild_id]

        config = (
            await self.bot.api.get_guild_config(guild_id, "autopub", AutoPublishConfig)
        ) or AutoPublishConfig(channels=[])

        self._cache[guild_id] = config

        return config

    async def set_config(self, guild_id: int, config: AutoPublishConfig) -> None:
        await self.bot.api.set_guild_config(guild_id, "autopub", config.json())

        self._cache[guild_id] = config

    @slash_command(name="publish")
    @has_guild_permissions(manage_guild=True)
    async def publish(
        self,
        ctx: ApplicationCommandInteraction,
        channel: NewsChannel = Param(
            desc="The channel to automatically publish messages in"
        ),
    ) -> None:
        """Automatically publish all new messages in an announcement channel."""

        assert ctx.guild

        gconf = await self.get_config(ctx.guild.id)
        cid = str(channel.id)

        if cid in gconf.channels:
            await ctx.send("That channel is already automatically published.", ephemeral=True)
            return

        gconf.channels.append(cid)

        await self.set_config(ctx.guild.id, gconf)

        await ctx.send(f"I will now automatically publish messages in {channel.mention}", ephemeral=True)

    @slash_command(name="unpublish")
    @has_guild_permissions(manage_guild=True)
    async def unpublish(
        self,
        ctx: ApplicationCommandInteraction,
        channel: NewsChannel = Param(
            desc="The channel to no longer automatically publish messages in"
        ),
    ) -> None:
        """Stop automatically publishing all new messages in an announcement channel."""

        assert ctx.guild

        gconf = await self.get_config(ctx.guild.id)
        cid = str(channel.id)

        if cid not in gconf.channels:
            await ctx.send("That channel is not automatically published.", ephemeral=True)
            return

        gconf.channels.remove(cid)

        await self.set_config(ctx.guild.id, gconf)

        await ctx.send(f"I will no longer automatically publish messages in {channel.mention}", ephemeral=True)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.guild:
            return

        if message.channel.type != ChannelType.news:
            return

        gconf = await self.get_config(message.guild.id)

        if not gconf.channels:
            return

        if message.author.id == self.bot.user.id:
            return

        if str(message.channel.id) in gconf.channels:
            await message.publish()


def setup(bot: Bot) -> None:
    bot.add_cog(Publish(bot))

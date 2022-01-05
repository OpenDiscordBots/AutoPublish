from os import environ
from traceback import format_exc
from typing import List

from disnake.ext.commands import Bot as _Bot
from libodb import APIClient
from loguru import logger


class Bot(_Bot):
    """A subclass of `disnake.ext.commands.Bot` to add functionality."""

    def __init__(self, api: APIClient = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.api = api or APIClient(environ["API_TOKEN"])

    def load_extensions(self, exts: List[str]) -> None:
        ld = 0

        for ext in exts:
            try:
                self.load_extension(ext)
                logger.info(f"Successfully loaded extension {ext}")
                ld += 1
            except Exception as e:
                logger.error(
                    f"Error occurred while loading extension {ext}: {e}\n{format_exc()}"
                )

        logger.info(
            f"Extension loading complete. {ld} extensions loaded, {len(exts) - ld} failed."
        )

    async def on_ready(self) -> None:
        logger.info(f"Bot is ready. Connected to {len(self.guilds)} guilds.")

    @staticmethod
    async def on_connect() -> None:
        logger.info("Bot is connected to the gateway.")

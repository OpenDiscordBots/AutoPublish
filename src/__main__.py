from os import environ as env

from dotenv import load_dotenv

from src.bot import Bot

load_dotenv()


def main() -> None:
    bot = Bot(command_prefix="ap!")
    bot.load_extensions(
        [
            "src.exts.ping",
            "src.exts.publish",
        ]
    )

    bot.run(env["TOKEN"])


if __name__ == "__main__":
    main()

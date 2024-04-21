from aiogram import Bot

from telegram_bot.config import Config


def create_bot(config: Config) -> Bot:
    return Bot(token=config.common.bot_token.get_secret_value())

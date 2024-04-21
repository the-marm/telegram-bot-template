from typing import TYPE_CHECKING

from telegram_bot.factories.config import create_config

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

    from telegram_bot.config import Config

from telegram_bot.factories.bot import create_bot
from telegram_bot.factories.dispatcher import create_dispatcher
from telegram_bot.runners import run_polling, run_webhook
from telegram_bot.utils.loggers import setup_logger


def main() -> None:
    setup_logger()

    config: Config = create_config()

    dispatcher: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)

    if config.webhook.use:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot)


try:
    main()
except Exception:
    import traceback

    traceback.print_exc()
    # raise NotImplementedError from error
finally:
    ...
    # raise NotImplementedError

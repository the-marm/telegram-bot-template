from aiogram import Router

from telegram_bot.handlers.extra import errors

router = Router(name=__name__)
router.include_router(errors.router)

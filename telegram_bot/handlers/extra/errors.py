from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n.context import I18nContext

from telegram_bot.exceptions import BotError

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent, i18n: I18nContext) -> None:
    if error.update.message:
        await error.update.message.answer(
            text=i18n.messages.somethings_went_wrong(),
        )

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n.context import I18nContext

from telegram_bot.keyboards.reply.menu import main
from telegram_bot.services.database.models import DBUser

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(
    message: Message, i18n: I18nContext, user: DBUser,
) -> None:
    await message.answer(
        text=i18n.messages.start(name=user.first_name),
        reply_markup=main(i18n_context=i18n),
    )

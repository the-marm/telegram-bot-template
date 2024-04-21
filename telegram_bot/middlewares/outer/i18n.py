from typing import Self, cast

from aiogram.types import User
from aiogram_i18n.managers import BaseManager

from telegram_bot.services.database import UoW
from telegram_bot.services.database.models import BotUser


class UserManager(BaseManager):
    async def get_locale(
        self: Self,
        event_from_user: User | None = None,
        user: BotUser | None = None,
    ) -> str:
        if user:
            return user.locale
        if event_from_user and event_from_user.language_code is not None:
            return event_from_user.language_code
        return cast(str, self.default_locale)

    async def set_locale(
        self: Self, locale: str, user: BotUser, uow: UoW,
    ) -> None:
        user.locale = locale
        await uow.commit(user)

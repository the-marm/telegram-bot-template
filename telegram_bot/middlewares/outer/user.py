from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User
from aiogram_i18n import I18nMiddleware

from telegram_bot.services.database.models import DBUser
from telegram_bot.utils.loggers import database as logger

if TYPE_CHECKING:

    from telegram_bot.services.database import UoW
    from telegram_bot.services.database.repositories import Repository


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any | None:
        aiogram_user: User | None = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")

        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)

        repository: Repository = data["repository"]
        user: DBUser | None = await repository.users.get(
            telegram_user_id=aiogram_user.id,
        )

        if user:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = self._update_user_profile(
                user=user, aiogram_user=aiogram_user, i18n=i18n,
            )
            await uow.commit(user)

        if not user:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = DBUser.from_aiogram(
                aiogram_user=aiogram_user,
                locale=self._get_user_locale(aiogram_user=aiogram_user, i18n=i18n),
            )
            await uow.commit(user)

            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )


        data["user"] = user

        return await handler(event, data)

    def _update_user_profile(
        self, user: DBUser, aiogram_user: User, i18n: I18nMiddleware,
    ) -> DBUser:
        if user.first_name != aiogram_user.first_name:
            user.first_name = aiogram_user.first_name
        elif user.last_name != aiogram_user.last_name:
            user.last_name = aiogram_user.last_name
        elif user.locale != aiogram_user.language_code:
            user.locale = self._get_user_locale(aiogram_user=aiogram_user, i18n=i18n)
        return user

    def _get_user_locale(self, aiogram_user: User, i18n: I18nMiddleware) -> str:
        return (aiogram_user.language_code
                if aiogram_user.language_code
                in i18n.core.available_locales
                else cast(str, i18n.core.default_locale)
                )


from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User

from telegram_bot.services.database.models import BotUser
from telegram_bot.utils.loggers import database as logger

if TYPE_CHECKING:
    from aiogram_i18n import I18nMiddleware

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
        user: BotUser | None = await repository.users.get(
            telegram_user_id=aiogram_user.id,
        )

        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            uow: UoW = data["uow"]
            user = BotUser.from_aiogram(
                aiogram_user=aiogram_user,
                locale=(
                    aiogram_user.language_code
                    if aiogram_user.language_code
                    in i18n.core.available_locales
                    else cast(str, i18n.core.default_locale)
                ),
            )
            await uow.commit(user)

            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user

        return await handler(event, data)

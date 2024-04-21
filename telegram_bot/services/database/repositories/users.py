from typing import Self, cast

from sqlalchemy import select

from telegram_bot.services.database.models import BotUser
from telegram_bot.services.database.repositories import BaseRepository


class UsersRepository(BaseRepository):
    async def get(self: Self, telegram_user_id: int) -> BotUser | None:
        return cast(
            BotUser | None,
            await self._session.scalar(
                select(BotUser).where(
                    BotUser.telegram_user_id == telegram_user_id,
                ),
            ),
        )

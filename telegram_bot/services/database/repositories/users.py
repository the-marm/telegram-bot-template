from typing import cast

from sqlalchemy import select

from telegram_bot.services.database.models import DBUser
from telegram_bot.services.database.repositories import BaseRepository


class UsersRepository(BaseRepository):
    async def get(self, telegram_user_id: int) -> DBUser | None:
        return cast(
            DBUser | None,
            await self._session.scalar(
                select(DBUser).where(
                    DBUser.telegram_user_id == telegram_user_id,
                ),
            ),
        )

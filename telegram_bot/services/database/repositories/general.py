from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .users import UsersRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    users: UsersRepository

    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.users = UsersRepository(session=session)

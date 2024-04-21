from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    _session: AsyncSession

    def __init__(self: Self, session: AsyncSession) -> None:
        self._session = session

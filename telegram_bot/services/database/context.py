import asyncio
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .repositories.general import Repository
from .uow import UoW


class SQLSessionContext:
    _session_pool: async_sessionmaker[AsyncSession]
    _session: AsyncSession | None

    def __init__(
        self: Self, session_pool: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_pool = session_pool
        self._session = None

    async def __aenter__(self: Self) -> tuple[Repository, UoW]:
        self._session: AsyncSession | None = (
            await self._session_pool().__aenter__()
        )
        return Repository(session=self._session), UoW(session=self._session)

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._session is None:
            return
        task: asyncio.Task[None] = asyncio.create_task(self._session.close())
        await asyncio.shield(task)
        self._session = None

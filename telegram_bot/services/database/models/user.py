from typing import Self

from aiogram.types import User
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    telegram_user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=False,
    )
    username: Mapped[str | None] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str] = mapped_column(String(68))
    last_name: Mapped[str | None] = mapped_column(String(68), nullable=True)
    locale: Mapped[str] = mapped_column(String(2), nullable=False)

    @classmethod
    def from_aiogram(cls, aiogram_user: User, locale: str) -> Self:
        return cls(
            telegram_user_id=aiogram_user.id,
            username=aiogram_user.username,
            first_name=aiogram_user.first_name,
            last_name=aiogram_user.last_name,
            locale=locale,
        )

    def __repr__(self: Self) -> str:
        return (
            f"<User "
            f"{self.telegram_user_id}"
            f"{self.username}"
            f"{self.first_name}"
            f"{self.last_name}"
            ">"
        )

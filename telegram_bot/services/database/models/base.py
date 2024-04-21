from datetime import datetime
from typing import Annotated

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import func

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(),
    )

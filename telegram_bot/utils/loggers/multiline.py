from collections.abc import Iterable
from logging import INFO, Logger, getLogger
from typing import Self


class MultilineLogger:
    level: int
    logger: Logger

    __slots__ = ("level", "logger")

    def __init__(
        self: Self, level: int = INFO, logger: Logger | None = None,
    ) -> None:
        self.level = level
        self.logger = logger or getLogger()

    def __call__(self: Self, message: Iterable[str]) -> None:
        if isinstance(message, str):
            message = message.splitlines()
        for line in message:
            self.logger.log(level=self.level, msg=line)

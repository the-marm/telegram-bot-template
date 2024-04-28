from telegram_bot.config import (
    CommonConfig,
    Config,
    PostgresConfig,
    RedisConfig,
    WebhookConfig,
)


def create_config() -> Config:
    return Config(
        common=CommonConfig(),  # pyright: ignore[reportCallIssue]
        postgres=PostgresConfig(),  # pyright: ignore[reportCallIssue]
        redis=RedisConfig(),  # pyright: ignore[reportCallIssue]
        webhook=WebhookConfig(),  # pyright: ignore[reportCallIssue]
    )

from telegram_bot.config import (
    CommonConfig,
    Config,
    PostgresConfig,
    RedisConfig,
    WebhookConfig,
)


def create_config() -> Config:
    return Config(
        common=CommonConfig(),
        postgres=PostgresConfig(),
        redis=RedisConfig(),
        webhook=WebhookConfig(),
    )

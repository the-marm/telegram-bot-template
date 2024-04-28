"""Telegram Bot Configuration Module.

This module provides a structured approach to managing configuration settings
for a Telegram bot application.

It utilizes the `pydantic` and `pydantic-settings` libraries to define and validate
configuration values, and supports reading settings from environment variables
and a `.env` file.

**Key Features:**

- Model-based configuration:
    Settings are defined using Pydantic models, ensuring type safety and validation.
- Environment variable support:
    Configuration values can be read from environment variables prefixed with the
    specified prefix.
- Dotenv support:
    Settings can be loaded from a `.env` file located in the project root directory.
- Sub-configurations:
    Complex configurations can be organized into nested sub-configurations.
- Secret handling:
    Sensitive values like passwords can be stored as secrets using Pydantic's
    `SecretStr` field.

**Example Usage:**

```python
from telegram_bot.config import (
    CommonConfig,
    Config,
    PostgresConfig,
    RedisConfig,
    WebhookConfig,
)


config: Config = Config()

config = Config(
    common=CommonConfig(),
    postgres=PostgresConfig(),
    redis=RedisConfig(),
    webhook=WebhookConfig(),
)

print(config.common.bot_token)
"""

from secrets import token_urlsafe

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    """Base class for configuration settings.

    Inherits from `pydantic_settings.BaseSettings`.
    Defines global configuration for reading environment variables
    and ignoring extra fields in the configuration model.
    """

    model_config = SettingsConfigDict(
        extra="ignore", env_file="telegram_bot/.env",
    )


class CommonConfig(BaseSettings, env_prefix="COMMON_"):
    """Common configuration settings for the Telegram bot application.

    Defines settings related to the bot itself, such as the bot token,
    update management, logging, and admin chat ID.
    Uses the `COMMON_` prefix for environment variables.
    """

    bot_token: SecretStr
    drop_pending_updates: bool
    sqlalchemy_logging: bool
    admin_chat_id: int


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    """PostgreSQL database configuration.

    Defines connection details for the PostgreSQL database used by the application.
    Uses the `POSTGRES_` prefix for environment variables.
    """

    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    def build_dsn(self) -> URL:
        """Construct a SQLAlchemy URL object from the configuration.

        Returns
        -------
            URL: A SQLAlchemy URL object representing the PostgreSQL connection.

        """
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    """Redis configuration.

    Defines connection details for the Redis server used by the application.
    Uses the `REDIS_` prefix for environment variables.
    """

    host: str
    port: int
    db: int
    data: str


class WebhookConfig(BaseSettings, env_prefix="WEBHOOK_"):
    """Webhook configuration.

    Defines settings for running the bot in webhook mode.
    Uses the `WEBHOOK_` prefix for environment variables.
    """

    use: bool
    reset: bool
    base_url: str
    path: str
    port: int
    host: str
    secret_token: SecretStr = Field(default_factory=token_urlsafe)

    def build_url(self) -> str:
        """Construct the complete webhook URL.

        Returns
        -------
            str: The full webhook URL concatenating base URL and path.

        """
        return f"{self.base_url}{self.path}"


class Config(BaseModel):
    """Combined configuration object."""

    common: CommonConfig
    postgres: PostgresConfig
    redis: RedisConfig
    webhook: WebhookConfig

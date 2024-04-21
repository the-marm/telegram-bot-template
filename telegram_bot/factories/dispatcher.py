from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from redis.asyncio import ConnectionPool, Redis

from telegram_bot.config import Config
from telegram_bot.enums import Locale
from telegram_bot.handlers import admin, common, extra
from telegram_bot.middlewares.outer.database import DBSessionMiddleware
from telegram_bot.middlewares.outer.i18n import UserManager
from telegram_bot.middlewares.outer.user import UserMiddleware
from telegram_bot.services.database.create_pool import create_pool


def _setup_outer_middlewares(dispatcher: Dispatcher, config: Config) -> None:
    pool = dispatcher["session_pool"] = create_pool(
        dsn=config.postgres.build_dsn(),
        enable_logging=config.common.sqlalchemy_logging,
    )
    i18n_middleware = dispatcher["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(
            path="telegram_bot/locales/{locale}",
            raise_key_error=False,
        ),
        manager=UserManager(),
        default_locale=Locale.DEFAULT,
    )
    dispatcher.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dispatcher.update.outer_middleware(UserMiddleware())
    i18n_middleware.setup(dispatcher=dispatcher)


def create_dispatcher(config: Config) -> Dispatcher:
    redis = Redis(
        connection_pool=ConnectionPool(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        ),
    )
    dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis),
        config=config,
    )

    dispatcher.include_routers(admin.router, common.router, extra.router)

    _setup_outer_middlewares(dispatcher=dispatcher, config=config)

    return dispatcher

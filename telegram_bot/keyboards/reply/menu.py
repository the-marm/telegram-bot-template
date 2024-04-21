from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram_i18n import I18nContext


def main(i18n_context: I18nContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=i18n_context.button()),
            ],
        ],
    )

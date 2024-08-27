from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import ABOUT_CATEGORIES, DESIGN_PROJECT, ABOUT_US, PORTFOLIO, GO_BACK


def info_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=ABOUT_CATEGORIES)
    keyboard.button(text=DESIGN_PROJECT)
    keyboard.button(text=ABOUT_US)
    keyboard.button(text=PORTFOLIO)
    keyboard.button(text=GO_BACK)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

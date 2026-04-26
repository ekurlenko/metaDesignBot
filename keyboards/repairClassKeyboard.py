from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import COMFORT, BUSINESS, ABOUT_CATEGORIES


def repair_class_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=COMFORT)
    keyboard.button(text=BUSINESS)
    keyboard.button(text=ABOUT_CATEGORIES)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

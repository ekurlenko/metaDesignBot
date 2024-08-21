from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import MORE_INFO, CALCULATE_COST


def start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=CALCULATE_COST)
    keyboard.button(text=MORE_INFO)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

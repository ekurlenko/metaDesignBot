from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import GO_BACK, CALCULATE_COST, NEXT


def portfolio_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=NEXT)
    keyboard.button(text=GO_BACK)
    keyboard.button(text=CALCULATE_COST)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
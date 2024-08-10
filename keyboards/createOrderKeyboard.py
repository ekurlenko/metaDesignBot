from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import CREATE_ORDER


def create_order_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=CREATE_ORDER)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Отправить свой номер телефона", request_contact=True)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
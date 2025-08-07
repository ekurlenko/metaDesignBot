import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from handlers import bot

from keyboards.calculateOrMenuKeyboard import calculate_or_menu_keyboard

from misc.files import get_photo_from_dir
from misc.consts import DESIGN_PROJECT, ABOUT_DESIGN_PROJECT

router = Router()


@router.message(F.text == DESIGN_PROJECT)
async def design_project(message: Message):
    media = MediaGroupBuilder()

    for file in get_photo_from_dir("section3"):
        ph = FSInputFile(os.path.abspath(file))
        media.add_photo(media=ph)

    await bot.send_chat_action(message.chat.id, action="typing", request_timeout=7)
    await bot.send_media_group(message.chat.id, media=media.build(), )

    await message.answer(text=ABOUT_DESIGN_PROJECT,
                         parse_mode=ParseMode.HTML,
                         reply_markup=calculate_or_menu_keyboard())

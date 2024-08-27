import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from handlers import bot

from keyboards.calculateOrMenuKeyboard import calculate_or_menu_keyboard

from misc.files import get_photo_from_dir
from misc.consts import ABOUT_US, ABOUT_COMPANY

router = Router()


@router.message(F.text == ABOUT_US)
async def about_us(message: Message):
    media = MediaGroupBuilder()

    for file in get_photo_from_dir("section4"):
        ph = FSInputFile(os.path.abspath(file))
        media.add_photo(media=ph)

    await bot.send_media_group(message.chat.id, media=media.build(), )

    await message.answer(text=ABOUT_COMPANY,
                         parse_mode=ParseMode.HTML,
                         reply_markup=calculate_or_menu_keyboard())

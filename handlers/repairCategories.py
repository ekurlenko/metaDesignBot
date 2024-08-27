import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from handlers import bot

from keyboards.calculateOrMenuKeyboard import calculate_or_menu_keyboard

from misc.files import get_photo_from_dir
from misc.consts import ABOUT_CATEGORIES, FIRST_ABOUT_CATEGORIES, SECOND_ABOUT_CATEGORIES

router = Router()


@router.message(F.text == ABOUT_CATEGORIES)
async def about_repair_categories(message: Message):
    media = MediaGroupBuilder(caption=FIRST_ABOUT_CATEGORIES)

    for file in get_photo_from_dir("section2"):
        ph = FSInputFile(os.path.abspath(file))
        media.add_photo(media=ph)

    await bot.send_media_group(message.chat.id, media=media.build(), )

    await message.answer(text=SECOND_ABOUT_CATEGORIES,
                         parse_mode=ParseMode.HTML,
                         reply_markup=calculate_or_menu_keyboard())

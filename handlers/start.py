import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from handlers import bot

from keyboards.startKeyboard import start_keyboard

from misc.files import get_photo_from_dir
from misc.consts import FIRST_START_MESSAGE, SECOND_START_MESSAGE, MAIN_MENU, GO_BACK


router = Router()


@router.message(Command("start"))
@router.message(F.text == MAIN_MENU)
@router.message(F.text == GO_BACK)
async def start(message: Message):
    media = MediaGroupBuilder(caption=FIRST_START_MESSAGE)

    for file in get_photo_from_dir("section1"):
        ph = FSInputFile(os.path.abspath(file))
        media.add_photo(media=ph)

    await bot.send_media_group(message.chat.id, media=media.build(), )

    await message.answer(text=SECOND_START_MESSAGE,
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_keyboard())

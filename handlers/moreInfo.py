from aiogram import Router, F
from aiogram.types import Message

from keyboards.infoKeyboard import info_keyboard

from misc.consts import MORE_INFO

router = Router()


@router.message(F.text == MORE_INFO)
async def more_info(message: Message):
    await message.answer(text="Выбeрите кнопку ниже:",
                         reply_markup=info_keyboard())

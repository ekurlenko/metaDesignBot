from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from handlers import bot
from keyboards.portfolioKeyboard import portfolio_keyboard
from keyboards.calculateOrMenuKeyboard import calculate_or_menu_keyboard

from misc.consts import PORTFOLIO, CASES, NEXT
from misc.files import get_photo_for_portfolio

router = Router()


@router.message(F.text == PORTFOLIO)
@router.message(F.text == NEXT)
async def portfolio(message: Message, state: FSMContext):
    photos = get_photo_for_portfolio()
    data = await state.get_data()
    media = MediaGroupBuilder()
    ind = int(data.get('ind') or 0)
    try:
        if message.text == NEXT:
            if ind >= len(photos) - 1:
                await state.update_data(ind=0)
                for file in photos[ind]:
                    ph = FSInputFile(file)
                    media.add_photo(media=ph)
                await bot.send_media_group(message.chat.id, media=media.build(), )
                await message.answer(text=CASES[ind],
                                     reply_markup=calculate_or_menu_keyboard())
            else:
                for file in photos[ind]:
                    ph = FSInputFile(file)
                    media.add_photo(media=ph)
                await bot.send_media_group(message.chat.id, media=media.build(), )
                await message.answer(text=CASES[ind],
                                     reply_markup=portfolio_keyboard())

                await state.update_data(ind=ind + 1)

        else:
            if ind >= len(photos) - 1:
                await state.update_data(ind=0)
            for file in photos[ind]:
                ph = FSInputFile(file)
                media.add_photo(media=ph)
            await bot.send_media_group(message.chat.id, media=media.build(), )
            await message.answer(text=CASES[ind],
                                 reply_markup=portfolio_keyboard())
            await state.update_data(ind=ind + 1)
    except TypeError:
        await state.update_data(ind=0)
        for file in photos[ind]:
            ph = FSInputFile(file)
            media.add_photo(media=ph)
        await bot.send_media_group(message.chat.id, media=media.build(), )

        await message.answer(text=CASES[ind],
                             reply_markup=calculate_or_menu_keyboard())

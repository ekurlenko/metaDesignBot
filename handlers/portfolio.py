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
    try:
        if message.text == NEXT:
            if data.get('ind') >= len(photos) - 1:
                await state.update_data(ind=0)
                media = MediaGroupBuilder()
                for file in photos[data.get('ind')]:
                    ph = FSInputFile(file)
                    media.add_photo(media=ph)
                await bot.send_media_group(message.chat.id, media=media.build(), )

                await message.answer(text=CASES[data.get('ind')],
                                     reply_markup=calculate_or_menu_keyboard())
            else:
                media = MediaGroupBuilder()
                for file in photos[data.get('ind')]:
                    ph = FSInputFile(file)
                    media.add_photo(media=ph)
                await bot.send_media_group(message.chat.id, media=media.build(), )

                await message.answer(text=CASES[data.get('ind')],
                                     reply_markup=portfolio_keyboard())

                await state.update_data(ind=data.get('ind') + 1)

        else:
            if data.get('ind') >= len(photos) - 1:
                await state.update_data(ind=0)
            media = MediaGroupBuilder()
            for file in photos[data.get('ind')]:
                ph = FSInputFile(file)
                media.add_photo(media=ph)
            await bot.send_media_group(message.chat.id, media=media.build(), )

            await message.answer(text=CASES[data.get('ind')],
                                 reply_markup=portfolio_keyboard())

            await state.update_data(ind=data.get('ind') + 1)
    except TypeError:
        await state.update_data(ind=0)
        media = MediaGroupBuilder()
        for file in photos[data.get('ind')]:
            ph = FSInputFile(file)
            media.add_photo(media=ph)
        await bot.send_media_group(message.chat.id, media=media.build(), )

        await message.answer(text=CASES[data.get('ind')],
                             reply_markup=calculate_or_menu_keyboard())

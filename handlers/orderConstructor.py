import os

import peewee
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from dataBase.repositories.order import OrderRepository
from dataBase.repositories.realty_type import RealtyTypeRepository
from dataBase.repositories.realty_type_status import RealtyStatusTypeRepository
from dataBase.repositories.repair_type import RepairTypeRepository
from dataBase.repositories.user import UserRepository
from handlers import bot
from keyboards.createOrderKeyboard import create_order_keyboard
from keyboards.phoneKeyboard import get_phone_keyboard
from keyboards.propertyTypeKeyboard import type_of_property_keyboard
from keyboards.repairClassKeyboard import repair_class_keyboard
from keyboards.roomTypeKeyboard import room_type_keyboard
from misc.consts import *
from misc.files import get_photo_from_dir
from misc.utils import phone_parse, cost_calculator, ru_to_en_translate
from states import OrderConfigure

router = Router()


@router.message(F.text == CREATE_ORDER)
@router.message(F.text == CALCULATE_COST)
async def start(message: Message, state: FSMContext):
    await message.answer("Какой у вас тип недвижимости?",
                         reply_markup=type_of_property_keyboard())
    await state.set_state(OrderConfigure.square)


@router.message(OrderConfigure.square)
async def square(message: Message, state: FSMContext):
    await state.update_data(first_name=message.chat.first_name,
                            chat_id=message.chat.id,
                            realty_type=message.text,
                            username=message.from_user.username)
    await message.answer("Укажите площадь вашего объекта")
    await state.set_state(OrderConfigure.room_type)


@router.message(OrderConfigure.room_type)
async def room_type(message: Message, state: FSMContext):
    try:
        room_square = abs(float(message.text.replace(',', '.').replace(' ', '')))
        if room_square % 1 == 0:
            room_square = int(room_square)
        await state.update_data(square=room_square)
        await state.set_state(OrderConfigure.repair_class)
        await message.answer("Какой у вас тип помещения?",
                             reply_markup=room_type_keyboard())
    except ValueError:
        await message.answer("Введите площадь в формате: 25.45 ")
        await state.set_state(OrderConfigure.room_type)


@router.message(OrderConfigure.repair_class)
async def repair_class(message: Message, state: FSMContext):
    await state.update_data(realty_status_type=message.text)
    await message.answer("Какая категория ремонта вам ближе?",
                         reply_markup=repair_class_keyboard())
    await state.set_state(OrderConfigure.phone)


@router.message(OrderConfigure.phone)
async def phone(message: Message, state: FSMContext):
    if message.text == "Подробнее о категориях ремонта":
        media = MediaGroupBuilder(caption=FIRST_ABOUT_CATEGORIES)

        for file in get_photo_from_dir("section2"):
            ph = FSInputFile(os.path.abspath(file))
            media.add_photo(media=ph)

        await bot.send_media_group(message.chat.id, media=media.build(), )

        await message.answer(text=SECOND_ABOUT_CATEGORIES,
                             parse_mode=ParseMode.HTML)
        await message.answer("Какая категория ремонта вам ближе?",
                             reply_markup=repair_class_keyboard())
        await state.set_state(OrderConfigure.phone)
    else:
        await state.update_data(repair_type=message.text)
        await message.answer("Ваш расчет готов! Нажмите на кнопку ниже, чтобы увидеть результат\n",
                             reply_markup=get_phone_keyboard())
        await state.set_state(OrderConfigure.confirm)


@router.message(OrderConfigure.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.contact is not None:
        await state.update_data(phone=phone_parse(message.contact.phone_number))
        data = await state.get_data()
        try:
            with UserRepository() as user_repo:
                user = user_repo.create(data=data)
        except peewee.IntegrityError:
            with UserRepository() as user_repo:
                user = user_repo.get_by_phone(data['phone'])
                if not user.chat_id:
                    user_repo.update_chat_id(user, data['chat_id'])


        name = ru_to_en_translate(data.get('realty_type'))
        with RealtyTypeRepository() as realty_type_repo:
            realty_type = realty_type_repo.find_by_name(name=name)

        name = ru_to_en_translate(data.get('realty_status_type'))
        with RealtyStatusTypeRepository() as realty_status_type_repo:
            realty_status_type = realty_status_type_repo.find_by_name(name=name)

        name = ru_to_en_translate(data.get('repair_type'))
        with RepairTypeRepository() as repair_type_repo:
            repair_type = repair_type_repo.find_by_name(name=name)

        order_data = {
            'user_id': user,
            'realty_type_id': realty_type,
            'realty_status_type_id': realty_status_type,
            'repair_type_id': repair_type,
            'square': float(data.get('square')),
            'cost': cost_calculator(data)
        }
        with OrderRepository() as order_repo:
            order = order_repo.create(order_data)


        #





        if data.get('realty_type') == FLAT:
            await message.answer(f"Тип недвижимости: {data.get('realty_type')}\n"
                                 f"Площадь помещения: {data.get('square')}\n"
                                 f"Тип помещения: {data.get('realty_status_type')}\n"
                                 f"Класс ремонта: {data.get('repair_type')}\n"
                                 f"Номер телефона для связи: +7{data.get('phone')}\n"
                                 f"Стоимость ремонта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.")

            await message.answer("Заявка принята, спасибо за обращение! Мы с Вами свяжемся в течение 15 минут.\n"
                                 "Если хотите оставить еще одну заявку, нажмите кнопку ниже",
                                 reply_markup=create_order_keyboard())

            await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Заказ_{order.id}\n"
                                                                          f"#Клиент_{data.get('phone')}\n"
                                                                          f"Тип недвижимости: {data.get('realty_type')}\n"
                                                                          f"Площадь помещения: {data.get('square')}\n"
                                                                          f"Тип помещения: {data.get('realty_status_type')}\n"
                                                                          f"Класс ремонта: {data.get('repair_type')}\n"
                                                                          f"Номер телефона для связи: +7{data.get('phone')}\n"
                                                                          f"Стоимость ремонта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.\n"
                                                                          f"@{data.get('user')}")

        else:
            await message.answer(f"Тип недвижимости: {data.get('realty_type')}\n"
                                 f"Площадь помещения: {data.get('square')}\n"
                                 f"Тип помещения: {data.get('realty_status_type')}\n"
                                 f"Класс ремонта: {data.get('repair_type')}\n"
                                 f"Номер телефона для связи: +7{data.get('phone')}\n"
                                 f"Стоимость дизайн-проекта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.")

            await message.answer("Заявка принята, спасибо за обращение!\n"
                                 "Расчет стоимости ремонта в выбранном типе недвижимости "
                                 "осуществляется в индивидуальном порядке.\n"
                                 "Мы с Вами свяжемся в течение 15 минут.")

            await message.answer("Если хотите оставить еще одну заявку, нажмите кнопку ниже",
                                 reply_markup=create_order_keyboard())

            await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Заказ_{order.id}\n"
                                                                          f"#Клиент_{data.get('phone')}\n"
                                                                          f"Тип недвижимости: {data.get('realty_type')}\n"
                                                                          f"Площадь помещения: {data.get('square')}\n"
                                                                          f"Тип помещения: {data.get('realty_status_type')}\n"
                                                                          f"Класс ремонта: {data.get('repair_type')}\n"
                                                                          f"Номер телефона для связи: +7{data.get('phone')}\n"
                                                                          f"Стоимость дизайн-проекта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.\n"
                                                                          f"@{data.get('user')}")

        await state.clear()
    else:
        await message.answer("Ваш расчет готов! Нажмите кнопку ниже, чтобы увидеть результат\n",
                             reply_markup=get_phone_keyboard())
        await state.set_state(OrderConfigure.confirm)

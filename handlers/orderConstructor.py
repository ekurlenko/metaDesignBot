from datetime import datetime

import peewee
import os

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.phoneKeyboard import get_phone_keyboard
from keyboards.roomTypeKeyboard import room_type_keyboard
from keyboards.repairClassKeyboard import repair_class_keyboard
from keyboards.createOrderKeyboard import create_order_keyboard
from keyboards.propertyTypeKeyboard import type_of_property_keyboard

from states import OrderConfigure

from dataBase.models.UserModel import UserModel
from dataBase.models.OrderModel import OrderModel
from dataBase.models.RoomTypeModel import RoomTypeModel
from dataBase.models.PropertyTypeModel import PropertyTypeModel
from dataBase.models.RepairClassModel import RepairClassModel

from handlers import bot

from misc.consts import *
from misc.files import get_photo_from_dir
from misc.utils import phone_parse, cost_calculator, ru_to_en_translate

router = Router()


@router.message(F.text == CREATE_ORDER)
@router.message(F.text == CALCULATE_COST)
async def start(message: Message, state: FSMContext):
    await message.answer("Какой у вас тип недвижимости?",
                         reply_markup=type_of_property_keyboard())
    await state.set_state(OrderConfigure.square)


@router.message(OrderConfigure.square)
async def square(message: Message, state: FSMContext):
    await state.update_data(name=message.chat.first_name,
                            chat_id=message.chat.id,
                            property_type=message.text,
                            user=message.from_user.username)
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
    await state.update_data(room_type=message.text)
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
        await state.update_data(repair_class=message.text)
        await message.answer("Ваш расчет готов! Нажмите на кнопку ниже, чтобы увидеть результат\n",
                             reply_markup=get_phone_keyboard())
        await state.set_state(OrderConfigure.confirm)


@router.message(OrderConfigure.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.contact is not None:
        await state.update_data(phone=phone_parse(message.contact.phone_number))
        data = await state.get_data()
        try:
            user = await UserModel.aio_create(chat_id=data.get('chat_id'),
                                              first_name=data.get('name'),
                                              phone_number=data.get('phone'))
        except peewee.IntegrityError:
            user = await UserModel.aio_get(UserModel.chat_id == data.get('chat_id'))

        property_type = await PropertyTypeModel.aio_get(PropertyTypeModel.name == ru_to_en_translate(data.get('property_type')))
        room_type = await RoomTypeModel.aio_get(RoomTypeModel.name == ru_to_en_translate(data.get('room_type')))
        repair_class = await RepairClassModel.aio_get(RepairClassModel.name == ru_to_en_translate(data.get('repair_class')))

        order = await OrderModel.aio_create(user_id=user,
                                            property_type=property_type,
                                            square=float(data.get('square')),
                                            room_type=room_type,
                                            repair_class=repair_class,
                                            cost=cost_calculator(data),
                                            done_at=datetime.now())
        #



        if data.get('property_type') == FLAT:
            await message.answer(f"Тип недвижимости: {data.get('property_type')}\n"
                                 f"Площадь помещения: {data.get('square')}\n"
                                 f"Тип помещения: {data.get('room_type')}\n"
                                 f"Класс ремонта: {data.get('repair_class')}\n"
                                 f"Номер телефона для связи: +7{data.get('phone')}\n"
                                 f"Стоимость ремонта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.")

            await message.answer("Заявка принята, спасибо за обращение! Мы с Вами свяжемся в течение 15 минут.\n"
                                 "Если хотите оставить еще одну заявку, нажмите кнопку ниже",
                                 reply_markup=create_order_keyboard())

            await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Заказ_{order.id}\n"
                                                                          f"#Клиент_{data.get('phone')}\n"
                                                                          f"Тип недвижимости: {data.get('property_type')}\n"
                                                                          f"Площадь помещения: {data.get('square')}\n"
                                                                          f"Тип помещения: {data.get('room_type')}\n"
                                                                          f"Класс ремонта: {data.get('repair_class')}\n"
                                                                          f"Номер телефона для связи: +7{data.get('phone')}\n"
                                                                          f"Стоимость ремонта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.\n"
                                                                          f"@{data.get('user')}")

        else:
            await message.answer(f"Тип недвижимости: {data.get('property_type')}\n"
                                 f"Площадь помещения: {data.get('square')}\n"
                                 f"Тип помещения: {data.get('room_type')}\n"
                                 f"Класс ремонта: {data.get('repair_class')}\n"
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
                                                                          f"Тип недвижимости: {data.get('property_type')}\n"
                                                                          f"Площадь помещения: {data.get('square')}\n"
                                                                          f"Тип помещения: {data.get('room_type')}\n"
                                                                          f"Класс ремонта: {data.get('repair_class')}\n"
                                                                          f"Номер телефона для связи: +7{data.get('phone')}\n"
                                                                          f"Стоимость дизайн-проекта: от {'{0:,}'.format(cost_calculator(data)).replace(',', ' ')} руб.\n"
                                                                          f"@{data.get('user')}")

        await state.clear()
    else:
        await message.answer("Ваш расчет готов! Нажмите кнопку ниже, чтобы увидеть результат\n",
                             reply_markup=get_phone_keyboard())
        await state.set_state(OrderConfigure.confirm)

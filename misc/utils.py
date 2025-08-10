import os

import peewee
import peewee_async
from aiogram import Bot
from datetime import datetime

from typing import Any, Dict

from dataBase.config import db
from dataBase.models.UserModel import UserModel
from dataBase.models.OrderModel import OrderModel
from dataBase.models.RealtyStatusTypeModel import RealtyStatusTypeModel
from dataBase.models.RealtyTypeModel import RealtyTypeModel
from dataBase.models.RepairTypeModel import RepairTypeModel
from dataBase.models.ServiceTypeModel import ServiceTypeModel
from dataBase.models.FeedbackModel import FeedbackModel



from misc.consts import COMFORT, BUSINESS, SECONDARY, FLAT, RU_EN_DICTIONARY, EN_RU_DICTIONARY


def phone_parse(x) -> str:
    s = str(x)
    phone = ''
    for i in s:
        if i.isdigit():
            phone += i
    phone = phone[-10:]
    return phone

def ru_to_en_translate(ru_word: str) -> str:
    return RU_EN_DICTIONARY.get(ru_word)

def en_to_ru_translate(en_word: str) -> str:
    return EN_RU_DICTIONARY.get(en_word)

def cost_calculator(data: Dict[str, Any]) -> int:
    square = data.get('square')
    realty_type = data.get('realty_type')
    repair_type = data.get('repair_type')
    realty_status_type = data.get('realty_status_type')

    cost = 0
    if realty_type == FLAT:

        if realty_status_type == SECONDARY:
            cost += 150 * 1000

        if square < 25:
            if repair_type == COMFORT:
                cost += 120 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 170 * 1000 * square
        elif square < 30:
            if repair_type == COMFORT:
                cost += 110 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 160 * 1000 * square
        elif square < 35:
            if repair_type == COMFORT:
                cost += 100 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 150 * 1000 * square
        elif square < 70:
            if repair_type == COMFORT:
                cost += 95 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 130 * 1000 * square
        elif square < 100:
            if repair_type == COMFORT:
                cost += 90 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 120 * 1000 * square
        else:
            if repair_type == COMFORT:
                cost += 85 * 1000 * square
            elif repair_type == BUSINESS:
                cost += 115 * 1000 * square
    else:
        if repair_type == COMFORT:
            cost += 4000 * square
        if repair_type == BUSINESS:
            cost += 6000 * square

    return int(cost)


async def pull_orders(bot: Bot):

    orders = await OrderModel.select().where(OrderModel.done_at == None).aio_execute()

    for order in orders:
        user = await UserModel.select().where(UserModel.id == order.user_id).aio_execute()
        property_type = await RealtyTypeModel.select().where(RealtyTypeModel.id == order.property_type_id).aio_execute()
        room_type = await RealtyStatusTypeModel.select().where(RealtyStatusTypeModel.id == order.room_type_id).aio_execute()
        repair_class = await RepairTypeModel.select().where(RepairTypeModel.id == order.repair_class_id).aio_execute()

        await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Заказ_{order.id}\n"
                                                                          f"#Клиент_{user[0].phone_number}\n"
                                                                          f"Тип недвижимости: {en_to_ru_translate(property_type[0].name)}\n"
                                                                          f"Площадь помещения: {int(order.square)}\n"
                                                                          f"Тип помещения: {en_to_ru_translate(room_type[0].name)}\n"
                                                                          f"Класс ремонта: {en_to_ru_translate(repair_class[0].name)}\n"
                                                                          f"Номер телефона для связи: +7{user[0].phone_number}\n"
                                                                          f"Стоимость ремонта: от {'{0:,}'.format(order.cost).replace(',', ' ')} руб.\n")

        order = await OrderModel.update(done_at=datetime.now()).aio_execute()


async def pull_feedbacks(bot: Bot):
    try:
        db.connect()
    except peewee.OperationalError:
        db.close()
        db.connect()

    feedbacks = await FeedbackModel.select().where(FeedbackModel.done_at == None).aio_execute()

    for feedback in feedbacks:
        user = await UserModel.select().where(UserModel.id == feedback.user_id).aio_execute()
        service_type = await ServiceTypeModel.select().where(ServiceTypeModel.id == feedback.service_type).aio_execute()

        await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Услуга_{feedback.id}\n"
                                                                          f"#Клиент_{user[0].phone_number}\n"
                                                                          f"{"Имя: " + user[0].first_name + "\n" if user[0].first_name else ""}"
                                                                          f"Тип услуги: {en_to_ru_translate(service_type[0].name)}\n"
                                                                          f"Удобные способы связи: "
                                                                          f"{"телеграмм, "if feedback.telegram else ''}"
                                                                          f"{"ватсап, "if feedback.whatsapp else ''}"
                                                                          f"{"телефонный звонок"if feedback.phone_call else ''}\n"
                                                                          f"Номер телефона для связи: +7{user[0].phone_number}\n")

        feedback = await FeedbackModel.update(done_at=datetime.now()).aio_execute()

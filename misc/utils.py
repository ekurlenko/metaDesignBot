import os
import peewee_async
from aiogram import Bot
from datetime import datetime

from typing import Any, Dict

from dataBase.models.UserModel import UserModel
from dataBase.models.OrderModel import OrderModel
from dataBase.models.RoomTypeModel import RoomTypeModel
from dataBase.models.PropertyTypeModel import PropertyTypeModel
from dataBase.models.RepairClassModel import RepairClassModel
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
    property_type = data.get('property_type')
    repair_class = data.get('repair_class')
    room_type = data.get('room_type')

    cost = 0
    if property_type == FLAT:

        if room_type == SECONDARY:
            cost += 150 * 1000

        if square < 25:
            if repair_class == COMFORT:
                cost += 120 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 170 * 1000 * square
        elif square < 30:
            if repair_class == COMFORT:
                cost += 110 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 160 * 1000 * square
        elif square < 35:
            if repair_class == COMFORT:
                cost += 100 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 150 * 1000 * square
        elif square < 70:
            if repair_class == COMFORT:
                cost += 95 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 130 * 1000 * square
        elif square < 100:
            if repair_class == COMFORT:
                cost += 90 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 120 * 1000 * square
        else:
            if repair_class == COMFORT:
                cost += 85 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 115 * 1000 * square
    else:
        if repair_class == COMFORT:
            cost += 4000 * square
        if repair_class == BUSINESS:
            cost += 6000 * square

    return int(cost)


async def pull_orders(bot: Bot):
    orders = await OrderModel.select().where(OrderModel.done_at == None).aio_execute()

    for order in orders:
        user = await UserModel.select().where(UserModel.id == order.user_id).aio_execute()
        property_type = await PropertyTypeModel.select().where(PropertyTypeModel.id == order.property_type_id).aio_execute()
        room_type = await RoomTypeModel.select().where(RoomTypeModel.id == order.room_type_id).aio_execute()
        repair_class = await RepairClassModel.select().where(RepairClassModel.id == order.repair_class_id).aio_execute()
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

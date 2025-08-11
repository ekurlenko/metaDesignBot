import os
from typing import Any, Dict

from aiogram import Bot

from dataBase.repositories.feedback import FeedbackRepository
from dataBase.repositories.order import OrderRepository
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
    with OrderRepository() as order_repo:
        orders = order_repo.get_not_done()

    for order in orders:
        user = order.user_id
        realty_type = order.realty_type
        realty_status_type = order.realty_status_type
        repair_type = order.repair_type

        await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Заказ_{order.id}\n"
                                                                      f"#Клиент_{user.phone_number}\n"
                                                                      f"Тип недвижимости: {en_to_ru_translate(realty_type.name)}\n"
                                                                      f"Площадь помещения: {int(order.square)}\n"
                                                                      f"Тип помещения: {en_to_ru_translate(realty_status_type.name)}\n"
                                                                      f"Класс ремонта: {en_to_ru_translate(repair_type.name)}\n"
                                                                      f"Номер телефона для связи: +7{user.phone_number}\n"
                                                                      f"Стоимость ремонта: от {'{0:,}'.format(order.cost).replace(',', ' ')} руб.\n")

        with OrderRepository() as order_repo:
            order_repo.update_done_at(order)


async def pull_feedbacks(bot: Bot):
    with FeedbackRepository() as feedback_repo:
        feedbacks = feedback_repo.get_not_done()

    for feedback in feedbacks:
        user = feedback.user_id
        service_type = feedback.service_type

        await bot.send_message(chat_id=os.getenv('TARGET_CHAT'), text=f"#Услуга_{feedback.id}\n"
                                                                      f"#Клиент_{user.phone_number}\n"
                                                                      f"{"Имя: " + user.first_name + "\n" if user.first_name else ""}"
                                                                      f"Тип услуги: {en_to_ru_translate(service_type.name)}\n"
                                                                      f"Удобные способы связи: "
                                                                      f"{"телеграмм, " if feedback.telegram else ''}"
                                                                      f"{"ватсап, " if feedback.whatsapp else ''}"
                                                                      f"{"телефонный звонок" if feedback.phone_call else ''}\n"
                                                                      f"Номер телефона для связи: +7{user.phone_number}\n")

        with FeedbackRepository() as feedback_repo:
            feedback_repo.update_done_at(feedback)

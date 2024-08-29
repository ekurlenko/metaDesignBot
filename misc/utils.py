from typing import Any, Dict

from misc.consts import COMFORT, BUSINESS, SECONDARY, FLAT


def phone_parse(x) -> str:
    s = str(x)
    phone = ''
    for i in s:
        if i.isdigit():
            phone += i
    phone = phone[-10:]
    return phone


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
        elif square < 65:
            if repair_class == COMFORT:
                cost += 100 * 1000 * square
            elif repair_class == BUSINESS:
                cost += 150 * 1000 * square
        elif square < 95:
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
                cost += 150 * 1000 * square
    else:
        cost += 4000 * square

    return int(cost)

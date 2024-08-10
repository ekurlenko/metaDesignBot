from typing import Any, Dict

from misc.consts import COMFORT, BUSINESS


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
    repair_class = data.get('repair_class')

    if square < 25:
        if repair_class == COMFORT:
            return 120 * 1000 * square
        elif repair_class == BUSINESS:
            return 170 * 1000 * square
    elif square < 30:
        if repair_class == COMFORT:
            return 110 * 1000 * square
        elif repair_class == BUSINESS:
            return 160 * 1000 * square
    elif square < 65:
        if repair_class == COMFORT:
            return 100 * 1000 * square
        elif repair_class == BUSINESS:
            return 150 * 1000 * square
    elif square < 95:
        if repair_class == COMFORT:
            return 95 * 1000 * square
        elif repair_class == BUSINESS:
            return 130 * 1000 * square
    elif square < 100:
        if repair_class == COMFORT:
            return 90 * 1000 * square
        elif repair_class == BUSINESS:
            return 120 * 1000 * square
    else:
        if repair_class == COMFORT:
            return 85 * 1000 * square
        elif repair_class == BUSINESS:
            return 150 * 1000 * square

from aiogram.fsm.state import State, StatesGroup


class OrderConfigure(StatesGroup):
    property_type = State()
    square = State()
    room_type = State()
    repair_class = State()
    phone = State()
    confirm = State()

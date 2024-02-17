from aiogram.fsm.state import StatesGroup, State


class CurrentLogic(StatesGroup):
    order_status = State()
    order_history = State()

from aiogram.fsm.state import StatesGroup, State


class CurrentLogic(StatesGroup):
    # for order_status
    order_status = State()
    order_history = State()

    # for input_order_number
    input_order_number = State()
    # sets when /start
    basic = State()

    # for loading_photos
    load_photo = State()

    # for b2c/b2b info_logic
    b2c_logic = State()
    b2b_logic = State()

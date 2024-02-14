from aiogram.types import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_authorize_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Авторизоваться", request_contact=True)
    kb = kb.as_markup()
    kb.one_time_keyboard = True
    kb.resize_keyboard = True
    return kb


def get_no_orders_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="Оформить новый заказ", callback_data="new_order")
    )
    kb.row(
        InlineKeyboardButton(text="Позвать менеджера", callback_data="ask_for_manager")
    )
    kb.row(
        InlineKeyboardButton(
            text="Проверить старые заказы", callback_data="check_order_history"
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="На главную", callback_data="back_to_menu"
        )
    )
    return kb.as_markup()

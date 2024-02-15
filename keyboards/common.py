from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Общая информация", callback_data="info"))
    kb.row(
        InlineKeyboardButton(
            text="Проверить статус заказа", callback_data="order_status"
        )
    )
    kb.row(InlineKeyboardButton(text="Получить скидку", callback_data="sale"))
    kb.row(
        InlineKeyboardButton(
            text="Проверить историю заказов", callback_data="check_order_history"
        )
    )
    kb.row(
        InlineKeyboardButton(text="Позвать менеджера", callback_data="ask_for_manager")
    )

    return kb.as_markup()

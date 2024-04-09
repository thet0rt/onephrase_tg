from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.row(InlineKeyboardButton(text="Общая информация", callback_data="info"))
    kb.row(
        InlineKeyboardButton(
            text="Проверить статус заказа", callback_data="order_status_menu"
        )
    )
    kb.row(InlineKeyboardButton(text="Получить скидку", callback_data="sale"))
    kb.row(
        InlineKeyboardButton(text="Позвать менеджера", callback_data="ask_for_manager")
    )

    return kb.as_markup()


def get_ask_for_manager_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.row(InlineKeyboardButton(text="Ответы на популярные вопросы", callback_data="Q&A_from_manager"))
    # todo вернуть позже
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт", url='https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot',
            callback_data="back_to_info_menu"
        )
    )
    kb.row(
        InlineKeyboardButton(text="На главную", callback_data="back_to_menu")
    )

    return kb.as_markup()


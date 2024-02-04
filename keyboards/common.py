from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Общая информация ✅', callback_data='info'))
    kb.row(InlineKeyboardButton(text='Проверить статус заказа ✅', callback_data='order_status'))
    kb.row(InlineKeyboardButton(text='Случайный выбор худи ✅', callback_data='random_choice'))
    # todo подумать, что делать с этой фразой (не умещается)
    kb.row(InlineKeyboardButton(text='Попросить нейросеть придумать фразу ✅', callback_data='neuro_phrase'))

    return kb.as_markup()

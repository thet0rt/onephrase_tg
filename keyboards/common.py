from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardButton


def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Общая информация ✅', callback_data='info'))
    kb.row(InlineKeyboardButton(text='Проверить статус заказа ✅', callback_data='order_status'))
    kb.row(InlineKeyboardButton(text='Случайный выбор худи ✅', callback_data='random_choice'))
    # todo подумать, что делать с этой фразой (не умещается)
    kb.row(InlineKeyboardButton(text='Попросить нейросеть придумать фразу ✅', callback_data='neuro_phrase'))

    return kb.as_markup()

#
# def get_main_kb_2() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardBuilder()
#     options = ['Общая информация', 'Проверить статус заказа', 'Случайный выбор худи',
#                'Попросить нейросеть придумать фразу', 'Получить скидку', 'Посмотреть старые заказы',
#                'Позвать менеджера']
#     for text in options:
#         kb.button(text=text, callback_data=text)
#     kb.adjust(2)
#     return kb.as_markup(resize_keyboard=True)

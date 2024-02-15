from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from logic.info_logic import INFO_MSG_CONFIG


def get_main_info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Цены", callback_data="price"))
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт", url='https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot',
            callback_data="-"
        )
    )
    kb.row(InlineKeyboardButton(text="Для бизнеса", callback_data="for_business"))
    kb.row(
        InlineKeyboardButton(
            text="Кастом", callback_data="custom"
        )
    )
    kb.row(
        InlineKeyboardButton(text="Цвета", callback_data="colors")
    )
    kb.row(
        InlineKeyboardButton(text='Срок изготовления и доставка', callback_data='terms_of_manufacturing')
    )

    return kb.as_markup()


def get_price_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for item, item_settings in INFO_MSG_CONFIG.items():
        kb.row(InlineKeyboardButton(text=item_settings.get('button_name'), callback_data=item))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_price_shown_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_price"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()

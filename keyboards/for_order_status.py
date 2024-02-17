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
        InlineKeyboardButton(
            text="Посмотреть старые заказы", callback_data="check_order_history"
        )
    )
    kb.row(
        InlineKeyboardButton(text="Позвать менеджера", callback_data="ask_for_manager")
    )
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))
    return kb.as_markup()


def get_subscribe_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Подписаться", url="https://t.me/justonephrase", callback_data="-"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="Проверить подписку и получить скидку", callback_data="sale"
        )
    )

    return kb.as_markup()


def get_subscribe_success_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт", url="https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot", callback_data="-"
        )  # todo посмотреть что тут можно сделать
    )
    kb.row(InlineKeyboardButton(text="Оформить заказ здесь", callback_data="new_order"))  # todo smth here
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_after_order_status_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт", url="https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot", callback_data="-"
        )  # todo посмотреть что тут можно сделать
    )
    kb.row(InlineKeyboardButton(text="Оформить новый заказ", callback_data="new_order"))  # todo smth here
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_after_order_history_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Проверить актуальные заказы", callback_data="order_status"
        )
    )
    kb.row(InlineKeyboardButton(text="Оформить новый заказ", callback_data="new_order"))  # todo smth here
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()

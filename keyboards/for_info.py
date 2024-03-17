from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from configuration import PRICE_MSG_CONFIG, FAQ_CFG, COLORS_MSG_CONFIG
from utils.states import CurrentLogic


def get_main_info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Цены", callback_data="price"))
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт",
            url="https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot",
            callback_data="-",
        )
    )
    kb.row(InlineKeyboardButton(text="Кастом", callback_data="custom"))
    kb.row(InlineKeyboardButton(text="Цвета", callback_data="colors"))
    kb.row(
        InlineKeyboardButton(
            text="Срок изготовления и доставка", callback_data="terms_of_manufacturing"
        )
    )
    kb.row(InlineKeyboardButton(text="Корпоративный мерч", callback_data="for_business"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


# region Price
def get_price_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for item, item_settings in PRICE_MSG_CONFIG.items():
        kb.row(
            InlineKeyboardButton(
                text=item_settings.get("button_name"), callback_data=item
            )
        )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_info_menu"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_price_shown_kb(item: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_price"))
    if item in ('price_t-shirt', 'price_t-shirt-true-over'):
        kb.row(InlineKeyboardButton(text="Футболки база/тру овер", callback_data='t-shirt_more_info_from_price'))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_price_tshirt_more_info_shown_kb() -> InlineKeyboardMarkup:
    # менять сразу в двух местах
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_price"))
    kb.row(InlineKeyboardButton(text='Подробнее на сайте',
                                url='https://onephrase.ru/size-chart#!/tab/668768217-3/?utm_source=tg_bot'))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))
    return kb.as_markup()


# endregion


# region Business
def get_for_business_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Ассортимент", callback_data="collections"))
    kb.row(InlineKeyboardButton(text="Ответы на вопросы", callback_data="Q&A"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_info_menu"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_collections_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="Назначить диалог на корпоративного менеджера и отправить уведомление",
            callback_data="corporate_manager",
        )
    )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_business"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_faq_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for question, question_settings in FAQ_CFG.items():
        kb.row(
            InlineKeyboardButton(
                text=question_settings.get("button_name"), callback_data=question
            )
        )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_business"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_faq_kb_from_manager() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for question, question_settings in FAQ_CFG.items():
        kb.row(
            InlineKeyboardButton(
                text=question_settings.get("button_name"), callback_data=question
            )
        )
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_answered_kb(item: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if item == 'b2b_colors':
        kb.row(InlineKeyboardButton(text="Посмотреть цвета в основном каталоге", callback_data="colors_from_b2b"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_questions"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


# endregion


# region Custom


def get_custom_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Заказать кастом на сайте",
            url="https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot",  # другая ссылка?
            callback_data="back_to_info_menu",
        )
    )
    kb.row(
        InlineKeyboardButton(text="Позвать менеджера", callback_data="ask_for_manager")
    )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_info_menu"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


# endregion


# region Colors
def get_colors_kb(back_cb_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for item, item_settings in COLORS_MSG_CONFIG.items():
        kb.row(
            InlineKeyboardButton(
                text=item_settings.get("button_name"), callback_data=item
            )
        )

    kb.row(InlineKeyboardButton(text="Назад", callback_data=back_cb_data))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_colors_shown_kb(item) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_colors"))
    if item in ('colors_t-shirt', 'colors_t-shirt-true-over'):
        kb.row(InlineKeyboardButton(text="Футболки база/тру овер", callback_data='t-shirt_more_info_from_colors'))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_colors_tshirt_more_info_shown_kb() -> InlineKeyboardMarkup:
    # менять сразу в двух местах
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Подробнее на сайте',
                                url='https://onephrase.ru/size-chart#!/tab/668768217-3/?utm_source=tg_bot'))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_colors"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))
    return kb.as_markup()


# endregion


# region Terms of manufacturing


def get_manufacturing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Перейти на сайт",
            url="https://onephrase.ru/?utm_source=tg&utm_medium=tg_bot",  # другая ссылка?
            callback_data="back_to_info_menu",
        )
    )
    kb.row(
        InlineKeyboardButton(text="В наличии (доставка за 1-2 рабочих дня)",
                             url='https://onephrase.ru/catalog/in-stock/?utm_source=tg&utm_medium=tg_bot',
                             callback_data="back_to_info_menu")
    )
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_info_menu"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()

# endregion

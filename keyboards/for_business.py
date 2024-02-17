from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from logic.configuration import BUSINESS_MSG_CONFIG
FAQ_CFG = BUSINESS_MSG_CONFIG.get('F&Q')


def get_for_business_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Ассортимент", callback_data="collections"))
    kb.row(InlineKeyboardButton(text="Ответы на вопросы", callback_data="F&Q"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_common_questions"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_collections_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Назначить диалог на корпоративного менеджера и отправить уведомление',
                                callback_data="corporate_manager"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_business"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_faq_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    faq_cfg = BUSINESS_MSG_CONFIG.get('F&Q')
    for question, question_settings in faq_cfg.items():
        kb.row(InlineKeyboardButton(text=question_settings.get('button_name'),
                                    callback_data=question))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_business"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()


def get_answered_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Назад", callback_data="back_to_questions"))
    kb.row(InlineKeyboardButton(text="На главную", callback_data="back_to_menu"))

    return kb.as_markup()

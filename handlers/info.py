from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.for_info import *
from logic.configuration import INFO_MSG_CONFIG, BUSINESS_MSG_CONFIG, CUSTOM_MSG_CONFIG, MANUFACTURING_MSG_CONFIG

FAQ_CFG = BUSINESS_MSG_CONFIG.get("Q&A")
router = Router()  # [1]


@router.callback_query(F.data.in_({"info", "back_to_common_questions"}))
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    if callback_query.data == "back_to_common_questions":
        await callback_query.message.delete()
    await callback_query.message.answer(
        "Рады, что вы хотите узнать нас получше. Что рассказать?",
        reply_markup=get_main_info_kb(),
    )


# region Price
@router.callback_query(F.data.in_({"price", "back_to_price"}))
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer("")
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Что вас интересует?", reply_markup=get_price_kb()
    )


@router.callback_query(F.data.in_(set(INFO_MSG_CONFIG.keys())))
async def price_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    item = callback_query.data
    info_msg = INFO_MSG_CONFIG.get(item, {}).get("msg")
    await callback_query.message.answer(info_msg, reply_markup=get_price_shown_kb())


# endregion


# region Business
@router.callback_query(F.data.in_({"for_business", "back_to_business"}))
async def business_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("main_msg")
    await callback_query.message.answer(text=msg, reply_markup=get_for_business_kb())


@router.callback_query(F.data == "collections")
async def about_collections(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("collections_msg")
    await callback_query.message.answer(text=msg, reply_markup=get_collections_kb())


@router.callback_query(F.data.in_(set(FAQ_CFG.keys())))
async def show_answer(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    item = callback_query.data
    msg = FAQ_CFG.get(item, {}).get("msg")
    await callback_query.message.answer(text=msg, reply_markup=get_answered_kb())


@router.callback_query(F.data.in_({"back_to_questions", "Q&A", "Q&A_from_manager"}))
async def faq_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    reply_kb = get_faq_kb() if callback_query.data != 'Q&A_from_manager' else get_faq_kb_from_manager()
    await callback_query.message.answer(
        text="Часто задаваемые вопросы", reply_markup=reply_kb
    )


# endregion


# region Custom
@router.callback_query(F.data == "custom")
async def custom_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = CUSTOM_MSG_CONFIG.get("main_msg")
    await callback_query.message.answer(msg, reply_markup=get_custom_kb())


# endregion


# region Colors
@router.callback_query(F.data == "colors")
async def colors_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    # msg = CUSTOM_MSG_CONFIG.get("main_msg")
    msg = 'todo'
    await callback_query.message.answer(msg, reply_markup=get_custom_kb())


# endregion


# region Terms of manufacturing
@router.callback_query(F.data == "terms_of_manufacturing")
async def manufacturing_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = MANUFACTURING_MSG_CONFIG.get("main_msg")
    await callback_query.message.answer(msg, reply_markup=get_manufacturing_kb())


# endregion

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.for_info import *
from configuration import (PRICE_MSG_CONFIG, BUSINESS_MSG_CONFIG, FAQ_CFG, COLORS_MSG_CONFIG, OTHER_MSG_CFG)
from log_settings import log
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from utils.states import CurrentLogic


router = Router()  # [1]


@router.callback_query(F.data.in_({"info", "back_to_info_menu"}))
async def info_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(CurrentLogic.b2c_logic)
    if callback_query.data == "back_to_info_menu":
        # await callback_query.message.delete()
        pass
    await callback_query.message.answer(
        "Рады, что вы хотите узнать нас получше. Что рассказать?",
        reply_markup=get_main_info_kb(),
    )


# region Price
@router.callback_query(F.data.in_({"price", "back_to_price"}))
async def price_menu(callback_query: CallbackQuery):
    await callback_query.answer("")
    # await callback_query.message.delete()
    await callback_query.message.answer(
        "Что вас интересует?", reply_markup=get_price_kb()
    )


@router.callback_query(F.data.in_(set(PRICE_MSG_CONFIG.keys())))
async def price_info(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    item = callback_query.data
    info_msg = PRICE_MSG_CONFIG.get(item, {}).get("msg")
    photo_path = PRICE_MSG_CONFIG.get(item, {}).get("photo_path")
    log.debug(photo_path)
    await callback_query.message.answer_photo(photo=FSInputFile(photo_path),
                                              caption=info_msg,
                                              reply_markup=get_price_shown_kb(item))


# endregion


# region Business
@router.callback_query(F.data.in_({"for_business", "back_to_business"}))
async def business_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(CurrentLogic.b2b_logic)
    # await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("main", {}).get('msg')
    await callback_query.message.answer(text=msg, reply_markup=get_for_business_kb())


@router.callback_query(F.data == "collections")
async def about_collections(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("collections", {}).get('msg')
    await callback_query.message.answer(text=msg, reply_markup=get_collections_kb())


@router.callback_query(F.data.in_(set(FAQ_CFG.keys())))
async def show_answer(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    item = callback_query.data
    msg = FAQ_CFG.get(item, {}).get("msg")
    photo_path = FAQ_CFG.get(item, {}).get("photo_path")
    await callback_query.message.answer_photo(photo=FSInputFile(photo_path),
                                              caption=msg,
                                              reply_markup=get_answered_kb(item))


@router.callback_query(F.data.in_({"back_to_questions", "Q&A", "Q&A_from_manager"}))
async def faq_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    reply_kb = get_faq_kb() if callback_query.data != 'Q&A_from_manager' else get_faq_kb_from_manager()
    await callback_query.message.answer(
        text="Часто задаваемые вопросы", reply_markup=reply_kb
    )


# endregion


# region Custom
@router.callback_query(F.data == "custom")
async def custom_info(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("custom", {}).get('msg')
    await callback_query.message.answer(msg, reply_markup=get_custom_kb())


# endregion


# region Colors

@router.callback_query(F.data.in_({"colors", "back_to_colors", "colors_from_b2b"}))
async def colors_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")
    # await callback_query.message.delete()
    current_state = await state.get_state()
    if current_state == CurrentLogic.b2b_logic:
        back_cb_data = 'back_to_questions'
    else:  # current_state == CurrentLogic.b2c_logic
        back_cb_data = "back_to_info_menu"
    await callback_query.message.answer(
        "Что вас интересует?", reply_markup=get_colors_kb(back_cb_data)
    )


@router.callback_query(F.data.in_(set(COLORS_MSG_CONFIG.keys())))
async def colors_info(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    item = callback_query.data
    info_msg = COLORS_MSG_CONFIG.get(item, {}).get("msg")
    photo_path = COLORS_MSG_CONFIG.get(item, {}).get("photo_path")
    await callback_query.message.answer_photo(photo=FSInputFile(photo_path),
                                              caption=info_msg,
                                              reply_markup=get_colors_shown_kb(item))


# endregion

# region More
@router.callback_query(F.data.in_({"t-shirt_more_info_from_colors", "t-shirt_more_info_from_price"}))
async def tshirt_more_info(callback_query: CallbackQuery):
    await callback_query.answer()
    msg = OTHER_MSG_CFG.get("t-shirt_more_info", {}).get('msg')
    photo_path = OTHER_MSG_CFG.get("t-shirt_more_info", {}).get('photo_path')
    # await callback_query.message.delete()
    if callback_query.data == 't-shirt_more_info_from_colors':
        reply_kb = get_colors_tshirt_more_info_shown_kb()
    else:
        reply_kb = get_price_tshirt_more_info_shown_kb()
    await callback_query.message.answer_photo(photo=FSInputFile(photo_path),
                                              caption=msg,
                                              reply_markup=reply_kb
                                              )


# endregion


# region Terms of manufacturing
@router.callback_query(F.data == "terms_of_manufacturing")
async def manufacturing_info(callback_query: CallbackQuery):
    await callback_query.answer()
    # await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get("manufacturing", {}).get('msg')
    await callback_query.message.answer(msg, reply_markup=get_manufacturing_kb())

# endregion

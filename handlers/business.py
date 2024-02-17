from aiogram import Router, F
from aiogram.types import CallbackQuery
from logic.configuration import BUSINESS_MSG_CONFIG
from keyboards.for_business import get_for_business_kb, get_collections_kb, get_faq_kb, get_answered_kb

FAQ_CFG = BUSINESS_MSG_CONFIG.get('F&Q')

router = Router()  # [1]


@router.callback_query(F.data.in_({'for_business', 'back_to_business'}))
async def business_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get('main_msg')
    await callback_query.message.answer(text=msg, reply_markup=get_for_business_kb())


@router.callback_query(F.data == 'collections')
async def about_collections(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    msg = BUSINESS_MSG_CONFIG.get('main_msg')
    await callback_query.message.answer(text=msg, reply_markup=get_collections_kb())


@router.callback_query(F.data.in_(set(FAQ_CFG.keys())))
async def show_answer(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    item = callback_query.data
    msg = FAQ_CFG.get(item, {}).get('msg')
    await callback_query.message.answer(text=msg, reply_markup=get_answered_kb())


@router.callback_query(F.data.in_({'back_to_questions', 'F&Q'}))
async def faq_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer(text='Часто задаваемые вопросы', reply_markup=get_faq_kb())

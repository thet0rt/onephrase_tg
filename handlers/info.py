from aiogram import Router, F
from aiogram.types import CallbackQuery
from logic.configuration import INFO_MSG_CONFIG
from keyboards.for_info import get_main_info_kb, get_price_kb, get_price_shown_kb

router = Router()  # [1]


@router.callback_query(F.data.in_({'info', "back_to_common_questions"}))
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    if callback_query.data == 'back_to_common_questions':
        await callback_query.message.delete()
    await callback_query.message.answer('Рады, что вы хотите узнать нас получше. Что рассказать?',
                                        reply_markup=get_main_info_kb())


@router.callback_query(F.data.in_({'price', 'back_to_price'}))
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer('')
    await callback_query.message.delete()
    await callback_query.message.answer('Что вас интересует?', reply_markup=get_price_kb())


@router.callback_query(F.data.in_(set(INFO_MSG_CONFIG.keys())))
async def price_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    item = callback_query.data
    info_msg = INFO_MSG_CONFIG.get(item, {}).get('msg')
    await callback_query.message.answer(info_msg, reply_markup=get_price_shown_kb())


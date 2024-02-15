from typing import Optional

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.states import CurrentLogic
from logic.info_logic import INFO_MSG_CONFIG
from keyboards.for_info import get_main_info_kb, get_price_kb, get_price_shown_kb

router = Router()  # [1]


@router.callback_query(F.data == 'info')
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer(' ')
    await callback_query.message.answer('Рады, что вы хотите узнать нас получше. Что рассказать?',
                                        reply_markup=get_main_info_kb())


@router.callback_query(F.data.in_({'price', 'back_to_price'}))
async def info_menu(callback_query: CallbackQuery):
    await callback_query.answer(' ')
    await callback_query.message.answer('Выберите элемент одежды', reply_markup=get_price_kb())


@router.callback_query(F.data.in_({'hoodie', 'sweet', 't-shirt', 't-shirt-true-over', 'pants', 'longsleeve'}))
async def price_info(callback_query: CallbackQuery):
    await callback_query.answer(' ')
    item = callback_query.data
    info_msg = INFO_MSG_CONFIG.get(item, {}).get('msg')
    await callback_query.message.answer(info_msg, reply_markup=get_price_shown_kb())


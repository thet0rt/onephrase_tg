from typing import Optional

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from integration.retailcrm_methods import get_orders_by_number
from integration.helpers import process_order_data
from db import set_to, get_from

from keyboards.for_order_status import get_authorize_kb, get_no_orders_kb

router = Router()  # [1]


@router.callback_query(F.data == "order_status")
async def order_status(callback_query: CallbackQuery):
    if phone_number := await check_authorization(str(callback_query.from_user.id)):
        await show_actual_orders(callback_query, phone_number)
    else:
        await callback_query.message.answer(
            text="Authorize", reply_markup=get_authorize_kb()
        )


@router.callback_query(F.data == "check_order_history")
async def order_status(callback_query: CallbackQuery):
    if phone_number := await check_authorization(str(callback_query.from_user.id)):
        await show_order_history(callback_query, phone_number)
    else:
        await callback_query.message.answer(
            text="Authorize", reply_markup=get_authorize_kb()
        )


@router.message(F.content_type.in_({"contact"}))
async def authorize(message: Message):
    phone_number = message.contact.phone_number
    print(message.from_user.id)
    await set_to(str(message.from_user.id), str(phone_number), ex=3600)
    # todo здесь надо запомнить, из какой функции мы пришли и продолжить разговор


async def check_authorization(user_id: str) -> Optional[str]:
    phone_number = await get_from(user_id)
    return phone_number


async def show_actual_orders(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'new')
    print(orders)
    if not orders:
        await callback_query.answer(
            text="Мы не нашли актуальных заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await callback_query.answer(text=order_info, reply_markup=ReplyKeyboardRemove())


async def show_order_history(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'old')
    if not orders:
        await callback_query.message.answer(
            text="Мы не нашли старых заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await callback_query.message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())

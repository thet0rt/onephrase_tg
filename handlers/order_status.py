from typing import Optional

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from integration.retailcrm_methods import get_orders_by_number
from integration.helpers import process_order_data
from db import set_to, get_from
from aiogram.fsm.context import FSMContext
from utils.states import CurrentLogic

from keyboards.for_order_status import get_authorize_kb, get_no_orders_kb

router = Router()  # [1]


@router.callback_query(F.data == "order_status")
async def order_status(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    if phone_number := await check_authorization(user_id):
        await show_actual_orders_query(callback_query, phone_number)
    else:
        await state.set_state(CurrentLogic.order_status)
        await callback_query.answer('Проверяем авторизацию')
        await callback_query.message.answer(
            text="Чтобы увидеть свои заказы, пройдите авторизацию", reply_markup=get_authorize_kb()
        )


@router.callback_query(F.data == "check_order_history")
async def order_status(callback_query: CallbackQuery, state: FSMContext):
    if phone_number := await check_authorization(str(callback_query.from_user.id)):
        await show_order_history_query(callback_query, phone_number)
    else:
        await state.set_state(CurrentLogic.order_history)
        await callback_query.answer(
            text="Проверяем авторизацию", reply_markup=get_authorize_kb()
        )


@router.message(F.content_type.in_({"contact"}))
async def authorize(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await set_to(str(message.from_user.id), str(phone_number), ex=3600)
    await message.answer('Спасибо! Теперь мы сможем найти Ваши заказы', reply_markup=ReplyKeyboardRemove())
    print(await state.get_state())
    if await state.get_state() == CurrentLogic.order_status:
        await show_actual_orders_msg(message, phone_number)
    elif await state.get_state() == CurrentLogic.order_history:
        await show_order_history_msg(message, phone_number)
    # todo придумать как убрать кнопку авторизации


async def check_authorization(user_id: str) -> Optional[str]:
    phone_number = await get_from(user_id)
    return phone_number


async def show_actual_orders_query(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'new')
    print(orders)
    if not orders:
        await callback_query.answer(' ')
        await callback_query.message.answer(
            text="Мы не нашли актуальных заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await callback_query.message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())


async def show_actual_orders_msg(message: Message, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'new')
    print(orders)
    if not orders:
        await message.answer(
            text="Мы не нашли актуальных заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())


async def show_order_history_query(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'old')
    if not orders:
        await callback_query.message.answer(
            text="Мы не нашли старых заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        await callback_query.answer(text='Проверяем историю заказов')
        for order_info in orders_info:
            await callback_query.message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())


async def show_order_history_msg(message: Message, phone_number: str):
    orders = await get_orders_by_number(phone_number, 'old')
    if not orders:
        await message.answer(
            text="Мы не нашли старых заказов.", reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())

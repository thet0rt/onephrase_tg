import re
from datetime import timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from configuration import OTHER_MSG_CFG
from db import set_to
from keyboards.for_order_status import (
    get_authorize_kb,
    get_subscribe_kb,
    get_subscribe_success_kb, get_invalid_number_kb, get_main_order_status_kb
)
from log_settings import log
from logic.order_status import (
    check_authorization,
    show_actual_orders_query,
    show_order_history_query,
    show_actual_orders_msg,
    show_order_history_msg, show_order_by_order_number,
)
from utils.states import CurrentLogic

router = Router()  # [1]


@router.callback_query(F.data == "order_status_menu")
async def order_status(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        text="Проверить статус заказа",
        reply_markup=get_main_order_status_kb(),
    )


@router.callback_query(F.data == "order_status")
async def order_status(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    if phone_number := await check_authorization(user_id):
        await show_actual_orders_query(callback_query, phone_number)
    else:
        await state.set_state(CurrentLogic.order_status)
        await callback_query.answer("Проверяем авторизацию")
        await callback_query.message.answer(
            text="Чтобы увидеть свои заказы, пройдите авторизацию",
            reply_markup=get_authorize_kb(),
        )


@router.callback_query(F.data == "check_order_history")
async def order_history(callback_query: CallbackQuery, state: FSMContext):
    user_id = str(callback_query.from_user.id)
    if phone_number := await check_authorization(user_id):
        await show_order_history_query(callback_query, phone_number)
    else:
        await state.set_state(CurrentLogic.order_history)
        await callback_query.answer("Проверяем авторизацию")
        await callback_query.message.answer(
            text="Чтобы увидеть свои заказы, пройдите авторизацию",
            reply_markup=get_authorize_kb(),
        )


@router.callback_query(F.data == "sale")
async def get_sale(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.answer("Проверяем подписку...")
    subscription_status = await bot.get_chat_member(
        chat_id=-1001613641192, user_id=callback_query.from_user.id
    )
    if subscription_status.status != "left":
        await callback_query.message.answer(
            text=OTHER_MSG_CFG.get('sale', {}).get('msg'),
            reply_markup=get_subscribe_success_kb(),
        )
    else:
        await callback_query.message.answer(
            "Чтобы получать бонусы нужно быть подписанным"
            " на наш канал @onephrase",
            reply_markup=get_subscribe_kb(),
        )


@router.message(F.content_type.in_({"contact"}))
async def authorize(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await set_to(str(message.from_user.id), str(phone_number), ex=timedelta(days=30))
    await message.answer(
        "Спасибо! Теперь мы сможем найти Ваши заказы",
        reply_markup=ReplyKeyboardRemove(),
    )  # todo мб убрать
    state = await state.get_state()
    log.debug(state)
    if state == CurrentLogic.order_status:
        await show_actual_orders_msg(message, phone_number)
    elif state == CurrentLogic.order_history:
        await show_order_history_msg(message, phone_number)


@router.callback_query(F.data == "input_order_number")
async def input_order_number(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(CurrentLogic.input_order_number)
    await callback_query.message.answer(
        text="Введите номер заказа:"
    )


@router.message(F.text, CurrentLogic.input_order_number)
async def get_order_by_order_number(message: Message):
    order_number = message.text
    if not re.fullmatch(r'[0-9]{1,5}[ACАС]', order_number):
        return await message.answer(
            text="Неверный номер заказа. Формат номера заказа: 12345C. Попробуйте ввести еще раз:",
            reply_markup=get_invalid_number_kb()
        )
    await show_order_by_order_number(message, order_number)


# todo delete in production
@router.message(F.text.in_({'logout', 'Logout'}))
async def login(message: Message):
    from db import redis_client
    await redis_client.delete(message.from_user.id)
    await message.answer(text=f'Logged out successfully',
                         reply_markup=get_invalid_number_kb())


# todo delete in production
@router.message(F.text)
async def login(message: Message):
    phone_number = message.text
    if not re.fullmatch(r'[0-9]{11}', phone_number):
        return await message.answer(
            text="Введи в формате 79087530154",
            reply_markup=get_invalid_number_kb()
        )
    await set_to(str(message.from_user.id), phone_number, timedelta(days=30))
    await message.answer(text=f'Authorized successfully as {phone_number}',
                         reply_markup=get_invalid_number_kb())

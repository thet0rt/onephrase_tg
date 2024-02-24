from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from db import set_to
from keyboards.for_order_status import (
    get_authorize_kb,
    get_subscribe_kb,
    get_subscribe_success_kb,
)
from log_settings import log
from logic.order_status import (
    check_authorization,
    show_actual_orders_query,
    show_order_history_query,
    show_actual_orders_msg,
    show_order_history_msg,
)
from utils.states import CurrentLogic

router = Router()  # [1]


@router.callback_query(F.data == "order_status")
async def order_status(callback_query: CallbackQuery, state: FSMContext):
    await set_to('test', 'test', 3600)  # todo delete later
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
async def order_status(callback_query: CallbackQuery, state: FSMContext):
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
            "Спасибо за подписку! Промокод на скидку 12% - TGSUB",
            reply_markup=get_subscribe_success_kb(),
        )
    else:
        await callback_query.message.answer(
            "Чтобы получать бонусы нужно быть подписанным"
            " на наш канал @justonephrase",
            reply_markup=get_subscribe_kb(),
        )


@router.message(F.content_type.in_({"contact"}))
async def authorize(message: Message, state: FSMContext):
    phone_number = '79244996888' or message.contact.phone_number
    await set_to(str(message.from_user.id), str(phone_number), ex=3600)
    await message.answer(
        "Спасибо! Теперь мы сможем найти Ваши заказы",
        reply_markup=ReplyKeyboardRemove(),
    )
    log.debug(await state.get_state())
    if await state.get_state() == CurrentLogic.order_status:
        await show_actual_orders_msg(message, phone_number)
    elif await state.get_state() == CurrentLogic.order_history:
        await show_order_history_msg(message, phone_number)

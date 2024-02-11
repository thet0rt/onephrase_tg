from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from retailcrm_integration.methods import get_orders_by_number
from retailcrm_integration.helpers import process_order_data

from keyboards.for_order_status import get_authorize_kb, get_no_orders_kb

router = Router()  # [1]


@router.callback_query(F.data == "order_status")
async def order_status(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Authorize", reply_markup=get_authorize_kb()
    )


@router.message(F.content_type.in_({"contact"}))
async def authorize(message: Message):
    phone_number = '79081652716' or message.contact.phone_number  # todo delete phone number later
    orders = await get_orders_by_number(phone_number)
    print(orders)
    if not orders:
        await message.answer(text='Мы не нашли актуальных заказов.', reply_markup=get_no_orders_kb())
    else:
        orders_info = process_order_data(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())

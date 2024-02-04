from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.types import FSInputFile

from keyboards.for_order_status import get_authorize_kb

router = Router()  # [1]


@router.callback_query(F.data == 'order_status')
async def order_status(callback_query: CallbackQuery):
    print('here')
    await callback_query.message.answer(text='Authorize', reply_markup=get_authorize_kb())

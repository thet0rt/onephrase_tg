from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, Update, CallbackQuery
from aiogram.handlers import InlineQueryHandler
from aiogram.types import FSInputFile, CallbackQuery, InlineQuery, ChosenInlineResult

from keyboards.common import get_main_kb

router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    logo = FSInputFile("media/logo.png")
    await message.answer_photo(
        photo=logo,
        caption="Твой текст",  # todo change text
        reply_markup=get_main_kb(),
    )


@router.callback_query(F.data == "back_to_menu")
async def order_status(callback_query: CallbackQuery):
    logo = FSInputFile("media/logo.png")
    await callback_query.answer(" ")
    await callback_query.message.answer_photo(
        photo=logo, caption="Твой текст", reply_markup=get_main_kb()
    )

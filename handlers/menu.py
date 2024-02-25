from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, CallbackQuery
from aiogram.types import Message

from keyboards.common import get_main_kb, get_ask_for_manager_kb

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


@router.callback_query(F.data == "back_to_menu")
async def ask_for_manager(callback_query: CallbackQuery):
    await callback_query.answer()
    msg_answer = ('Позвали человека, надеемся он поможет!'
                  ' Отвечаем в рабочее время с 10 до 22, на все сообщения отвечаем в порядке очереди,'
                  ' поэтому иногда ответ требует немного больше времени, пожалуйста, не дублируйте свои запросы.'
                  ' Для более оперативного ответа опишите, пожалуйста, в следующем сообщении свой запрос так подробно,'
                  ' как вы считаете нужным.')
    await callback_query.message.answer(text=msg_answer, reply_markup=get_ask_for_manager_kb())

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import FSInputFile

# from keyboards.for_questions import get_yes_no_kb
from keyboards.common import get_main_kb
router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    logo = FSInputFile('media/logo.png')
    await message.answer_photo(
        photo=logo,
        caption="Твой текст",
        reply_markup=get_main_kb(),
    )


@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )

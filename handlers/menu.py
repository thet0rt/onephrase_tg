import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery
from aiogram.types import Message

from configuration import OTHER_MSG_CFG
from integration.helpers import upload_photo_to_server, upload_zip_to_server
from keyboards.common import get_main_kb, get_ask_for_manager_kb
from utils.states import CurrentLogic
from logic.photos import compress_img
from aiogram.types.link_preview_options import LinkPreviewOptions

router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    if await state.get_state() == CurrentLogic.load_photo:
        await state.set_state(CurrentLogic.basic)
    msg = OTHER_MSG_CFG.get('main', {}).get('msg')
    photo_path = OTHER_MSG_CFG.get('main', {}).get('photo_path')
    await message.answer_photo(
        photo=FSInputFile(photo_path),
        caption=msg,
        reply_markup=get_main_kb(),
    )


@router.callback_query(F.data == "back_to_menu")
async def main_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    # msg = OTHER_MSG_CFG.get('main', {}).get('msg')
    photo_path = OTHER_MSG_CFG.get('main', {}).get('photo_path')
    await callback_query.message.answer(
        text=OTHER_MSG_CFG.get('main_menu', {}).get('msg'),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=get_main_kb()
    )


@router.callback_query(F.data == "ask_for_manager")
async def ask_for_manager(callback_query: CallbackQuery):
    await callback_query.answer()
    msg_answer = ('Позвали человека, надеемся он поможет!'
                  ' Отвечаем в рабочее время с 10 до 22, на все сообщения отвечаем в порядке очереди,'
                  ' поэтому иногда ответ требует немного больше времени, пожалуйста, не дублируйте свои запросы.'
                  ' Для более оперативного ответа опишите, пожалуйста, в следующем сообщении свой запрос так подробно,'
                  ' как вы считаете нужным.')
    await callback_query.message.answer(text=msg_answer, reply_markup=get_ask_for_manager_kb())


@router.message(F.text == os.getenv("ADMIN_LOGIN_PHRASE"))
async def admin_login(message: Message, state: FSMContext):
    await state.set_state(CurrentLogic.load_photo)
    await message.answer('Logged in successfully. Loading photos available.')


# @router.message(F.document, CurrentLogic.load_photo)
# async def handle_photo(message: Message):
#     file_id = message.document.file_id
#     file_name = message.document.file_name
#     file = await message.document.bot.get_file(file_id)
#     file_path = file.file_path
#     file_ext = file_path.split('.')[-1]
#     file_io = await message.document.bot.download_file(file_path)
#     if file_ext.lower() in ['png', 'jpg', 'jpeg', 'jpeg-2000', 'raw', 'tiff', 'bmp', 'heif']:
#         file_io_compressed = compress_img(file_io)
#         file_name = file_ext
#         route = await upload_photo_to_server(file_io_compressed, file_name)
#     else:
#         route = await upload_photo_to_server(file_io, file_name)
#     if route:
#         message_text = f'{os.getenv("DOWNLOAD_PHOTO_URL")}{route}'
#     else:
#         message_text = 'Не удалось создать ссылку на файл'
#     await message.answer(message_text)


@router.message(F.document, CurrentLogic.load_photo)
async def upload_zip(message: Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await message.document.bot.get_file(file_id)
    file_path = file.file_path
    file_ext = file_path.split('.')[-1]
    file_io = await message.document.bot.download_file(file_path)
    route = None
    if file_ext.lower() in ['zip']:
        xlsx_filename = await upload_zip_to_server(file_io, file_name)
    if route:
        message_text = f'{os.getenv("DOWNLOAD_PHOTO_URL")}/xlsx_info/{xlsx_filename}'
    else:
        message_text = 'Не удалось создать ссылку на файл'
    await message.answer(message_text)

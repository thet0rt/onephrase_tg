from dotenv import load_dotenv

load_dotenv("dev.env")

from os import getenv
from aiogram import Bot, Dispatcher
from middlewares import LoggingMiddleware


from handlers import menu, order_status, info

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_routers(
    menu.router, order_status.router,   # info.router todo вернуть позже
)
dp.message.middleware(LoggingMiddleware())
dp.callback_query.middleware(LoggingMiddleware())



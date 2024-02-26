from dotenv import load_dotenv

load_dotenv(".env")

from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from middlewares import LoggingMiddleware


from handlers import menu, order_status, info


# Запуск бота
async def main():
    token = getenv("BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(
        menu.router, order_status.router, info.router
    )
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from dotenv import load_dotenv

load_dotenv(".env")

from os import getenv, environ
import asyncio
from aiogram import Bot, Dispatcher

from handlers import menu, different_types, order_status


# Запуск бота
async def main():
    token = getenv("BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(menu.router, different_types.router, order_status.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

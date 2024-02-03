import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv


# Запуск бота
async def main():
    load_dotenv('.env')
    token = getenv('BOT_TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher()

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
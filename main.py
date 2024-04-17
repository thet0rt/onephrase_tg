import os.path

from fastapi import FastAPI
from aiogram import types, Bot
from aiogram.types import WebhookInfo, Update
from bot import dp, bot
from os import getenv
from log_settings import log
from fastapi.responses import FileResponse

from dotenv import load_dotenv

load_dotenv("dev.env")

app = FastAPI()
WEBHOOK_PATH = f'/bot/{getenv("BOT_TOKEN")}'
WEBHOOK_URL = os.getenv("SSL_URL") + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    await set_webhook(bot)


async def set_webhook(my_bot: Bot) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            log.error("Can't get webhook info - %s", e)
            return

    current_webhook_info = await check_webhook()
    if getenv("DEBUG"):
        log.debug("Current bot info: %s", current_webhook_info)
    try:
        token = getenv("BOT_TOKEN")
        print(token)
        await bot.set_webhook(
            WEBHOOK_URL,
            secret_token=token.split(":")[1],
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            max_connections=40 if getenv("DEBUG") else 100,
        )
        if getenv("DEBUG"):
            log.debug("Updated bot info: %s", await check_webhook())
    except Exception as e:
        log.error("Can't set webhook - %s", e)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    update = Update.model_validate(update, context={"bot": bot})
    await dp.feed_update(bot, update)


@app.get('/logo.svg')
async def download_logo():
    logo_path = 'media/other_msg_cfg/main.svg'
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type='image/svg', filename='logo.svg')
    return {"error": "File not found!"}


@app.on_event("shutdown")
async def on_shutdown():
    pass

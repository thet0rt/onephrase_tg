from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Union
from log_settings import log


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[TelegramObject, Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[TelegramObject, Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        log.info(f'Received message from user={user_id}, ')
        print(type(event))
        print("Before handler")
        result = await handler(event, data)
        print("After handler")
        return result

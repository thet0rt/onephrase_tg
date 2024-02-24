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
        log.info('Received message from user = %s', user_id)
        try:
            result = await handler(event, data)
            log.debug("After handler, user_id = %s", user_id)
            return result
        except Exception as e:
            log.error('user_id= %s, exc=%s', user_id, e)
            log.debug("After handler, user_id = %s", user_id)

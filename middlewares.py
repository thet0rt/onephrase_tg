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
        log.debug(type(event))
        log.debug("Before handler")

        try:
            result = await handler(event, data)
            log.debug("After handler")
            return result
        except Exception as e:
            log.error(f'user_id={user_id}, exc={e}')
        log.debug("After handler")

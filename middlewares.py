from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, Update
from typing import Union
from log_settings import log
from aiogram.fsm.context import FSMContext
from utils.states import CurrentLogic


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[TelegramObject, Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[TelegramObject, Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        state: FSMContext = data.get('state')
        log.info('Received message from user = %s', user_id)
        if isinstance(event, CallbackQuery):
            update: Update = data.get('event_update')
            callback_data = update.callback_query.data
            if callback_data != 'input_order_number' and await state.get_state() == CurrentLogic.input_order_number:
                await state.set_state(CurrentLogic.basic)

        log.debug("Before handler, user_id = %s", user_id)
        try:
            result = await handler(event, data)
            log.debug("After handler, user_id = %s", user_id)
            return result
        except Exception as e:
            log.error('user_id= %s, exc=%s', user_id, e)
            log.debug("After handler, user_id = %s", user_id)

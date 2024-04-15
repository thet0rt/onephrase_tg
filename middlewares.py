from typing import Callable, Dict, Any, Awaitable
from typing import Union

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery, Update
from statsd import StatsClient

from log_settings import log
from utils.states import CurrentLogic

c = StatsClient('94.228.118.145', '8125', prefix='onephrase')


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
        c.incr('bot.event')
        if isinstance(event, CallbackQuery):
            update: Update = data.get('event_update')
            callback_data = update.callback_query.data
            # if callback_data not in ['back_to_price', 'back_to_menu']:
            #     await event.message.delete()
            if callback_data != 'input_order_number' and await state.get_state() == CurrentLogic.input_order_number:
                await state.set_state(CurrentLogic.basic)
            timer_name = f'bot.event.{callback_data}'
        else:
            timer_name = 'bot.event.other'
        log.debug("Before handler, user_id = %s", user_id)
        timer = c.timer(timer_name)
        timer_2 = c.timer('bot.all_events')
        try:
            timer.start()
            timer_2.start()
            result = await handler(event, data)
            log.debug("After handler, user_id = %s", user_id)
            timer.stop(send=False)
            timer_2.stop(send=False)
            timer.send()
            timer_2.send()
            return result
        except Exception as e:
            timer.stop(send=False)
            timer_2.stop(send=False)
            timer.send()
            timer_2.send()
            log.error('user_id= %s, exc=%s', user_id, e)
            log.debug("After handler, user_id = %s", user_id)

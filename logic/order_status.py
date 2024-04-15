from datetime import datetime as dt
from datetime import timedelta
from typing import Optional

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from db import get_from
from integration.cdek_methods import get_cdek_status
from integration.helpers import get_message_mapping_config
from integration.retailcrm_methods import get_orders_by_phone_number, get_orders_by_order_number
from integration.ruspost_methods import get_ruspost_status
from keyboards.for_order_status import get_no_new_orders_kb, get_no_old_orders_kb, get_after_order_status_kb, \
    get_after_order_history_kb, get_no_order_kb, get_after_order_number_kb
from log_settings import log


async def check_authorization(user_id: str) -> Optional[str]:
    phone_number = await get_from(user_id)
    return phone_number


def normalize_order_number(order_number: str) -> str:
    order_number = order_number.replace('А', 'A')
    order_number = order_number.replace('С', 'C')
    return order_number


async def show_order_by_order_number(message: Message, order_number: str):
    order_number = normalize_order_number(order_number)
    orders = await get_orders_by_order_number(order_number)
    if orders:
        if orders_info := await process_order_data(orders):
            for order_info in orders_info:
                await message.answer(
                    text=order_info, reply_markup=get_after_order_number_kb()
                )
            return

    await message.answer(
        text="🤔 Не нашли такого заказа, если вы считаете, "
             "что это ошибка – позовите менеджера, он проверит вручную.",
        reply_markup=get_no_order_kb(),
    )


async def show_actual_orders_query(callback_query: CallbackQuery, phone_number: str):
    await callback_query.answer()
    orders = await get_orders_by_phone_number(phone_number, "new")
    if not orders:
        await callback_query.message.answer(
            text="🤔 Не нашли активных заказов, если вы считаете, "
                 "что это ошибка – позовите менеджера, он проверит вручную.",
            reply_markup=get_no_new_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await callback_query.message.answer(
                text=order_info, reply_markup=ReplyKeyboardRemove()
            )
        await callback_query.message.answer(
            text="Вот всё, что мне удалось найти",
            reply_markup=get_after_order_status_kb(),
        )


async def show_actual_orders_msg(message: Message, phone_number: str):
    orders = await get_orders_by_phone_number(phone_number, "new")
    if not orders:
        await message.answer(
            text="🤔 Не нашли активных заказов, если вы считаете, "
                 "что это ошибка – позовите менеджера, он проверит вручную.",
            reply_markup=get_no_new_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Вот всё, что мне удалось найти",
            reply_markup=get_after_order_history_kb(),
        )


async def show_order_history_query(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_phone_number(phone_number, "old")
    if not orders:
        await callback_query.message.answer(
            text="Мы не нашли старых заказов.",
            reply_markup=get_no_old_orders_kb(),
        )
    else:
        await callback_query.answer(text="Проверяем историю заказов")
        orders_info = await process_completed_order(orders)
        for order_info in orders_info:
            await callback_query.message.answer(
                text=order_info, reply_markup=ReplyKeyboardRemove()
            )
        await callback_query.message.answer(
            text="Вот всё, что мне удалось найти",
            reply_markup=get_after_order_history_kb(),
        )


async def show_order_history_msg(message: Message, phone_number: str):
    orders = await get_orders_by_phone_number(phone_number, "old")
    if not orders:
        await message.answer(
            text="Мы не нашли старых заказов.",
            reply_markup=get_no_old_orders_kb(),
        )
    else:
        orders_info = await process_completed_order(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Вот всё, что мне удалось найти",
            reply_markup=get_after_order_status_kb(),
        )


async def process_order_data(order_data: list) -> list[str]:
    log.info(order_data)
    info_list = []
    config = get_message_mapping_config()
    for order in order_data:
        number = order.get("number")
        status = order.get("status")
        items = order.get("items")
        if not items:
            continue
        emoji = config.get(status, {}).get("emoji", "")
        order_number_msg = f"{emoji} Заказ №{number}"
        item_msg = get_item_list(items)
        status_msg = config.get(status, {}).get("status_msg")
        delivery_status_msg = await get_delivery_status_msg(order, status, config)
        message = (
            f"{order_number_msg}\n{status_msg}\n{item_msg}"
        )
        if delivery_status_msg:
            message += f'\n\n{delivery_status_msg}'
        info_list.append(message)
    return info_list


async def process_completed_order(order_data: list) -> list[str]:
    info_list = []
    config = get_message_mapping_config()
    for order in order_data:
        number = order.get("number")
        status = order.get("status")
        items = order.get("items")
        emoji = config.get(status, {}).get("emoji", "")
        order_number_msg = f"{emoji} Заказ №{number}"
        item_msg = get_item_list(items)
        status_msg = config.get(status, {}).get("status_msg")
        completion_time = get_completion_time(order)
        message = f"{order_number_msg}\n{status_msg}\n{item_msg}{completion_time}"
        info_list.append(message)
    return info_list


def get_noun(number, one='день', two='дня', five='дней'):
    n = abs(number)
    n %= 100
    if 5 <= n <= 20:
        return five
    n %= 10
    if n == 1:
        return one
    if 2 <= n <= 4:
        return two
    return five


def get_completion_time(order: dict) -> str:
    payment_date = order.get('customFields', {}).get('real_date_of_payment')
    shipment_date = order.get('shipmentDate')
    try:
        payment_date = dt.strptime(payment_date, '%Y-%m-%d')
        shipment_date = dt.strptime(shipment_date, '%Y-%m-%d')
        completion_days_delta = shipment_date - payment_date
        completion_days = completion_days_delta.days
        day_noun = get_noun(completion_days)
        completion_time = f'\n\nЗаказ выполнен и передан в службу доставки за {completion_days} {day_noun}'
        return completion_time
    except TypeError as exc:
        log.error('Error while getting completion_time exc=%s', exc)
        return ''



def get_item_list(items: list) -> str:
    items_description = "\nСостав заказа:"
    for count, item in enumerate(items, 1):
        name = item.get("offer", {}).get("displayName")
        quantity = item.get("quantity")
        items_description += f"\n{count}. {name} - {quantity} шт."
    return items_description


async def get_delivery_status_msg(order: dict, status, config) -> str:
    if status in [
        'website-order',
        'not-ready'
    ]:
        return await get_dispatch_msg_alternative(order, config, status)
    elif status in [
        'delay-new',
        "emb",
    ]:
        return await get_dispatch_msg_special(order, config, status)

    elif status in [
        "assembling",
        "fail-gotov",
        "assembling-complete",
        "v-rabote",
        "pack-no-track-number",
        "pack",
        "ready",
    ]:
        return await get_dispatch_msg(config, status)
    elif status in [
        "send-to-delivery",
        "delivering",
        "redirect",
        "ready-for-self-pickup",
        "arrived-in-pickup-point",
        "vozvrat-otpravleniia",
    ]:
        delivery_type = order.get("delivery", {}).get("code")
        if delivery_type == "sdek-v-2":
            delivery_msg = await get_cdek_msg(order)
            return delivery_msg
        elif delivery_type == 'pochta-rossii-treking-tarifikator':
            delivery_msg = await get_ruspost_msg(order)
            return delivery_msg
        elif delivery_type == 'self-delivery':
            return ''
        else:
            log.warning("Delivery type not in [sdek-v-2, pochta-rossii-treking-tarifikator,"
                        " self-delivery, self-delivery] order=%s",
                        order.get('number'))


async def get_cdek_msg(order: dict) -> Optional[str]:
    cdek_uuid = order.get("delivery", {}).get("data", {}).get("externalId")
    track_number = order.get("delivery", {}).get("data", {}).get("trackNumber")
    cdek_status = await get_cdek_status(cdek_uuid)
    delivery_status = cdek_status.get("status")
    planned_date = cdek_status.get("planned_date")
    if not delivery_status or not planned_date:
        log.error('Something is wrong with cdek_status = %s', cdek_status)
        return ""
    delivery_msg = (f"\nТип доставки: СДЭК"
                    f"\nТрек-номер для отслеживания: {track_number}"
                    f"\nСтатус доставки: {delivery_status}"
                    f"\nОриентировочная дата прибытия: {planned_date}")
    return delivery_msg


async def get_ruspost_msg(order: dict) -> Optional[str]:
    ruspost_tracking_number = order.get("delivery", {}).get("data", {}).get("trackNumber")
    ruspost_status = await get_ruspost_status(ruspost_tracking_number)
    delivery_status = ruspost_status.get("status")
    planned_date = ruspost_status.get("planned_date")
    if not delivery_status:
        log.error('Something is wrong with ruspost = %s', ruspost_status)
        return ""
    delivery_msg = (f"\nТип доставки: Почта России"
                    f"\nТрек-номер для отслеживания: {ruspost_tracking_number}"
                    f"\nСтатус доставки: {delivery_status}")
    if planned_date:
        delivery_msg += f"\nОриентировочная дата прибытия: {planned_date}"

    return delivery_msg


async def get_dispatch_msg(config: dict, status: str) -> str:
    days_count = config.get(status).get("days_count")
    if days_count == 0:
        return ''
    sending_date_1 = dt.now() + timedelta(days=config.get(status).get("days_count")[0])
    sending_date_2 = dt.now() + timedelta(days=config.get(status).get("days_count")[1])
    sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
    sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
    return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"


async def get_dispatch_msg_alternative(order: dict, config: dict, status: str) -> str:
    real_date_of_payment = order.get('customFields', {}).get('real_date_of_payment')
    if not real_date_of_payment:
        log.error("Something is wrong with real_date_of_payment order= %s", order.get('number'))
        return ''
    real_date_of_payment = dt.strptime(real_date_of_payment, '%Y-%m-%d')

    sending_date_1 = real_date_of_payment + timedelta(days=config.get(status).get("days_count")[0])
    sending_date_2 = real_date_of_payment + timedelta(days=config.get(status).get("days_count")[1])
    sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
    sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
    return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"


async def get_dispatch_msg_special(order: dict, config: dict, status: str) -> str:
    real_date_of_payment = order.get('customFields', {}).get('real_date_of_payment')
    if not real_date_of_payment:
        log.error("Something is wrong with real_date_of_payment order= %s", order.get('number'))
        return ''
    real_date_of_payment = dt.strptime(real_date_of_payment, '%Y-%m-%d')
    today = dt.now()
    days_since = (today - real_date_of_payment).days
    if days_since <= 5:
        sending_date_1 = real_date_of_payment + timedelta(days=config.get(status).get("days_count")[0])
        sending_date_2 = real_date_of_payment + timedelta(days=config.get(status).get("days_count")[1])
        sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
        sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
        return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"
    return "Ориентировочная дата отправки: на уточнении, позвали менеджера для проверки срока отправки"

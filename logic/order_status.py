from datetime import datetime as dt
from datetime import timedelta
from typing import Optional

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from db import get_from
from integration.cdek_methods import get_cdek_status
from integration.helpers import get_message_mapping_config
from integration.retailcrm_methods import get_orders_by_number
from keyboards.for_order_status import get_no_orders_kb, get_after_order_status_kb


async def check_authorization(user_id: str) -> Optional[str]:
    phone_number = await get_from(user_id)
    return phone_number


async def show_actual_orders_query(callback_query: CallbackQuery, phone_number: str):
    await callback_query.answer()
    orders = await get_orders_by_number(phone_number, "new")
    print(orders)
    if not orders:
        await callback_query.message.answer(
            text="🤔 Не нашли активных заказов, если вы считаете, "
            "что это ошибка – позовите менеджера, он проверит вручную.",
            reply_markup=get_no_orders_kb(),
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
    orders = await get_orders_by_number(phone_number, "new")
    print(orders)
    if not orders:
        await message.answer(
            text="🤔 Не нашли активных заказов, если вы считаете, "
            "что это ошибка – позовите менеджера, он проверит вручную.",
            reply_markup=get_no_orders_kb(),
        )
    else:
        orders_info = await process_order_data(orders)
        for order_info in orders_info:
            await message.answer(text=order_info, reply_markup=ReplyKeyboardRemove())
        await message.answer(
            text="Вот всё, что мне удалось найти",
            reply_markup=get_after_order_status_kb(),
        )


async def show_order_history_query(callback_query: CallbackQuery, phone_number: str):
    orders = await get_orders_by_number(phone_number, "old")
    if not orders:
        await callback_query.message.answer(
            text="Мы не нашли старых заказов.",
            reply_markup=get_no_orders_kb(),
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
            reply_markup=get_after_order_status_kb(),
        )


async def show_order_history_msg(message: Message, phone_number: str):
    orders = await get_orders_by_number(phone_number, "old")
    if not orders:
        await message.answer(
            text="Мы не нашли старых заказов.",
            reply_markup=get_no_orders_kb(),
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
        delivery_status_msg = await get_delivery_status_msg(order, status, config)
        message = (
            f"{order_number_msg}\n{status_msg}\n{item_msg}\n\n{delivery_status_msg}"
        )
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
        message = f"{order_number_msg}\n{status_msg}\n{item_msg}"
        info_list.append(message)
    return info_list


def get_item_list(items: list) -> str:
    items_description = "\nСостав заказа:"
    for count, item in enumerate(items, 1):
        name = item.get("offer", {}).get("displayName")
        quantity = item.get("quantity")
        items_description += f"\n{count}. {name} - {quantity} шт."
    return items_description


async def get_delivery_status_msg(order: dict, status, config) -> str:
    if status in [
        "assembling",
        "fail-gotov",
        "assembling-complete",
        "emb",
        "v-rabote",
        "pack-no-track-number",
        "pack",
        "ready",
    ]:
        return await get_dispatch_msg(config, status)
    if status in [
        "send-to-delivery",
        "delivering",
        "redirect",
        "ready-for-self-pickup",
        "arrived-in-pickup-point",
        "vozvrat-otpravleniia",
    ]:
        if order.get("delivery", {}).get("code") == "sdek-v-2":
            delivery_msg = await get_cdek_msg(order)
            return delivery_msg


async def get_cdek_msg(order: dict) -> Optional[str]:
    cdek_uuid = order.get("delivery", {}).get("data", {}).get("externalId")
    cdek_status = await get_cdek_status(cdek_uuid)
    delivery_status = cdek_status.get("status")
    planned_date = cdek_status.get("planned_date")
    if not delivery_status or not planned_date:
        print(
            f"Something is wrong with cdek_status={cdek_status}"
        )  # todo change to logging
        return ""
    delivery_msg = f"\nСтатус доставки: {delivery_status}\nОриентировочная дата прибытия: {planned_date}"
    return delivery_msg


async def get_dispatch_msg(config: dict, status: str) -> str:
    sending_date_1 = dt.now() + timedelta(days=config.get(status).get("days_count")[0])
    sending_date_2 = dt.now() + timedelta(days=config.get(status).get("days_count")[1])
    sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
    sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
    return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"


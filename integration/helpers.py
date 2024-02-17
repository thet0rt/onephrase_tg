from datetime import datetime as dt
from datetime import timedelta
from typing import Optional

from .cdek_methods import get_cdek_status


def get_status_filters(actuality: str) -> str:
    filters = ""
    if actuality == "new":
        for status_code in get_message_mapping_config(codes_only=True):
            filters += f"&filter[extendedStatus][]={status_code}"
    elif actuality == "old":
        filters += f"&filter[extendedStatus][]=complete"
    print(filters)
    return filters


async def get_cdek_msg(order: dict) -> Optional[str]:
    cdek_uuid = order.get("delivery", {}).get("data", {}).get("externalId")
    cdek_status = await get_cdek_status(cdek_uuid)
    delivery_status = cdek_status.get("status")
    planned_date = cdek_status.get("planned_date")
    if not delivery_status or not planned_date:
        print(
            f"Something is wrong with cdek_status={cdek_status}"
        )  # todo change to logging
        return
    delivery_msg = f"\nСтатус доставки: {delivery_status}\nОриентировочная дата прибытия: {planned_date}"
    return delivery_msg


async def get_dispatch_msg(config: dict, status: str) -> str:
    sending_date_1 = dt.now() + timedelta(days=config.get(status).get("days_count")[0])
    sending_date_2 = dt.now() + timedelta(days=config.get(status).get("days_count")[1])
    sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
    sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
    return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"


def get_message_mapping_config(
        codes_only: bool = False,
) -> dict:  # todo change to real db later
    config = {
        "website-order": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳"
        },
        "not_ready": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳"

        },
        "sertifivate": {"status_msg": "-", "days_count": 7 - 10,
                        "emoji": "⏳"},
        "delay-new": {
            "status_msg": "Ваш заказ в очереди на изготовление,"
                          "может быть небольшая задержка",
            "days_count": 0,
            "emoji": "⏳"
        },
        "product-booking-new": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": 0,
            "emoji": "⏳"
        },
        "assembling": {"status_msg": "Ваш заказ изготавливается", "days_count": (3, 5)},
        "fail-gotov": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳"
        },
        "assembling-complete": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳"
        },
        "emb": {"status_msg": "Ваш заказ изготоваливается", "days_count": (3, 5)},
        "v-rabote": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (2, 3),
            "emoji": "⏳"
        },
        "pack-no-track-number": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе,"
                          " осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳"
        },
        "pack": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳"
        },
        "ready": {
            "status_msg": "Заказ передан курьеру и скоро начнет движение к вам",
            "days_count": (1, 2),
            "emoji": "⏳"
        },
        "sent-to-delivery": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛"
        },
        "delivering": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛"
        },
        "redirect": {"status_msg": "Заказ готов и передан в доставку", "days_count": 0},
        "ready-for-self-pickup": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "✅"
        },
        "arrived-in-pickup-point": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛"
        },
        "vozvrat-otpravleniia": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛"
        },
        "complete": {
            "status_msg": "Получен.",
            "days_count": 0,
            "emoji": "✅"
        },
    }
    return config.keys() if codes_only else config


async def process_order_data(order_data: list) -> list[str]:
    info_list = []
    config = get_message_mapping_config()
    for order in order_data:
        number = order.get("number")
        status = order.get("status")
        items = order.get("items")
        emoji = config.get(status, {}).get('emoji', '')
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
        emoji = config.get(status, {}).get('emoji', '')
        order_number_msg = f"{emoji} Заказ №{number}"
        item_msg = get_item_list(items)
        status_msg = config.get(status, {}).get("status_msg")
        message = (
            f"{order_number_msg}\n{status_msg}\n{item_msg}"
        )
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

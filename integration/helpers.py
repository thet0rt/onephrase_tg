from datetime import datetime as dt
from datetime import timedelta
from .cdek_methods import get_cdek_status


def get_status_filters() -> str:
    filters = ""
    for status_code in get_message_mapping_config(codes_only=True):
        filters += f"&filter[extendedStatus][]={status_code}"
    return filters


def get_message_mapping_config(
    codes_only: bool = False,
) -> dict:  # todo change to real db later
    config = {
        "website-order": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
        },
        "not_ready": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
        },
        "sertifivate": {"status_msg": "-", "days_count": 7 - 10},
        "delay-new": {
            "status_msg": "Ваш заказ в очереди на изготовление,"
            "может быть небольшая задержка",
            "days_count": 0,
        },
        "product-booking-new": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": 0,
        },
        "assembling": {"status_msg": "Ваш заказ изготавливается", "days_count": (3, 5)},
        "fail-gotov": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
        },
        "assembling-complete": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
        },
        "emb": {"status_msg": "Ваш заказ изготоваливается", "days_count": (3, 5)},
        "v-rabote": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (2, 3),
        },
        "pack-no-track-number": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе,"
            " осталось подготовить вещи к отправке",
            "days_count": (1, 2),
        },
        "pack": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (1, 2),
        },
        "ready": {
            "status_msg": "Заказ передан курьеру и скоро начнет движение к вам",
            "days_count": (1, 2),
        },
        "sent-to-delivery": {"status_msg": "", "days_count": 0},  # todo later
        "delivering": {"status_msg": "", "days_count": 0},
        "redirect": {"status_msg": "", "days_count": 0},
        "ready-for-self-pickup": {"status_msg": "", "days_count": 0},
        "arrived-in-pickup-point": {"status_msg": "", "days_count": 0},
        "vozvrat-otpravleniia": {"status_msg": "", "days_count": 0},
        "complete": {"status_msg": "", "days_count": 0},
    }
    return config.keys() if codes_only else config


def process_order_data(order_data: list) -> list[str]:
    info_list = []
    config = get_message_mapping_config()
    for order in order_data:
        number = order.get("number")
        status = order.get("status")
        items = order.get("items")
        order_number_msg = f"Заказ №{number}"
        item_msg = get_item_list(items)
        status_msg = config.get(status, {}).get("status_msg")
        delivery_status_msg = get_delivery_status_msg(order, status, config)
        message = (
            f"{order_number_msg}\n{status_msg}\n{item_msg}\n\n{delivery_status_msg}"
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


def get_delivery_status_msg(order: dict, status, config) -> str:
    # if order.get('delivery', {}).get('integration_code') == 'sdek-v-2':
    #     return
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
        sending_date_1 = dt.now() + timedelta(
            days=config.get(status).get("days_count")[0]
        )
        sending_date_2 = dt.now() + timedelta(
            days=config.get(status).get("days_count")[1]
        )
        sending_date_1 = sending_date_1.strftime("%d.%m.%Y")
        sending_date_2 = sending_date_2.strftime("%d.%m.%Y")
        return f"Ориентировочная дата отправки {sending_date_1} - {sending_date_2}"
    if status in [
        "send-to-delivery",
        "delivering",
        "redirect",
        "ready-for-self-pickup",
        "arrived-in-pickup-point",
        "vozvrat-otpravleniia",
    ]:
        if order.get("delivery", {}).get("code") == "sdek-v-2":
            cdek_uuid = order.get("delivery", {}).get("data", {}).get("externalId")
            cdek_status = get_cdek_status(cdek_uuid)
            delivery_msg = f""
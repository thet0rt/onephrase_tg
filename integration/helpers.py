def get_status_filters(actuality: str) -> str:
    filters = ""
    if actuality == "new":
        for status_code in get_message_mapping_config(codes_only=True):
            filters += f"&filter[extendedStatus][]={status_code}"
    elif actuality == "old":
        filters += f"&filter[extendedStatus][]=complete"
    print(filters)
    return filters


def get_message_mapping_config(
    codes_only: bool = False,
) -> dict:  # todo change to real db later
    config = {
        "website-order": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳",
        },
        "not_ready": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳",
        },
        "sertifivate": {"status_msg": "-", "days_count": 7 - 10, "emoji": "⏳"},
        "delay-new": {
            "status_msg": "Ваш заказ в очереди на изготовление,"
            "может быть небольшая задержка",
            "days_count": 0,
            "emoji": "⏳",
        },
        "product-booking-new": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": 0,
            "emoji": "⏳",
        },
        "assembling": {"status_msg": "Ваш заказ изготавливается", "days_count": (3, 5)},
        "fail-gotov": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳",
        },
        "assembling-complete": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳",
        },
        "emb": {"status_msg": "Ваш заказ изготоваливается", "days_count": (3, 5)},
        "v-rabote": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (2, 3),
            "emoji": "⏳",
        },
        "pack-no-track-number": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе,"
            " осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳",
        },
        "pack": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳",
        },
        "ready": {
            "status_msg": "Заказ передан курьеру и скоро начнет движение к вам",
            "days_count": (1, 2),
            "emoji": "⏳",
        },
        "sent-to-delivery": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
        },
        "delivering": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
        },
        "redirect": {"status_msg": "Заказ готов и передан в доставку", "days_count": 0},
        "ready-for-self-pickup": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "✅",
        },
        "arrived-in-pickup-point": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
        },
        "vozvrat-otpravleniia": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
        },
        "complete": {"status_msg": "Получен.", "days_count": 0, "emoji": "✅"},
    }
    return config.keys() if codes_only else config

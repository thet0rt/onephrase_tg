from log_settings import log


def get_status_filters(actuality: str) -> str:
    filters = ""
    if actuality == "new":
        for status_code in get_message_mapping_config(codes_only=True, categories=('active', 'delivery')):
            filters += f"&filter[extendedStatus][]={status_code}"
    elif actuality == "old":
        for status_code in get_message_mapping_config(codes_only=True, categories=('done',)):
            filters += f"&filter[extendedStatus][]={status_code}"
    log.debug('filters= %s', filters)
    return filters


def get_message_mapping_config(
        codes_only: bool = False, categories: tuple = ()
) -> dict:  # todo change to real db later
    config = {
        "website-order": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳",
            'category': 'active'
        },
        "not_ready": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": (5, 7),
            "emoji": "⏳",
            'category': 'active'
        },
        "sertifivate": {"status_msg": "-", "days_count": 7 - 10, "emoji": "⏳"},
        "delay-new": {
            "status_msg": "Ваш заказ в очереди на изготовление,"
                          "может быть небольшая задержка",
            "days_count": 0,
            "emoji": "⏳",
            'category': 'active'
        },
        "product-booking-new": {
            "status_msg": "Ваш заказ в очереди на выполнение",
            "days_count": 0,
            "emoji": "⏳",
            'category': 'active'
        },
        "assembling": {
            "status_msg": "Ваш заказ изготавливается", "days_count": (3, 5),
            "emoji": "⏳",
            'category': 'active'},
        "fail-gotov": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳",
            'category': 'active'
        },
        "assembling-complete": {
            "status_msg": "Ваш заказ изготоваливается",
            "days_count": (3, 5),
            "emoji": "⏳",
            'category': 'active'
        },
        "emb": {"status_msg": "Ваш заказ изготоваливается", "days_count": (3, 5), 'emoji': "⏳", 'category': 'active'},
        "v-rabote": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (2, 3),
            "emoji": "⏳",
            'category': 'active'
        },
        "pack-no-track-number": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе,"
                          " осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳",
            'category': 'active'
        },
        "pack": {
            "status_msg": "Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке",
            "days_count": (1, 2),
            "emoji": "⏳",
            'category': 'active'
        },
        "ready": {
            "status_msg": "Заказ передан курьеру и скоро начнет движение к вам",
            "days_count": (1, 2),
            "emoji": "⏳",
            'category': 'active'
        },
        "send-to-delivery": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
            'category': 'delivery'
        },
        "delivering": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
            'category': 'delivery'
        },
        "redirect": {"status_msg": "Заказ готов и передан в доставку", "days_count": 0},
        "ready-for-self-pickup": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "✅",
            'category': 'delivery'
        },
        "arrived-in-pickup-point": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
            'category': 'delivery'
        },
        "vozvrat-otpravleniia": {
            "status_msg": "Заказ готов и передан в доставку",
            "days_count": 0,
            "emoji": "🚛",
            'category': 'delivery'
        },
        "complete": {"status_msg": "Получен.", "days_count": 0, "emoji": "✅", 'category': 'done'},
        "sold": {"status_msg": "Получен.", "days_count": 0, "emoji": "✅", 'category': 'done'},
    }
    codes = {key for key, val in config.items() if val.get('category') in categories}
    return codes if codes_only else config

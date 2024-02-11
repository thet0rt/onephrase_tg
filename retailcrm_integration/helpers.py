def get_status_filters() -> str:
    filters = ''
    for status_code in get_codes_from_db():
        filters += f'&filter[extendedStatus][]={status_code}'
    return filters


def get_codes_from_db() -> list:  # todo change to real db later
    return ['website-order', 'not_ready', 'sertifivate', 'delay-new', 'product-booking-new', 'assembling',
            'fail-gotov', 'assembling-complete', 'emb', 'v-rabote', 'pack-no-track-number', 'pack', 'ready',
            'sent-to-delivery', 'delivering', 'redirect', 'ready-for-self-pickup', 'arrived-in-pickup-point',
            'vozvrat-otpravleniia', 'complete']


def process_order_data(order_data: dict) -> list[str]:
    print(order_data)
    return ['1', '2']

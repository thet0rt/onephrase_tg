def get_status_filters() -> str:
    filters = ''
    for status_code in get_message_mapping_config(codes_only=True):
        filters += f'&filter[extendedStatus][]={status_code}'
    return filters


def get_message_mapping_config(codes_only: bool = False) -> dict:  # todo change to real db later
    config = {'website-order': {'status_msg': 'Ваш заказ в очереди на выполнение', 'days_count': (5, 7)},
              'not_ready': {'status_msg': 'Ваш заказ в очереди на выполнение', 'days_count': (5, 7)},
              'sertifivate': {'status_msg': '-', 'days_count': 7-10},
              'delay-new': {'status_msg': 'Ваш заказ в очереди на изготовление,'
                                          'может быть небольшая задержка', 'days_count': 0},
              'product-booking-new': {'status_msg': 'Ваш заказ в очереди на выполнение', 'days_count': 0},
              'assembling': {'status_msg': 'Ваш заказ изготавливается', 'days_count': (3, 5)},
              'fail-gotov': {'status_msg': 'Ваш заказ изготоваливается', 'days_count': (3, 5)},
              'assembling-complete': {'status_msg': 'Ваш заказ изготоваливается', 'days_count': (3, 5)},
              'emb': {'status_msg': 'Ваш заказ изготоваливается', 'days_count': (3, 5)},
              'v-rabote': {'status_msg': 'Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке',
                           'days_count': (2, 3)},
              'pack-no-track-number': {'status_msg': 'Мы уже сделали вышивку на вашем заказе,'
                                                     ' осталось подготовить вещи к отправке', 'days_count': (1, 2)},
              'pack': {'status_msg': 'Мы уже сделали вышивку на вашем заказе, осталось подготовить вещи к отправке',
                       'days_count': (1, 2)},
              'ready': {'status_msg': 'Заказ передан курьеру и скоро начнет движение к вам', 'days_count': (1, 2)},
              'sent-to-delivery': {'status_msg': '', 'days_count': 0},  # todo later
              'delivering': {'status_msg': '', 'days_count': 0}, 'redirect': {'status_msg': '', 'days_count': 0},
              'ready-for-self-pickup': {'status_msg': '', 'days_count': 0},
              'arrived-in-pickup-point': {'status_msg': '', 'days_count': 0},
              'vozvrat-otpravleniia': {'status_msg': '', 'days_count': 0},
              'complete': {'status_msg': '', 'days_count': 0}}
    return config.keys() if codes_only else config


def process_order_data(order_data: list) -> list[str]:
    info_list = []
    config = get_message_mapping_config()
    for order in order_data:
        number = order.get('number')
        status = order.get('status')
        items = order.get('items')
        order_number_msg = f'Заказ №{number}'
        status_msg = config.get('status', {}).get('status_msg')
        delivery_status_msg = get_delivery_status_msg(order)
        ''


def get_item_list(items: list) -> str:
    items_description = '\nСостав заказа:'
    for count, item in enumerate(items, 1):
        name = item.get('offer', {}).get('displayName')
        quantity = item.get('quantity')
        items_description += f'\n{count}. {name} - {quantity} шт.'
    return items_description


def get_delivery_status_msg(order: dict) -> str:
    if order.get('delivery', {}).get('integration_code') == 'sdek-v-2':
        return

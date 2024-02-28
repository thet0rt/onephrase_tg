from log_settings import log
from configuration import DELIVERY_MSG_CFG


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
) -> dict:

    codes = {key for key, val in DELIVERY_MSG_CFG.items() if val.get('category') in categories}
    return codes if codes_only else DELIVERY_MSG_CFG

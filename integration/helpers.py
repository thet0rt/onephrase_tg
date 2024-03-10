import os
from io import BytesIO

import aiohttp

from configuration import DELIVERY_MSG_CFG
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
) -> dict:
    codes = {key for key, val in DELIVERY_MSG_CFG.items() if val.get('category') in categories}
    return codes if codes_only else DELIVERY_MSG_CFG


async def upload_photo_to_server(file_io, file_name):
    url = os.getenv('UPLOAD_PHOTO_URL')

    async with aiohttp.ClientSession() as session:
        try:
            with BytesIO(file_io.getvalue()) as f:
                photo_bytes = f.read()
            files = {'file': photo_bytes, 'file_name': '' or file_name}
            async with session.post(url, data=files, raise_for_status=True) as response:
                return await response.text()
        except Exception as e:
            log.error('Error while uploading photo to yourcstm.space, exc = %s', e)
            return

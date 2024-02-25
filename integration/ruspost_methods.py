import os

import aiohttp
from log_settings import log


RUSPOST_TOKEN = os.getenv("RUSPOST_TOKEN")
RUSPOST_KEY = os.getenv("RUSPOST_KEY")


async def get_ruspost_order_info(ext_order_id) -> dict:
    url = f'https://www.pochta.ru/api/tracking/api/v1/trackings/by-barcodes?language=ru&track-numbers={ext_order_id}'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "Authorization": "AccessToken " + RUSPOST_TOKEN,
        "X-User-Authorization": "Basic " + RUSPOST_KEY
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    url, headers=headers, raise_for_status=True
            ) as response:
                response = await response.json()
                log.debug('Ruspost response = %s', response)
                return response
        except Exception as e:
            log.error('Error while making ruspost request e= %s', e)
            return {}


async def get_ruspost_status(ruspost_tracking_number) -> dict:
    ruspost_status = {"status": None, "planned_date": None}
    log.debug('ruspost_tracking_number = %s', ruspost_tracking_number)
    order_info = await get_ruspost_order_info(ruspost_tracking_number)
    try:
        status_info = order_info.get('detailedTrackings', {})[0].get('trackingItem')
        status = status_info.get('commonStatus')
        expected_delivery_date = status_info.get('shipmentTripInfo', {}).get('expectedDeliveryDate')
        if expected_delivery_date:
            expected_delivery_date = expected_delivery_date[:10]
            log.debug('Expected_delivery_date = %s', expected_delivery_date)
            ruspost_status.update(
                status=status,
                planned_date=expected_delivery_date
            )
        log.debug('ruspost_status=%s', ruspost_status)
    except (TypeError, IndexError, AttributeError) as e:
        log.error('Error while getting ruspost stastus, exc = %s', e)
    return ruspost_status

import os
from typing import Optional

import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv("../.env")  # todo delete later

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
                print(response.text)
                response = await response.json()
                return response
        except Exception as e:
            print(e)
            return {}


async def get_ruspost_status(ruspost_tracking_number) -> dict:
    ruspost_status = {"status": None, "planned_date": None}
    print(ruspost_tracking_number)
    order_info = await get_ruspost_order_info(ruspost_tracking_number)
    try:
        status_info = order_info.get('detailedTrackings', {})[0].get('trackingItem')
        status = status_info.get('commonStatus')
        expected_delivery_date = status_info.get('shipmentTripInfo', {}).get('expectedDeliveryDate')[:10]
        ruspost_status.update(
            status=status,
            planned_date=expected_delivery_date
        )
        print(ruspost_status)
    except (IndexError, AttributeError) as e:
        print(e)
        pass  # todo logging
    return ruspost_status


# async def main():
#     response = await get_ruspost_order_info('80081292072278')
#     print(response)
#
# asyncio.run(main())

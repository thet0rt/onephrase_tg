from os import getenv
from .helpers import get_status_filters
import aiohttp
from typing import Optional

SUBDOMAIN = getenv("SUB_DOMAIN")
TOKEN = getenv("RETAIL_CRM_TOKEN")


async def get_orders_by_number(phone: str) -> Optional[list]:
    url = f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders?filter[customer]={phone}{get_status_filters()}"

    headers = {"X-API-KEY": TOKEN}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, raise_for_status=True) as response:
                response = await response.json()
                if not response.get('success') or not response.get('orders'):
                    return
                print(response)
                print(response.get('orders'))  # todo delete
                return response.get('orders')
        except Exception as e:
            return  # todo logging

from os import getenv
from .helpers import get_status_filters
import aiohttp

SUBDOMAIN = getenv("SUB_DOMAIN")
TOKEN = getenv("RETAIL_CRM_TOKEN")


async def get_orders_by_number(phone: str) -> dict:
    url = f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders?filter[customer]={phone}{get_status_filters()}"

    headers = {"X-API-KEY": TOKEN}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            if not response.get('success') or not response.get('orders'):
                return
            print(response)
            print(response.get('orders'))  # todo delete
            return response.get('orders')

from os import getenv
from .helpers import get_status_filters
import aiohttp
from typing import Optional
from log_settings import log

SUBDOMAIN = getenv("SUB_DOMAIN")
TOKEN = getenv("RETAIL_CRM_TOKEN")


async def get_orders_by_number(
    phone: str, actuality: str
) -> Optional[list]:  # todo обработка ошибок. Сделать ретрай
    url = f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders?filter[customer]={phone}{get_status_filters(actuality)}"
    log.debug('url = %s', url)
    headers = {"X-API-KEY": TOKEN}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, headers=headers, raise_for_status=True
            ) as response:
                response = await response.json()
                if not response.get("success") or not response.get("orders"):
                    return
                log.debug(response)
                return response.get("orders")
        except Exception as e:
            log.error(e)
            return

from os import getenv
from .helpers import get_status_filters
import aiohttp
from typing import Optional
from log_settings import log

SUBDOMAIN = getenv("SUB_DOMAIN")
TOKEN = getenv("RETAIL_CRM_TOKEN")


async def get_orders_by_phone_number(
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
                return response.get("orders")
        except Exception as e:
            log.error('Error while getting order_info from CRM, exc = %s', e)
            return


async def get_orders_by_order_number(order_number: str) -> Optional[list]:  # todo обработка ошибок. Сделать ретрай
    # todo сделать небольшой таймаут, чтоб пользователи не ждали долго
    url = f"https://{SUBDOMAIN}.retailcrm.ru/api/v5/orders?filter[numbers][]={order_number}"
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
                return response.get("orders")
        except Exception as e:
            log.error('Error while getting order_info from CRM, exc = %s', e)
            return

import os
from typing import Optional

import aiohttp
from dotenv import load_dotenv

from db import get_from, set_to
from log_settings import log

load_dotenv("../.env")  # todo delete later

CDEK_CLIENT_ID = os.getenv("CDEK_CLIENT_ID")
CDEK_CLIENT_SECRET = os.getenv("CDEK_CLIENT_SECRET")


async def get_cdek_token():
    url = "https://api.cdek.ru/v2/oauth/token?parameters"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": CDEK_CLIENT_ID,
                    "client_secret": CDEK_CLIENT_SECRET,
                },
                headers=headers,
                raise_for_status=True,
            ) as response:
                response = await response.json()
                access_token = response.get("access_token")
                log.debug(response)
                await set_to("cdek_token", access_token, 3500)
                return access_token
        except Exception as e:
            log.error(e)
            return


async def get_cdek_order_info(cdek_uuid) -> Optional[dict]:
    cdek_token = await get_from("cdek_token") or await get_cdek_token()
    url = f"https://api.cdek.ru/v2/orders/{cdek_uuid}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {cdek_token}",
        "content-type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, headers=headers, raise_for_status=True
            ) as response:
                response = await response.json()
                log.debug(response)
                return response
        except Exception as e:
            log.error(e)
            return


async def get_cdek_status(cdek_uuid) -> dict:
    cdek_status = {"status": None, "planned_date": None}
    order_info = await get_cdek_order_info(cdek_uuid)
    log.debug(order_info)
    status_list = order_info.get("entity", {}).get(
        "statuses"
    )  # todo проверить если несколько packages
    if status_list:
        cdek_status.update(status=status_list[0].get("name"))
    cdek_status.update(
        planned_date=order_info.get("entity", {}).get("planned_delivery_date")
    )
    return cdek_status

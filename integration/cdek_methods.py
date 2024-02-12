import os
from typing import Optional

import aiohttp
import asyncio
from dotenv import load_dotenv

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
                return response.get("access_token")
        except Exception as e:
            print(e)
            return  # todo add logging


async def get_cdek_order_info(cdek_uuid) -> Optional[dict]:
    cdek_token = await get_cdek_token()  # todo change to redis
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
                return response
        except Exception as e:
            print(e)
            return  # todo add logging


async def get_cdek_status(cdek_uuid) -> dict:
    cdek_status = {"status": None, "planned_date": None}
    order_info = await get_cdek_order_info(cdek_uuid)
    status_list = order_info.get("statuses")
    if status_list:
        cdek_status.update(status=status_list[0].get("name"))
    cdek_status.update(planned_date=order_info.get("planned_delivery_date"))
    return cdek_status


#
# async def main():
#     response = await get_cdek_order_info(cdek_uuid='72753032-5f07-464c-a1b1-c8281678718d')
#     print(response)
#
# asyncio.run(main())

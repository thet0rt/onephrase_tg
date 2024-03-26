import asyncio
import os
import pathlib
import time
from collections import namedtuple
from functools import wraps
from json import load

import aiohttp
import gspread
from gspread import Spreadsheet

from log_settings import log

PhotoData = namedtuple('PhotoData', ['path', 'link'])


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log.debug(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


@timeit
def get_spreadsheet() -> Spreadsheet:
    with open('google_creds.json', 'r') as creds_file:
        google_creds = load(creds_file)

    gc = gspread.service_account_from_dict(google_creds)
    sh = gc.open_by_key(os.getenv('SPREADSHEET_CODE'))
    return sh


@timeit
def get_msg_config(sh: Spreadsheet) -> dict:
    msg_config = {}
    for config_name in ['price_msg_cfg', 'colors_msg_cfg', 'qa_msg_cfg']:
        worksheet = sh.worksheet(config_name)
        ws_data = worksheet.batch_get(['B2:E50'])[0]
        config = {}
        for data in ws_data[1:]:
            position = data[0]
            config[position] = {'button_name': data[1],
                                'msg': data[2],
                                'photo_link': data[3],
                                'photo_path': f'media/{config_name}/{position}.jpg'}
            pathlib.Path(f'media/{config_name}').mkdir(exist_ok=True, parents=True)  # пришлось пока вставить это сюда
        msg_config.update({worksheet.title: config})
    return msg_config


@timeit
def get_business_config(sh: Spreadsheet) -> dict:
    worksheet = sh.worksheet('business_msg_cfg')
    ws_data = worksheet.batch_get(['B2:D50'])[0]
    config = {}
    for data in ws_data[1:]:
        config[data[0]] = {'button_name': data[1],
                           'msg': data[2]}
    return config


@timeit
def get_delivery_msg_cfg(sh: Spreadsheet) -> dict:
    config = {}
    worksheet = sh.worksheet('delivery_msg_cfg')
    ws_data = worksheet.batch_get(['B2:F50'])[0]
    for data in ws_data[1:]:
        days_count = data[2]
        if '-' in days_count:
            days_count = tuple([int(x) for x in days_count.split('-')])
        else:
            days_count = int(days_count)
        config[data[0]] = {'status_msg': data[1],
                           'days_count': days_count,
                           'emoji': data[3],
                           'category': data[4]}
    return config


def get_other_msg_cfg(sh: Spreadsheet) -> dict:
    config = {}
    worksheet = sh.worksheet('other_msg_cfg')
    ws_data = worksheet.batch_get(['B2:D50'])[0]
    for data in ws_data[1:]:
        button_name = data[0]
        config[button_name] = {'msg': data[1],
                               'photo_link': data[2] if len(data) >= 3 else None,
                               'photo_path': f'media/other_msg_cfg/{button_name}.jpg'
                               }
    pathlib.Path(f'media/other_msg_cfg').mkdir(exist_ok=True, parents=True)  # пришлось пока вставить это сюда
    return config


async def download_media(photo_data_list: list[PhotoData]) -> None:
    async with aiohttp.ClientSession() as session:
        for photo_data in photo_data_list:
            response = await request_download_media(session, photo_data.link)
            with open(photo_data.path, 'wb') as photo:
                photo.write(response)


async def request_download_media(session: aiohttp.ClientSession, url: str):
    log.debug('Sending request for photo url = %s', url)
    async with session.get(url) as response:
        log.debug(f'Request_status = {response.status} , for {url=}')
        assert response.status == 200
        return await response.read()


def get_media_paths() -> list[PhotoData]:
    media_paths = []
    for config in [PRICE_MSG_CONFIG, COLORS_MSG_CONFIG, FAQ_CFG, OTHER_MSG_CFG]:
        for _, position_data in config.items():
            if not position_data.get('photo_link'):
                continue
            media_paths.append(PhotoData(position_data.get('photo_path'), position_data.get('photo_link')))
    return media_paths


def get_missing_media(photo_data_list) -> list[PhotoData]:
    missing_media = []
    log.debug('Required_media = %s', photo_data_list)
    for photo_data in photo_data_list:
        if not os.path.exists(photo_data.path):
            missing_media.append(photo_data)
    log.debug('Missing media = %s', missing_media)
    return missing_media


@timeit
def check_media() -> None:
    photo_data_list = get_media_paths()
    missing_media = get_missing_media(photo_data_list)
    if not missing_media:
        log.info('All media exist')
        return
    asyncio.run(download_media(missing_media))


log.info('Started importing configuration')  # todo change to func. or not
sh = get_spreadsheet()
GLOBAL_MSG_CONFIG = get_msg_config(sh)
PRICE_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("price_msg_cfg")
BUSINESS_MSG_CONFIG = get_business_config(sh)
COLORS_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("colors_msg_cfg")
FAQ_CFG = GLOBAL_MSG_CONFIG.get('qa_msg_cfg')
DELIVERY_MSG_CFG = get_delivery_msg_cfg(sh)
OTHER_MSG_CFG = get_other_msg_cfg(sh)
check_media()
log.info('Configuration imported successfully')

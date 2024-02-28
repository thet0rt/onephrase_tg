import os
from json import load

import gspread
from gspread import Spreadsheet


def get_spreadsheet() -> Spreadsheet:
    with open('google_creds.json', 'r') as creds_file:
        google_creds = load(creds_file)

    gc = gspread.service_account_from_dict(google_creds)
    sh = gc.open_by_key(os.getenv('SPREADSHEET_CODE'))
    return sh


def get_msg_config(sh: Spreadsheet) -> dict:
    msg_config = {}
    for config_name in ['price_msg_cfg', 'business_msg_cfg', 'qa_msg_cfg']:
        worksheet = sh.worksheet(config_name)
        ws_data = worksheet.batch_get(['A1:C50'])[0]
        config = {}
        for data in ws_data[1:]:
            config[data[0]] = {'button_name': data[1],
                               'msg': data[2]}
        msg_config.update({worksheet.title: config})
    return msg_config


def get_delivery_msg_cfg(sh: Spreadsheet) -> dict:
    config = {}
    worksheet = sh.worksheet('delivery_msg_cfg')
    ws_data = worksheet.batch_get(['A1:E50'])[0]
    headers = ws_data[0]
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


sh = get_spreadsheet()
GLOBAL_MSG_CONFIG = get_msg_config(sh)
PRICE_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("price_msg_cfg")
BUSINESS_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("business_msg_cfg")
FAQ_CFG = GLOBAL_MSG_CONFIG.get('qa_msg_cfg')
DELIVERY_MSG_CFG = get_delivery_msg_cfg(sh)

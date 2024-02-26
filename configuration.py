from typing import Optional
import os
from json import load
import gspread


def get_msg_config() -> dict:
    with open('google_creds.json', 'r') as creds_file:
        google_creds = load(creds_file)

    gc = gspread.service_account_from_dict(google_creds)
    sh = gc.open_by_key(os.getenv('SPREADSHEET_CODE'))
    worksheets = sh.worksheets()
    msg_config = {}
    for worksheet in worksheets:
        load_data_raw = worksheet.batch_get(['A1:C50'])[0]
        config = {}
        for data in load_data_raw[1:]:
            config[data[0]] = {'button_name': data[1],
                               'msg': data[2]}
        msg_config.update({worksheet.title: config})
    return msg_config


GLOBAL_MSG_CONFIG = get_msg_config()
PRICE_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("price_msg_cfg")
BUSINESS_MSG_CONFIG = GLOBAL_MSG_CONFIG.get("business_msg_cfg")
FAQ_CFG = GLOBAL_MSG_CONFIG.get('qa_msg_cfg')


def get_price_msg(
        cloth_type: str,
) -> Optional[dict]:
    return PRICE_MSG_CONFIG.get(cloth_type)

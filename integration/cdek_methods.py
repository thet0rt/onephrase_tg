import requests
import os

CDEK_CLIENT_ID = os.getenv('CDEK_CLIENT_ID')
CDEK_CLIENT_SECRET = os.getenv('CDEK_CLIENT_SECRET')


def get_cdek_token():
    url = 'https://api.cdek.ru/v2/oauth/token?parameters'
    client_id = CDEK_CLIENT_ID
    client_secret = CDEK_CLIENT_SECRET
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]


def get_cdek_uuid(cdek_uuid, cdek_token):
    url = f'https://api.cdek.ru/v2/orders?{cdek_uuid}'
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {cdek_token}', "content-type": "application/json"
    }
    response = requests.get(url=url, headers=headers)
    response = response.json()
    # time.sleep(10)
    log_3.debug(f'get_cdek_uuid response - {response}')
    uuid = response.get('entity').get('uuid')
    log_3.info(f'uuid - {uuid}')
    return uuid


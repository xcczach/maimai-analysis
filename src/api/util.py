from urllib.parse import urljoin
import requests

ROOT_URL = "https://maimai.lxns.net/api/v0/"

def get_player_info(token: str, info_type_url: str):
    target_url = urljoin(urljoin(ROOT_URL, "user/maimai/"), info_type_url)
    header = {"X-User-Token": token}
    response = requests.get(target_url, headers=header)
    return response.json()

def get_public_info(info_type_url: str):
    target_url = urljoin(urljoin(ROOT_URL, "maimai/"), info_type_url)
    print(target_url)
    response = requests.get(target_url)
    return response.json()
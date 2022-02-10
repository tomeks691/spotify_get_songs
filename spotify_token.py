import requests
import json
import os
from dotenv import load_dotenv, find_dotenv


def get_code():
    '''Get code to generate token access'''
    load_dotenv(find_dotenv())
    with open("cookies.json", "r") as f:
        cookies_dict = json.load(f)
    url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={os.environ.get('client_id')}&scope=user-read-currently-playing&redirect_uri=http://example.com/callback"
    result = requests.get(url, cookies=cookies_dict)
    current_url = result.url
    return current_url[current_url.index("=") + 1:]
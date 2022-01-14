import requests
import json
import os
from dotenv import load_dotenv, find_dotenv


def get_code():
    load_dotenv(find_dotenv())
    with open("cookies.json", "r") as f:
        cookies_dict = json.load(f)
    url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={os.environ.get('client_id')}&scope=user-read-currently-playing&redirect_uri=http://example.com/callback"
    result = requests.get(url, cookies=cookies_dict)
    current_url = result.url
    return current_url[current_url.index("=") + 1:]


def get_token():
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'client_id': os.environ.get("client_id"),
        'client_secret': os.environ.get("client_secret"),
        'grant_type': 'authorization_code',
        "code": get_code(),
        "redirect_uri": "http://example.com/callback"
    })
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    return access_token

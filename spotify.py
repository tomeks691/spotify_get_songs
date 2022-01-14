import requests
import sqlite3
import os
from datetime import date
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from spotify_token import get_code


def get_name_artist(songs_from_spotify):
    for keys in songs_from_spotify.keys():
        if keys == "item":
            for key in songs_from_spotify[keys]:
                if key == "artists":
                    for artists in songs_from_spotify[keys][key]:
                        if "name" in artists:
                            return artists["name"]


def get_name_song(songs_from_spotify):
    for keys in songs_from_spotify.keys():
        if keys == "item":
            for key in songs_from_spotify[keys]:
                if "name" in key:
                    return songs_from_spotify[keys][key]


def get_sample_link(songs_from_spotify):
    for keys in songs_from_spotify.keys():
        if keys == "item":
            for key in songs_from_spotify[keys]:
                if "preview_url" in key:
                    return songs_from_spotify[keys][key]


def get_token():
    load_dotenv(find_dotenv())
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
    access_token = auth_response_data['access_token']
    return access_token


conn = sqlite3.connect("songs.db")
cursor = conn.cursor()
token = get_token()
headers = {
    "Authorization": f"Bearer {token}"
}

hour = datetime.now().hour
today = str(date.today())
table_name = "t" + today.replace("-", "_")
cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (name_song text, artist text, link_sample text)""")
cursor.execute(f"SELECT * FROM {table_name}")
last_song = cursor.fetchall()
result = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
if result.status_code not in [204, 200]:
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    quit()

if result.status_code != 204:
    songs = result.json()
    song_name = get_name_song(songs)
    artist = get_name_artist(songs)
    sample = get_sample_link(songs)
    cursor.execute("SELECT name_song FROM T2022_01_14 WHERE name_song = ? AND artist = ?",
                   (song_name, artist))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?)", (song_name, artist, sample))
        conn.commit()
    else:
        print(f"{artist}: {song_name}")
        print("Znaleziono")

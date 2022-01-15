import dropbox
import os
from dropbox.files import WriteMode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
file_to_send = "songs.db"
token_access = os.environ.get("token_access")
dbx = dropbox.Dropbox(token_access)

with open(file_to_send, 'rb') as f:
    dbx.files_upload(f=f.read(), path=f"/spotify/{file_to_send}", mode=WriteMode('overwrite'))
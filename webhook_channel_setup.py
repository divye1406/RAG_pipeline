import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_KEY_PATH")
WEBHOOK_ADDRESS = os.getenv("WEBHOOK_ADDRESS")
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)


start_token = drive.changes().getStartPageToken().execute().get('startPageToken')

import time
import uuid
channel_id = str(uuid.uuid4())
channel_token = "my_secret_channel_token"
channel = drive.changes().watch(
    pageToken=start_token,
    body={
        'id': channel_id,
        'type': 'web_hook',
        'address': WEBHOOK_ADDRESS,
        'token': channel_token,
        'expiration':  int(time.time()+604800)*1000  # one week from now
    }
).execute()
resource_id = channel['resourceId']
print(resource_id)
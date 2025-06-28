from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import os

# Zie YouTube API v3 Python docs voor volledige set-up
CLIENT_SECRETS_FILE = "client_secret.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

storage = Storage("oauth2.json")
credentials = storage.get()
if credentials is None or credentials.invalid:
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    credentials = run_flow(flow, storage)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

body=dict(
    snippet=dict(
        title="Clickbait titel hier",  # Genereer via GPT!
        description="Automatisch gegenereerde beschrijving.",
        tags=["AI", "trending", "hack"],
        categoryId="28"
    ),
    status=dict(
        privacyStatus="public"
    )
)

media = MediaFileUpload('data/videos/output.mp4', resumable=True)
request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
response = request.execute()
print("Video geüpload!")

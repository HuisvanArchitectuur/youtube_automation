from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os

print("[DEBUG] Start script")

# OAuth scope die je nodig hebt voor uploaden naar YouTube
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Pak secrets uit environment variables (deze zet je in GitHub Secrets)
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN')

if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
    raise Exception("Je mist een of meerdere benodigde secrets: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN")

print("[DEBUG] Credentials ophalen vanuit environment variables")
credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    token_uri="https://oauth2.googleapis.com/token"
)

print("[DEBUG] Bouw YouTube client")
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

print("[DEBUG] Bouw request body op")
body = dict(
    snippet=dict(
        title="Clickbait titel (automatisch invullen!)",
        description="Automatisch gegenereerde beschrijving.",
        tags=["AI", "trending", "hack"],
        categoryId="28"
    ),
    status=dict(
        privacyStatus="public"
    )
)

# Let op: check of je pad naar je video correct is
VIDEO_PATH = 'data/videos/output.mp4'

print("[DEBUG] Zet MediaFileUpload klaar")
media = MediaFileUpload(VIDEO_PATH, resumable=True)

print("[DEBUG] Maak YouTube insert request aan")
request = youtube.videos().insert(
    part="snippet,status",
    body=body,
    media_body=media
)

print("[DEBUG] Voer upload uit (request.execute())")
response = request.execute()

print("[DEBUG] Video geüpload!")
print(response)

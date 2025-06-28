from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import OAuth2Credentials
import os

print("[DEBUG] Start script")

# OAuth scope en API info
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Haal client ID, client secret en refresh token uit environment variables (van GitHub Secrets)
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    raise Exception("Missende environment variables voor YouTube API: check YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET en YOUTUBE_REFRESH_TOKEN")

print("[DEBUG] Maak OAuth2 credentials aan vanuit refresh token")
credentials = OAuth2Credentials(
    access_token=None,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    refresh_token=REFRESH_TOKEN,
    token_expiry=None,
    token_uri="https://oauth2.googleapis.com/token",
    user_agent=None,
    scopes=[YOUTUBE_UPLOAD_SCOPE]
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

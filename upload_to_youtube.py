from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import os

print("[DEBUG] Start script")

CLIENT_SECRETS_FILE = "client_secret.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

print("[DEBUG] Controleer oauth2.json (credentials ophalen)")
storage = Storage("oauth2.json")
credentials = storage.get()

if credentials is None or credentials.invalid:
    print("[DEBUG] Geen geldige credentials gevonden, start authenticatie-flow")
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    credentials = run_flow(flow, storage)
else:
    print("[DEBUG] Credentials OK, ga verder")

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

print("[DEBUG] Zet MediaFileUpload klaar")
media = MediaFileUpload('data/videos/output.mp4', resumable=True)

print("[DEBUG] Maak YouTube insert request aan")
request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

print("[DEBUG] Voer upload uit (request.execute())")
response = request.execute()

print("[DEBUG] Video geüpload!")

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import os
import json

print("[DEBUG] Start script")

# Veronderstel dat secrets als env vars worden gezet in GitHub Actions
CLIENT_SECRET_JSON_ENV = "YOUTUBE_CLIENT_SECRET_JSON"
OAUTH2_JSON_ENV = "YOUTUBE_REFRESH_TOKEN_JSON"

CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "oauth2.json"

# Schrijf de client_secret.json naar disk als die niet bestaat (vanuit env var)
if not os.path.isfile(CLIENT_SECRETS_FILE):
    print(f"[DEBUG] Schrijf {CLIENT_SECRETS_FILE} vanuit environment variable")
    secret_json = os.getenv(CLIENT_SECRET_JSON_ENV)
    if secret_json:
        with open(CLIENT_SECRETS_FILE, "w") as f:
            f.write(secret_json)
    else:
        print(f"[ERROR] Environment variable {CLIENT_SECRET_JSON_ENV} niet gevonden!")

# Schrijf de oauth2.json naar disk als die niet bestaat (vanuit env var)
if not os.path.isfile(TOKEN_FILE):
    print(f"[DEBUG] Schrijf {TOKEN_FILE} vanuit environment variable")
    token_json = os.getenv(OAUTH2_JSON_ENV)
    if token_json:
        with open(TOKEN_FILE, "w") as f:
            f.write(token_json)
    else:
        print(f"[ERROR] Environment variable {OAUTH2_JSON_ENV} niet gevonden!")

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

print("[DEBUG] Controleer of token file bestaat (credentials ophalen)")
storage = Storage(TOKEN_FILE)
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

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import os
import json
import signal
import sys
import traceback

print("[DEBUG] Start script")

CLIENT_SECRET_JSON_ENV = "YOUTUBE_CLIENT_SECRET_JSON"
OAUTH2_JSON_ENV = "YOUTUBE_REFRESH_TOKEN_JSON"

CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "oauth2.json"

def debug_list_folder(path):
    try:
        print(f"[DEBUG] Inhoud van {path}: {os.listdir(path)}")
    except Exception as e:
        print(f"[DEBUG] Kan inhoud van {path} niet tonen: {e}")

print("[DEBUG] Huidige working dir:", os.getcwd())
debug_list_folder(".")
debug_list_folder("data")
debug_list_folder("data/videos")

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

if not os.path.exists(VIDEO_PATH):
    print(f"[ERROR] Video-bestand bestaat niet: {VIDEO_PATH}")
    sys.exit(1)
else:
    print(f"[DEBUG] Video-bestand gevonden: {VIDEO_PATH}, grootte: {os.path.getsize(VIDEO_PATH)} bytes")

print("[DEBUG] Zet MediaFileUpload klaar")
media = MediaFileUpload(VIDEO_PATH, resumable=True, chunksize=5*1024*1024)  # 5 MB chunks

print("[DEBUG] Maak YouTube insert request aan")
request = youtube.videos().insert(
    part="snippet,status",
    body=body,
    media_body=media
)

class TimeoutException(Exception): pass
def handler(signum, frame):
    raise TimeoutException("Upload duurde te lang!")

signal.signal(signal.SIGALRM, handler)
UPLOAD_TIMEOUT_SECONDS = 900  # 15 minuten
signal.alarm(UPLOAD_TIMEOUT_SECONDS)

try:
    print(f"[DEBUG] Start upload met voortgang (timeout op {UPLOAD_TIMEOUT_SECONDS // 60} minuten)")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[DEBUG] Upload voortgang: {int(status.progress() * 100)}%")
    print("[DEBUG] Video geüpload!")
    print(response)
except TimeoutException:
    print("[ERROR] Upload duurde te lang, mogelijk netwerk/API probleem!")
except HttpError as e:
    print(f"[ERROR] Fout van de YouTube API: {e}")
    print(e.content)
except Exception as e:
    print(f"[ERROR] Onverwachte fout bij upload: {e}")
    print(traceback.format_exc())
    sys.exit(1)
finally:
    signal.alarm(0)  # Zet alarm uit

print("[DEBUG] Einde uploadscript")

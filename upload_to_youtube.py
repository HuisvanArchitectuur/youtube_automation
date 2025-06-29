print("==== START VAN SCRIPT ====")

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

# === Toevoeging voor automatische titel/omschrijving ===
from transformers import pipeline
import glob
import re

print("[DEBUG] Stap 1: Start script")

CLIENT_SECRET_JSON_ENV = "YOUTUBE_CLIENT_SECRET_JSON"
OAUTH2_JSON_ENV = "YOUTUBE_REFRESH_TOKEN_JSON"

CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "oauth2.json"

def debug_list_folder(path):
    try:
        print(f"[DEBUG] Inhoud van {path}: {os.listdir(path)}")
    except Exception as e:
        print(f"[DEBUG] Kan inhoud van {path} niet tonen: {e}")

print("[DEBUG] Stap 2: Huidige working dir:", os.getcwd())
debug_list_folder(".")
debug_list_folder("data")
debug_list_folder("data/videos")

print("[DEBUG] Stap 3: Check/maak client_secret.json")
if not os.path.isfile(CLIENT_SECRETS_FILE):
    secret_json = os.getenv(CLIENT_SECRET_JSON_ENV)
    if secret_json:
        with open(CLIENT_SECRETS_FILE, "w") as f:
            f.write(secret_json)
        print("[DEBUG] client_secret.json aangemaakt")
    else:
        print(f"[ERROR] Environment variable {CLIENT_SECRET_JSON_ENV} niet gevonden!")

print("[DEBUG] Stap 4: Check/maak oauth2.json")
if not os.path.isfile(TOKEN_FILE):
    token_json = os.getenv(OAUTH2_JSON_ENV)
    if token_json:
        with open(TOKEN_FILE, "w") as f:
            f.write(token_json)
        print("[DEBUG] oauth2.json aangemaakt")
    else:
        print(f"[ERROR] Environment variable {OAUTH2_JSON_ENV} niet gevonden!")

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

print("[DEBUG] Stap 5: Credentials ophalen")
storage = Storage(TOKEN_FILE)
credentials = storage.get()

if credentials is None or credentials.invalid:
    print("[DEBUG] Geen geldige credentials gevonden, start authenticatie-flow")
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    credentials = run_flow(flow, storage)
else:
    print("[DEBUG] Credentials OK, ga verder")

print("[DEBUG] Stap 6: Bouw YouTube client")
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

# =======================
# Toevoeging: Maak automatisch clickbait titel & description
# =======================
try:
    script_files = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
    if not script_files:
        raise Exception("Geen scriptbestand gevonden in data/scripts/")
    with open(script_files[0], 'r') as f:
        script_text = f.read().strip()
    generator = pipeline('text-generation', model='google/flan-t5-small')

    prompt = (
        "Genereer een virale YouTube titel die nieuwsgierig maakt en aanzet tot klikken. "
        "Gebruik psychologisch bewezen technieken zoals een vraag, cijfers, geheimen, urgentie, of verrassing. "
        "Titel moet maximaal 100 tekens zijn. Hier is het script:\n"
        f"{script_text}\n"
        "Geef alleen de titel terug."
    )
    title_result = generator(prompt, max_length=100)[0]['generated_text'].strip().split('\n')[0]
    # CLEANUP
    title_result = re.sub(r'[^\x20-\x7E]', '', title_result)
    title_result = title_result.strip()[:100]
    if ("genereer" in title_result.lower() or "titel" in title_result.lower() or len(title_result) < 8):
        title_result = "Deze AI-video wil je niet missen! 😱 (Trending 2025)"

    # Eerste 3 zinnen als description
    script_sents = re.split(r'(?<=[.!?]) +', script_text)
    description = ' '.join(script_sents[:3])

    # Tags dynamisch
    tags = ["AI", "trending", "hack"]
    if script_sents:
        tags.append(script_sents[0][:20])

    print(f"[DEBUG] Final YouTube titel: {title_result}")
    print(f"[DEBUG] Final YouTube description: {description}")
    print(f"[DEBUG] Final YouTube tags: {tags}")

except Exception as e:
    print(f"[WARNING] Titel/omschrijving automatisch genereren mislukt, gebruik fallback. ({e})")
    title_result = "Clickbait titel (automatisch invullen!)"
    description = "Automatisch gegenereerde beschrijving."
    tags = ["AI", "trending", "hack"]

print("[DEBUG] Stap 7: Bouw request body op")
body = dict(
    snippet=dict(
        title=title_result,
        description=description,
        tags=tags,
        categoryId="28"
    ),
    status=dict(
        privacyStatus="public"
    )
)

VIDEO_PATH = 'data/videos/output.mp4'

print("[DEBUG] Stap 8: Controleer of video-bestand bestaat")
if not os.path.exists(VIDEO_PATH):
    print(f"[ERROR] Video-bestand bestaat niet: {VIDEO_PATH}")
    sys.exit(1)
else:
    size_bytes = os.path.getsize(VIDEO_PATH)
    print(f"[DEBUG] Video-bestand gevonden: {VIDEO_PATH}, grootte: {size_bytes} bytes")
    size_mb = size_bytes / (1024 * 1024)
    print(f"[DEBUG] Bestandsgrootte in MB: {size_mb:.2f} MB")

print("[DEBUG] Stap 9: Zet MediaFileUpload klaar")
media = MediaFileUpload(VIDEO_PATH, resumable=True, chunksize=5*1024*1024)  # 5 MB chunks

print("[DEBUG] Stap 10: Maak YouTube insert request aan")
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
    print(f"[DEBUG] Stap 11: Start upload met voortgang (timeout op {UPLOAD_TIMEOUT_SECONDS // 60} minuten)")
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

print("[DEBUG] Stap 12: Einde uploadscript")

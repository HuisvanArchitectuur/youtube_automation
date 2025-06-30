# generate_visuals.py

import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image

# 📦 Secrets laden
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not PEXELS_API_KEY:
    raise Exception("❌ PEXELS_API_KEY not found in environment variables.")

# 📂 Paden
VOICEOVER_TEXTS_PATH = "data/voiceovers/voiceover_texts.json"
VISUAL_DIR = "data/videos"
VISUAL_LIST_PATH = f"{VISUAL_DIR}/visual_list.json"

# 📄 Laad de voiceover-teksten
if not os.path.exists(VOICEOVER_TEXTS_PATH):
    raise FileNotFoundError(f"{VOICEOVER_TEXTS_PATH} not found! Run generate_voiceover_texts.py first.")

with open(VOICEOVER_TEXTS_PATH, "r", encoding="utf-8") as f:
    voiceover_texts = json.load(f)

# 📁 Zorg dat visual folder bestaat
os.makedirs(VISUAL_DIR, exist_ok=True)

headers = {"Authorization": PEXELS_API_KEY}
visual_paths = []

# 🔁 Per scene 1 beeld genereren
for idx, text in enumerate(voiceover_texts):
    query = f"technology, future, innovation, {text[:40]}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get('photos'):
            image_url = data['photos'][0]['src']['large']
            img_data = requests.get(image_url).content
            visual_path = f"{VISUAL_DIR}/visual_{idx+1}.jpg"
            with open(visual_path, 'wb') as handler:
                handler.write(img_data)

            # 📏 Fix dimensions (even numbers required by FFmpeg)
            img = Image.open(visual_path)
            w, h = img.size
            w_even = w - (w % 2)
            h_even = h - (h % 2)
            if (w_even != w) or (h_even != h):
                img = img.resize((w_even, h_even))
                img.save(visual_path)

            print(f"[✅] Visual saved: {visual_path}")
            visual_paths.append(visual_path)
        else:
            raise Exception("No results from Pexels API.")

    except Exception as e:
        print(f"[⚠️] Failed to fetch image for scene {idx+1}: {e}")
        fallback = f"{VISUAL_DIR}/fallback_{idx+1}.jpg"
        Image.new("RGB", (1280, 720), color="black").save(fallback)
        visual_paths.append(fallback)
        print(f"[🖼️] Fallback image created: {fallback}")

# 💾 Save paths
if not visual_paths:
    raise Exception("❌ No visuals could be generated.")
with open(VISUAL_LIST_PATH, "w", encoding="utf-8") as f:
    json.dump(visual_paths, f)

print(f"📂 Visual list saved to {VISUAL_LIST_PATH}")

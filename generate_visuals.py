import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

voiceover_texts_path = 'data/voiceovers/voiceover_texts.json'
if not os.path.exists(voiceover_texts_path):
    raise Exception(f"❌ Bestand {voiceover_texts_path} niet gevonden! Run generate_voiceover_texts.py eerst.")

with open(voiceover_texts_path, 'r') as f:
    voiceover_texts = json.load(f)

headers = {"Authorization": PEXELS_API_KEY}
visual_paths = []

MAX_VISUALS = len(voiceover_texts)  # dynamisch gebaseerd op scenes
visual_dir = "data/videos"
os.makedirs(visual_dir, exist_ok=True)

for idx, text in enumerate(voiceover_texts[:MAX_VISUALS]):
    query = f"AI technology, innovation, {text[:45]}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get('photos'):
            image_url = data['photos'][0]['src']['large']
            img_data = requests.get(image_url).content
            visual_path = f"{visual_dir}/visual_{idx+1}.jpg"
            with open(visual_path, 'wb') as handler:
                handler.write(img_data)
            img = Image.open(visual_path)
            w, h = img.size
            even_w = w - (w % 2)
            even_h = h - (h % 2)
            if (even_w != w) or (even_h != h):
                img = img.resize((even_w, even_h))
                img.save(visual_path)
            print(f"[INFO] Visual saved: {visual_path}")
            visual_paths.append(visual_path)
        else:
            raise Exception("No image found")
    except Exception as e:
        print(f"[WARNING] Failed to get image for scene {idx+1}: {e}")
        # Fallback image logic
        fallback_path = f"{visual_dir}/fallback_{idx+1}.jpg"
        Image.new('RGB', (1280, 720), color='black').save(fallback_path)
        visual_paths.append(fallback_path)
        print(f"[INFO] Fallback image saved: {fallback_path}")

# Save list
if not visual_paths:
    raise Exception("❌ No visuals were generated or added!")

with open(f"{visual_dir}/visual_list.json", 'w') as f:
    json.dump(visual_paths, f)

print(f"✅ All visuals saved to {visual_dir}/visual_list.json")

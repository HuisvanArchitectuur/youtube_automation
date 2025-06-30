import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

voiceover_texts_path = 'data/voiceovers/voiceover_texts.json'
if not os.path.exists(voiceover_texts_path):
    raise Exception(f"❌ File not found: {voiceover_texts_path}. Run generate_voiceover_texts.py first.")

with open(voiceover_texts_path, 'r') as f:
    voiceover_texts = json.load(f)

headers = {"Authorization": PEXELS_API_KEY}
visual_paths = []

visual_dir = "data/videos"
os.makedirs(visual_dir, exist_ok=True)

MAX_VISUALS = len(voiceover_texts)

for idx, text in enumerate(voiceover_texts[:MAX_VISUALS]):
    query = f"technology, innovation, {text[:45]}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('photos'):
            image_url = data['photos'][0]['src']['large']
            img_data = requests.get(image_url).content
            visual_path = f"{visual_dir}/visual_{idx+1}.jpg"
            with open(visual_path, 'wb') as handler:
                handler.write(img_data)

            img = Image.open(visual_path)
            w, h = img.size
            img = img.resize((w - w % 2, h - h % 2))
            img.save(visual_path)

            print(f"✅ Visual {idx+1} saved: {visual_path}")
            visual_paths.append(visual_path)
        else:
            raise Exception("No image found")
    except Exception as e:
        print(f"⚠️ Scene {idx+1} image error: {e}")
        fallback_path = f"{visual_dir}/fallback_{idx+1}.jpg"
        Image.new('RGB', (1280, 720), color='black').save(fallback_path)
        print(f"🖼️ Using fallback image: {fallback_path}")
        visual_paths.append(fallback_path)

if not visual_paths:
    raise Exception("❌ No visuals found or generated.")

with open(f"{visual_dir}/visual_list.json", 'w') as f:
    json.dump(visual_paths, f)

print(f"📂 Visual list saved to {visual_dir}/visual_list.json")

import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Laad per-scene voice-over teksten (korte, heldere prompts)
voiceover_texts_path = 'data/voiceovers/voiceover_texts.json'
if not os.path.exists(voiceover_texts_path):
    raise Exception(f"Bestand {voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

with open(voiceover_texts_path, 'r') as f:
    voiceover_texts = json.load(f)

headers = {"Authorization": PEXELS_API_KEY}
visual_paths = []

MAX_VISUALS = 5  # Past aan voor het aantal scenes (of: len(voiceover_texts))

for idx, text in enumerate(voiceover_texts[:MAX_VISUALS]):
    # Maak zoekprompt: focus op kern van voice-over, met context
    query = f"AI technologie, innovatie, {text[:45]}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('photos'):
        image_url = data['photos'][0]['src']['large']
        img_data = requests.get(image_url).content
        visual_path = f"data/videos/visual_{idx+1}.jpg"
        with open(visual_path, 'wb') as handler:
            handler.write(img_data)
        # Zorg dat breedte/hoogte even zijn (ffmpeg vereist dit)
        img = Image.open(visual_path)
        w, h = img.size
        even_w = w - (w % 2)
        even_h = h - (h % 2)
        if (even_w != w) or (even_h != h):
            img = img.resize((even_w, even_h))
            img.save(visual_path)
        print(f"Visual opgeslagen als {visual_path}")
        visual_paths.append(visual_path)
    else:
        print(f"Geen afbeelding gevonden voor scene: {text}")
        # Voeg standaardbeeld toe
        default_img = "data/videos/default_visual.jpg"
        if os.path.exists(default_img):
            visual_paths.append(default_img)
        else:
            # Maak een zwart beeld als default niet bestaat
            if not os.path.exists("data/videos"):
                os.makedirs("data/videos")
            Image.new('RGB', (940, 528), color='black').save(default_img)
            visual_paths.append(default_img)

# Sla de lijst van visuals op voor gebruik in assemble_video.py
with open('data/videos/visual_list.json', 'w') as f:
    json.dump(visual_paths, f)

print("Alle visuals gegenereerd en paden opgeslagen in data/videos/visual_list.json")

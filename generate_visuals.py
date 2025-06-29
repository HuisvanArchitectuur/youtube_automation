import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Haal script op en splits in scenes (regels)
with open('data/scripts', 'r') as scriptfile:
    # Gebruik altijd het nieuwste scriptbestand
    script_files = sorted([f for f in os.listdir('data/scripts') if f.endswith('.txt')])
    if not script_files:
        raise Exception("Geen scriptbestand gevonden in data/scripts/")
    with open(f"data/scripts/{script_files[-1]}", "r") as f:
        script_text = f.read()

scenes = [s.strip() for s in script_text.split('.') if s.strip()]  # Split op punt

headers = {
    "Authorization": PEXELS_API_KEY
}

visual_paths = []
for idx, scene in enumerate(scenes):
    query = scene[:60]  # Max 60 chars query
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('photos'):
        image_url = data['photos'][0]['src']['large']
        img_data = requests.get(image_url).content
        visual_path = f"data/videos/visual_{idx+1}.jpg"
        with open(visual_path, 'wb') as handler:
            handler.write(img_data)
        # Optional: zorg dat de afbeelding een even breedte/hoogte heeft
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
        print(f"Geen afbeelding gevonden voor scene: {scene}")

# Sla lijst van visuals op voor gebruik in assemble_video.py
with open('data/videos/visual_list.json', 'w') as f:
    json.dump(visual_paths, f)

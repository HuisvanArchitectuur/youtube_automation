import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image
import glob

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Haal de titel van de video uit het scriptbestand of een apart bestand
script_files = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
if not script_files:
    raise Exception("Geen scriptbestand gevonden in data/scripts/")
script_path = script_files[0]
with open(script_path, 'r') as scriptfile:
    script_text = scriptfile.read()

# Probeer de titel te halen (eerste regel, of met regex)
video_title = script_text.split('\n')[0]
if len(video_title) < 5:
    video_title = "AI technologie"  # fallback

# Splits script op scenes/zinnen, filter lege zinnen eruit
scenes = [s.strip() for s in script_text.split('.') if s.strip()]

headers = {"Authorization": PEXELS_API_KEY}
visual_paths = []
MAX_VISUALS = 5  # **Pas dit aan als je meer/minder visuals wilt**

for idx, scene in enumerate(scenes[:MAX_VISUALS]):
    # **Prompt optimalisatie**: Voeg AI/tech-context toe
    query = f"AI technologie, digitale innovatie, {video_title}, {scene[:30]}"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('photos'):
        image_url = data['photos'][0]['src']['large']
        img_data = requests.get(image_url).content
        visual_path = f"data/videos/visual_{idx+1}.jpg"
        with open(visual_path, 'wb') as handler:
            handler.write(img_data)
        # Maak breedte/hoogte even (anders ffmpeg error)
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
        # Voeg een default afbeelding toe
        default_img = "data/videos/default_visual.jpg"
        if os.path.exists(default_img):
            visual_paths.append(default_img)
        else:
            # Maak 1x een dummy (zwart) beeld als deze niet bestaat
            if not os.path.exists("data/videos"):
                os.makedirs("data/videos")
            Image.new('RGB', (940, 528), color='black').save(default_img)
            visual_paths.append(default_img)

# Sla lijst van visuals op voor gebruik in assemble_video.py
with open('data/videos/visual_list.json', 'w') as f:
    json.dump(visual_paths, f)

print("Alle visuals gegenereerd en paden opgeslagen in data/videos/visual_list.json")

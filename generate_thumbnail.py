import os
import json
from PIL import Image

# Laad de lijst met visuals
visual_list_path = 'data/videos/visual_list.json'
if not os.path.exists(visual_list_path):
    raise Exception(f"{visual_list_path} bestaat niet! Draai eerst generate_visuals.py")

with open(visual_list_path, 'r') as f:
    visuals = json.load(f)

if not visuals:
    raise Exception("Geen visuals gevonden in visual_list.json!")

visual_path = visuals[0]  # Pak de eerste afbeelding als thumbnail

# Open en sla op als PNG voor YouTube thumbnail
image = Image.open(visual_path).convert("RGB")
thumbnail_path = "data/thumbnails/thumb.png"
os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
image.save(thumbnail_path)
print(f"Thumbnail opgeslagen als {thumbnail_path}")

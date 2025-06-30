# generate_thumbnail.py

import openai
import os
import json
from PIL import Image
from dotenv import load_dotenv

# 🔑 Laad API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📂 Paden
VISUAL_LIST_PATH = "data/videos/visual_list.json"
TOPIC_PATH = "data/topic.json"
THUMB_PATH = "data/thumbnails/thumb.png"
TITLE_PATH = "data/thumbnails/title.txt"

# 🖼️ Laad eerste visueel als thumbnail
with open(VISUAL_LIST_PATH, 'r') as f:
    visuals = json.load(f)
if not visuals:
    raise Exception("❌ Geen visuals beschikbaar!")
thumb_source = visuals[0]
image = Image.open(thumb_source).convert("RGB")
os.makedirs(os.path.dirname(THUMB_PATH), exist_ok=True)
image.save(THUMB_PATH)
print(f"✅ Thumbnail image opgeslagen: {THUMB_PATH}")

# 🎯 Laad onderwerp
with open(TOPIC_PATH, "r", encoding="utf-8") as f:
    topic = json.load(f)["topic"]

# 🧠 Genereer clickbait-titel met GPT-4
prompt = f"""
Create a viral YouTube Shorts title (max 60 characters) for the topic: "{topic}"

Make it curiosity-driven, emotional or surprising. Do NOT include hashtags, emojis, or numbers. Output ONLY the title.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=50
)

title = response['choices'][0]['message']['content'].strip().strip('"')
with open(TITLE_PATH, 'w', encoding='utf-8') as f:
    f.write(title)

print(f"📝 Title opgeslagen: {title}")

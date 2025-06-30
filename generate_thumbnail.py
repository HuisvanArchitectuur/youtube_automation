# generate_thumbnail.py
import openai
import os
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
VISUAL_LIST_PATH = 'data/videos/visual_list.json'
TOPIC_PATH = 'data/topic.json'
THUMB_PATH = 'data/thumbnails/thumb.png'
TITLE_PATH = 'data/thumbnails/title.txt'

# Load first image
with open(VISUAL_LIST_PATH, 'r') as f:
    visuals = json.load(f)
visual_path = visuals[0]

image = Image.open(visual_path).convert("RGB")
os.makedirs(os.path.dirname(THUMB_PATH), exist_ok=True)
image.save(THUMB_PATH)
print(f"✅ Thumbnail saved to: {THUMB_PATH}")

# Generate title
with open(TOPIC_PATH) as f:
    topic = json.load(f)["topic"]

prompt = f"""
Write a viral YouTube Shorts title (max 60 characters) based on the topic: "{topic}"

Make it engaging, curiosity-driven, and avoid hashtags or numbers.
Only return the title, no explanation or formatting.
"""

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=60
)

title = response.choices[0].message.content.strip().strip('"')
with open(TITLE_PATH, 'w', encoding='utf-8') as f:
    f.write(title)

print(f"📝 Title saved: {title}")

import os
import json
from PIL import Image
from transformers import pipeline

# Paths
visual_list_path = 'data/videos/visual_list.json'
topic_path = 'data/topic.json'
thumbnail_path = "data/thumbnails/thumb.png"
title_path = "data/thumbnails/title.txt"

# Load visual list
if not os.path.exists(visual_list_path):
    raise Exception("❌ visual_list.json not found. Run generate_visuals.py first.")

with open(visual_list_path, 'r') as f:
    visuals = json.load(f)

if not visuals:
    raise Exception("❌ No visuals found in visual_list.json!")

visual_path = visuals[0]  # Use the first visual

# Create and save thumbnail
image = Image.open(visual_path).convert("RGB")
os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
image.save(thumbnail_path)
print(f"🖼️ Thumbnail saved to: {thumbnail_path}")

# Load topic for title generation
with open(topic_path, 'r') as f:
    topic_data = json.load(f)
topic = topic_data["topic"]

# Generate YouTube-style catchy title
generator = pipeline("text2text-generation", model="google/flan-t5-small")

title_prompt = f"""
Create a catchy, curiosity-driven YouTube Short video title (max 60 characters) based on the topic: "{topic}".

Avoid hashtags or numbers. Use an engaging, mysterious or exciting tone.
Only return the title, no quotes or explanations.
"""

result = generator(title_prompt, max_length=60)
title = result[0]['generated_text'].strip().replace('"', '')

# Save title
with open(title_path, 'w', encoding='utf-8') as f:
    f.write(title)

print(f"📝 Title generated and saved: {title}")

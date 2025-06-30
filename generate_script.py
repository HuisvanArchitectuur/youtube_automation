from transformers import pipeline
import json
import os
from datetime import datetime

# Load generators
generator = pipeline("text2text-generation", model="google/flan-t5-small")
fact_checker = pipeline("text2text-generation", model="google/flan-t5-small")

# File paths
TOPIC_FILE = "data/topic.json"
SCRIPT_FILE = "data/scripts/script.txt"
FACTCHECK_FILE = "data/scripts/factcheck.txt"

# Load topic
with open(TOPIC_FILE) as f:
    topic_data = json.load(f)
topic = topic_data["topic"]
print(f"🎯 Selected topic: {topic}")

# Prompt for script generation
prompt = f"""
You are a creative and factual YouTube scriptwriter.

Write a short-form video script (for a 60-second YouTube Short) in **10 scenes** about: "{topic}".

✅ Each scene must be **1 standalone, compelling sentence**, ready to be used as voice-over.
✅ Start with a strong hook (Scene 1), build curiosity, and end with a bold claim or cliffhanger (Scene 10).
✅ Include surprising facts, scientific tidbits, or shocking insights — but keep it accessible and truthful.
❌ Do not mention visuals, pictures, or say "as you can see".
❌ Do not use numbering or headings — just list 10 clean lines of text.
"""

response = generator(prompt, max_length=180)
script_raw = response[0]['generated_text']
scenes = [s.strip() for s in script_raw.strip().split('\n') if s.strip()]
print("🧠 Script generated:", scenes)

# Save script
os.makedirs(os.path.dirname(SCRIPT_FILE), exist_ok=True)
with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
    for scene in scenes:
        f.write(scene + "\n")

print(f"✅ Script saved to: {SCRIPT_FILE}")

# Factcheck (optional)
factcheck_prompt = f"""
Here is a 10-scene YouTube short script:\n\n{script_raw}\n\n
Please do the following:
1. Are the claims factually accurate? (yes/no)
2. Highlight any errors or exaggerations.
3. Provide a corrected/improved version of the script if needed.
"""

factcheck_response = fact_checker(factcheck_prompt, max_length=180)
factcheck_text = factcheck_response[0]['generated_text']

# Save factcheck
with open(FACTCHECK_FILE, 'w', encoding='utf-8') as f:
    f.write(factcheck_text)

print(f"🧪 Factcheck saved to: {FACTCHECK_FILE}")

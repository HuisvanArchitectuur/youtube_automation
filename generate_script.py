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
with open(TOPIC_FILE, "r") as f:
    topic_data = json.load(f)
topic = topic_data["topic"]
print(f"🎯 Selected topic: {topic}")

# Prompt for script generation
prompt = f"""
You are a creative and factual scriptwriter for YouTube Shorts.

Write 10 short, standalone sentences for a video on: "{topic}"

Each line should be exactly one sentence — engaging, surprising, and ideal for voice-over narration.

Use a strong hook at the beginning and end with a twist, cliffhanger, or call to action.

Do not repeat the same word more than once per sentence.

Avoid numbering or any formatting — just output 10 clean lines of text.

Example:
- There's a planet made entirely of diamonds.
- On Venus, it actually rains metal.
- One human brain can store more data than all iPhones combined.
"""

# Generate script
response = generator(prompt, max_length=180)
script_raw = response[0]['generated_text']
lines = [line.strip() for line in script_raw.strip().split('\n') if line.strip()]
scenes = []

# Extra: filter out repetition-only lines like "science fiction"
for line in lines:
    if len(set(line.lower().split())) > 3:  # at least 4 unique words
        scenes.append(line)
    if len(scenes) == 10:
        break

if len(scenes) < 10:
    raise Exception("❌ Script generation failed or was too short. Check the model output.")

# Save script
os.makedirs(os.path.dirname(SCRIPT_FILE), exist_ok=True)
with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
    for scene in scenes:
        f.write(scene + "\n")

print(f"✅ Script saved to: {SCRIPT_FILE}")

# Optional: Factcheck
factcheck_prompt = f"""
Here is a 10-sentence script for a YouTube Short:\n\n{script_raw}\n\n
Please do the following:
1. Are the facts accurate and plausible?
2. Correct any exaggerated or false claims.
3. Return an improved version with 10 clear, factual sentences.
"""

factcheck_response = fact_checker(factcheck_prompt, max_length=180)
factcheck_text = factcheck_response[0]['generated_text']

with open(FACTCHECK_FILE, 'w', encoding='utf-8') as f:
    f.write(factcheck_text)

print(f"🧪 Factcheck saved to: {FACTCHECK_FILE}")

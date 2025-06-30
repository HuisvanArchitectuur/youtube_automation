# generate_script.py
import openai
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_FILE = "data/topic.json"
SCRIPT_FILE = "data/scripts/script.txt"
FACTCHECK_FILE = "data/scripts/factcheck.txt"

with open(TOPIC_FILE, "r") as f:
    topic = json.load(f)["topic"]

print(f"🎯 Generating script for topic: {topic}")

prompt = f"""
You are a creative and factual YouTube Shorts scriptwriter.

Write a 10-sentence script about: "{topic}".

Each sentence should be 1 scene — engaging, voice-over-ready, based on real facts or plausible science. 
Start with a hook, build curiosity, and end with a bold or emotional twist.

Do not use numbering, no scene labels. Just output 10 unique, punchy sentences — one per line.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.85,
    max_tokens=400
)

script_text = response['choices'][0]['message']['content']
scenes = [line.strip() for line in script_text.split("\n") if line.strip()]
if len(scenes) < 5:
    raise Exception("Script too short or invalid.")

os.makedirs(os.path.dirname(SCRIPT_FILE), exist_ok=True)
with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
    for scene in scenes:
        f.write(scene + "\n")

print(f"✅ Script saved to: {SCRIPT_FILE}")

# Optional: factcheck
factcheck_prompt = f"""
Fact-check the following 10-sentence YouTube Short script. Correct any misinformation.

SCRIPT:
{script_text}
"""

factcheck = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": factcheck_prompt}],
    temperature=0.2,
    max_tokens=400
)
with open(FACTCHECK_FILE, "w", encoding="utf-8") as f:
    f.write(factcheck['choices'][0]['message']['content'])

print(f"🧪 Factcheck saved to: {FACTCHECK_FILE}")

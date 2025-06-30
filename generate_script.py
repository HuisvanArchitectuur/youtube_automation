# generate_script.py
import os
import json
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

TOPIC_FILE = "data/topic.json"
SCRIPT_FILE = "data/scripts/script.txt"
FACTCHECK_FILE = "data/scripts/factcheck.txt"

# Topic laden
with open(TOPIC_FILE, "r") as f:
    topic = json.load(f)["topic"]

print(f"🎯 Genereer script voor topic: {topic}")

# Init model
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Prompt met ALLE eisen
prompt = (
    f"You are a viral YouTube Shorts scriptwriter.\n\n"
    f"Write a script of 10 **independent sentences** about the topic: \"{topic}\".\n\n"
    "Each sentence will become a separate scene with a voice-over.\n"
    "✅ Start with a strong hook.\n"
    "✅ End with a cliffhanger or emotional twist.\n"
    "✅ Each sentence must be based on **real facts**, science, or plausible information.\n"
    "✅ Each line must be punchy, interesting, and storytelling-style.\n"
    "❌ Do not use numbers or labels.\n"
    "❌ Do not mention images or visuals.\n"
    "Write exactly 10 separate lines, ready for English voice-over."
)

# Genereer
result = generator(prompt, max_length=350)[0]['generated_text']
scenes = [line.strip() for line in result.strip().split('\n') if line.strip()]

if len(scenes) < 8:
    raise Exception("⚠️ Te weinig geldige zinnen gegenereerd.")

# Opslaan
os.makedirs(os.path.dirname(SCRIPT_FILE), exist_ok=True)
with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
    for scene in scenes[:10]:
        f.write(scene + "\n")

print(f"✅ Script opgeslagen: {SCRIPT_FILE}")

# Dummy factcheck
with open(FACTCHECK_FILE, 'w', encoding='utf-8') as f:
    f.write("🔍 Factcheck (not available in free Hugging Face version). Please verify manually.\n\n")
    for scene in scenes[:10]:
        f.write(f"- {scene}\n")

print(f"🧪 Factcheck opgeslagen (placeholder): {FACTCHECK_FILE}")

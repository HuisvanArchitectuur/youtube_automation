# generate_voiceover_texts.py
import json
import os
import glob
from transformers import pipeline

# Zoek laatste script
script_files = sorted(glob.glob("data/scripts/*.txt"), reverse=True)
if not script_files:
    raise FileNotFoundError("⚠️ Geen scriptbestand gevonden in data/scripts/")

with open(script_files[0], "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Init model
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Genereer voice-over-ready tekst
voiceover_texts = []
for idx, line in enumerate(lines):
    prompt = (
        "Rewrite this scene as a natural-sounding, engaging voice-over for a short YouTube video. "
        "Use a warm, friendly male tone. Maximum 2 sentences.\n"
        f"Scene: {line}"
    )
    result = generator(prompt, max_length=80)[0]['generated_text']
    voiceover_texts.append(result.strip())

# Opslaan
os.makedirs("data/voiceovers", exist_ok=True)
with open("data/voiceovers/voiceover_texts.json", "w", encoding="utf-8") as f:
    json.dump(voiceover_texts, f, indent=2, ensure_ascii=False)

print("✅ Voice-over teksten gegenereerd per scene:")
for i, txt in enumerate(voiceover_texts, 1):
    print(f"Scene {i}: {txt}")

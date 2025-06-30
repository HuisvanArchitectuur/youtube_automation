# generate_voiceover_texts.py

import openai
import json
import glob
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Zoek het meest recente script
scripts = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
if not scripts:
    raise FileNotFoundError("❌ No scripts found in data/scripts/")
script_path = scripts[0]

# Laad scènes
with open(script_path, 'r', encoding='utf-8') as f:
    scenes = [line.strip() for line in f if line.strip()]

print(f"📄 {len(scenes)} scènes geladen.")

voiceover_texts = []

for idx, scene in enumerate(scenes):
    prompt = f"""
Rewrite the following 2-sentence scene into a smooth, natural-sounding voice-over line for a YouTube Short.

- Use a confident and warm male voice
- Keep it under 20 words
- Maintain the core scientific or factual meaning
- Make it engaging and clear

Scene:
\"{scene}\"

Only return the rewritten voice-over line.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=80
        )
        text = response['choices'][0]['message']['content'].strip().strip('"')
        voiceover_texts.append(text)
        print(f"✅ [{idx+1}] {text}")
    except Exception as e:
        print(f"⚠️  Error bij scene {idx+1}: {e}")
        voiceover_texts.append(scene)  # fallback: originele scène

# Opslaan voor voice-over generatie
os.makedirs("data/voiceovers", exist_ok=True)
with open("data/voiceovers/voiceover_texts.json", "w", encoding="utf-8") as f:
    json.dump(voiceover_texts, f, indent=2, ensure_ascii=False)

print("🎙️ Voice-over teksten opgeslagen in data/voiceovers/voiceover_texts.json")

# generate_voiceover_texts.py
import openai
import json
import glob
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Laad het meest recente scriptbestand
scripts = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
if not scripts:
    raise FileNotFoundError("❌ No scripts found in data/scripts/")
script_path = scripts[0]

with open(script_path, 'r') as f:
    scenes = [line.strip() for line in f if line.strip()]

print(f"🎬 Found {len(scenes)} scenes.")

voiceover_texts = []

for idx, scene in enumerate(scenes):
    prompt = f"""
Rewrite this sentence into a smooth, engaging voice-over line for a YouTube Short. 
Use a warm, friendly male tone. Max 2 sentences.

Scene: "{scene}"
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
        print(f"⚠️ Error for scene {idx+1}: {e}")
        voiceover_texts.append(scene)

# Sla op voor TTS
os.makedirs("data/voiceovers", exist_ok=True)
with open('data/voiceovers/voiceover_texts.json', 'w') as f:
    json.dump(voiceover_texts, f, ensure_ascii=False, indent=2)

print("✅ Voice-over lines saved to data/voiceovers/voiceover_texts.json")

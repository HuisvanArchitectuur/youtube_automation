from transformers import pipeline
import json
import glob
import os

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# 1. Vind automatisch het nieuwste scriptbestand
scripts = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
if not scripts:
    raise FileNotFoundError("Geen scripts gevonden in data/scripts/")
script_path = scripts[0]

with open(script_path, 'r') as f:
    script_text = f.read()

# 2. Split in scenes (op punt)
scenes = [s.strip() for s in script_text.split('.') if s.strip()]

voiceover_texts = []
for i, scene in enumerate(scenes):
    prompt = (
        "Herschrijf deze scene als een korte, vloeiende YouTube voice-over tekst. "
        "Gebruik een warme, vriendelijke mannelijke toon. Maximaal 2 zinnen. "
        f"Scene: '{scene}'"
    )
    result = generator(prompt, max_length=80)[0]['generated_text']
    voiceover_texts.append(result.strip())

# 3. Sla op als JSON voor TTS input
os.makedirs('data/voiceovers', exist_ok=True)
with open('data/voiceovers/voiceover_texts.json', 'w') as f:
    json.dump(voiceover_texts, f, ensure_ascii=False, indent=2)

print("Voiceover teksten per scene gegenereerd!")

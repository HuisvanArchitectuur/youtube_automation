from transformers import pipeline
import json

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# Laad het script en splits in scenes
with open('data/scripts/NAAM_VAN_SCRIPT.txt', 'r') as f:
    script_text = f.read()
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

# Sla op als JSON of TXT (voor TTS input)
with open('data/voiceovers/voiceover_texts.json', 'w') as f:
    json.dump(voiceover_texts, f, ensure_ascii=False, indent=2)

print("Voiceover teksten per scene gegenereerd!")

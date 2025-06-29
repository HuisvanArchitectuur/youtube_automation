from TTS.api import TTS
import json
import os

print("Zoek het nieuwste voiceover_texts.json...")
voiceover_texts_path = "data/voiceovers/voiceover_texts.json"
if not os.path.exists(voiceover_texts_path):
    raise FileNotFoundError(f"{voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

with open(voiceover_texts_path, "r") as f:
    texts = json.load(f)

# Initialiseer TTS voor Nederlands (standaardstem, man/vrouw niet in te stellen)
print("Initialiseer TTS...")
tts = TTS(model_name="tts_models/nl/mai/tacotron2-DCC", progress_bar=False)

os.makedirs("data/voiceovers", exist_ok=True)

for idx, text in enumerate(texts):
    print(f"Genereer voice-over voor scene {idx+1}: {text[:80]}...")
    out_path = f"data/voiceovers/voiceover_scene_{idx+1}.wav"
    tts.tts_to_file(text=text, file_path=out_path)

print("Alle voice-over bestanden gegenereerd.")

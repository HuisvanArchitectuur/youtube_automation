from TTS.api import TTS
import glob
import os
import json

print("Zoek het nieuwste voiceover_texts.json...")
# Gebruik nu de gegenereerde voiceover_texts.json
voiceover_texts_path = "data/voiceovers/voiceover_texts.json"
if not os.path.exists(voiceover_texts_path):
    raise FileNotFoundError(f"{voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

with open(voiceover_texts_path, "r") as f:
    texts = json.load(f)

# Initialiseer TTS (gebruik standaard stem)
print("Initialiseer TTS...")
tts = TTS(model_name="tts_models/nl/mai/tacotron2-DCC", progress_bar=False)

for idx, text in enumerate(texts):
    print(f"Genereer voice-over voor scene {idx+1}: {text[:80]}...")
    out_path = f"data/voiceovers/voiceover_scene_{idx+1}.wav"
    tts.tts_to_file(text=text, file_path=out_path)

print("Alle voice-over bestanden gegenereerd.")

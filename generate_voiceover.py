from TTS.api import TTS
import glob
import os
import json

# Path naar de gegenereerde voiceover-zinnen
voiceover_texts_path = "data/voiceovers/voiceover_texts.json"
if not os.path.exists(voiceover_texts_path):
    raise FileNotFoundError(f"{voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

print("Zoek het nieuwste voiceover_texts.json...")
with open(voiceover_texts_path, "r") as f:
    texts = json.load(f)

# Kies hier een stemmodel
# ENGLISH: "tts_models/en/ljspeech/glow-tts"
# DUTCH (NL): "tts_models/nl/mai/tacotron2-DDC"  (alleen als beschikbaar)
# Je kan dit aanpassen naar wens!
model_name = "tts_models/en/ljspeech/glow-tts"  # Voor een warme, mannelijke stem

print("Initialiseer TTS...")
tts = TTS(model_name=model_name, progress_bar=False)

# Bestandsnaam voor de voiceover audio
voiceover_wav = f"data/voiceovers/voiceover.wav"
if os.path.exists(voiceover_wav):
    os.remove(voiceover_wav)  # verwijder oude file

print(f"Start synthese van {len(texts)} zinnen...")

# Combineer alle zinnen tot één audio
tts.tts_to_file(text=" ".join(texts), file_path=voiceover_wav)

print(f"Voice-over gegenereerd in {voiceover_wav}")

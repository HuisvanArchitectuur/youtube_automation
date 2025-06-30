from TTS.api import TTS
import json
import os

voiceover_texts_path = "data/voiceovers/voiceover_texts.json"
if not os.path.exists(voiceover_texts_path):
    raise FileNotFoundError(f"{voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

with open(voiceover_texts_path, "r") as f:
    texts = json.load(f)

# Kies hier een stemmodel
# ENGLISH: "tts_models/en/ljspeech/glow-tts"
# DUTCH (NL): "tts_models/nl/mai/tacotron2-DDC"  (alleen als beschikbaar)
model_name = "tts_models/en/ljspeech/glow-tts"  # Voor warme, mannelijke stem

print("Initialiseer TTS...")
tts = TTS(model_name=model_name, progress_bar=False)

os.makedirs("data/voiceovers", exist_ok=True)

voice_files = []
for idx, text in enumerate(texts):
    audio_file = f"data/voiceovers/voiceover_scene_{idx+1}.wav"
    print(f"Genereer voice-over voor scene {idx+1}: {text[:80]}...")
    tts.tts_to_file(text=text, file_path=audio_file)
    voice_files.append(audio_file)

print("Alle losse voice-over bestanden per scene gegenereerd:", voice_files)

# (OPTIONEEL) Voeg alle audio's samen tot één bestand:
from pydub import AudioSegment
audio = AudioSegment.silent(duration=0)
for audio_file in voice_files:
    audio += AudioSegment.from_wav(audio_file)
audio.export("data/voiceovers/voiceover.wav", format="wav")
print("Samengevoegd audiobestand aangemaakt als voiceover.wav")

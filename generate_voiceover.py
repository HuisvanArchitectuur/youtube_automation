# generate_voiceover.py

from TTS.api import TTS
import json
import os
from pydub import AudioSegment

VOICEOVER_TEXTS_PATH = "data/voiceovers/voiceover_texts.json"
OUTPUT_DIR = "data/voiceovers"
COMBINED_AUDIO_PATH = f"{OUTPUT_DIR}/voiceover.wav"

# Check inputbestand
if not os.path.exists(VOICEOVER_TEXTS_PATH):
    raise FileNotFoundError(f"{VOICEOVER_TEXTS_PATH} not found! Run generate_voiceover_texts.py first.")

# Laad tekst
with open(VOICEOVER_TEXTS_PATH, "r", encoding="utf-8") as f:
    texts = json.load(f)

# Initialiseer TTS model
model_name = "tts_models/en/ljspeech/glow-tts"  # Warm mannelijke Engelse stem
print(f"🎤 Loading TTS model: {model_name}")
tts = TTS(model_name=model_name, progress_bar=False)

# Zorg dat outputmap bestaat
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Genereer per scene audio
voice_files = []
for idx, text in enumerate(texts):
    audio_path = f"{OUTPUT_DIR}/voiceover_scene_{idx+1}.wav"
    print(f"🔊 Generating audio for scene {idx+1}: {text}")
    try:
        tts.tts_to_file(text=text, file_path=audio_path)
        voice_files.append(audio_path)
    except Exception as e:
        print(f"⚠️ Failed to generate scene {idx+1}: {e}")

# Combineer audio's
if voice_files:
    print("🎧 Combining all voice-over scenes into one file...")
    combined = AudioSegment.silent(duration=0)
    for vf in voice_files:
        combined += AudioSegment.from_wav(vf)
    combined.export(COMBINED_AUDIO_PATH, format="wav")
    print(f"✅ Combined audio saved: {COMBINED_AUDIO_PATH}")
else:
    raise Exception("❌ No voice files were generated!")

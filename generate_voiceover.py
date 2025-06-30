# generate_voiceover.py
from TTS.api import TTS
from pydub import AudioSegment
import json
import os

# === Config ===
VOICE_MODEL = "tts_models/en/ljspeech/glow-tts"  # Warme mannelijke Engelse stem
INPUT_FILE = "data/voiceovers/voiceover_texts.json"
OUTPUT_DIR = "data/voiceovers"
MERGED_FILE = os.path.join(OUTPUT_DIR, "voiceover.wav")

# === 1. Voice-over zinnen laden ===
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"❌ {INPUT_FILE} not found. Please run generate_voiceover_texts.py first.")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    texts = json.load(f)

# === 2. Initialiseer TTS-model ===
print(f"🗣️ Initializing voice model: {VOICE_MODEL}")
tts = TTS(model_name=VOICE_MODEL, progress_bar=False)

os.makedirs(OUTPUT_DIR, exist_ok=True)
voice_files = []

# === 3. Genereer losse voice-over bestanden ===
for idx, text in enumerate(texts):
    output_path = os.path.join(OUTPUT_DIR, f"voiceover_scene_{idx+1}.wav")
    print(f"🎙️ Generating voiceover {idx+1}/{len(texts)}: {text[:60]}...")
    try:
        tts.tts_to_file(text=text, file_path=output_path)
        voice_files.append(output_path)
    except Exception as e:
        print(f"⚠️ Error generating voiceover for scene {idx+1}: {e}")

print("✅ Alle losse voice-over bestanden gegenereerd.")

# === 4. Combineer tot 1 bestand ===
audio = AudioSegment.silent(duration=0)
for f in voice_files:
    audio += AudioSegment.from_wav(f)

audio.export(MERGED_FILE, format="wav")
print(f"📦 Samengevoegde voiceover opgeslagen: {MERGED_FILE}")

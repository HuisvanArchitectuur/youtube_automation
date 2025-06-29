from TTS.api import TTS
import os
import json
from pydub import AudioSegment

# ---- 1. Laad de voice-over teksten per scene ----
voiceover_texts_path = 'data/voiceovers/voiceover_texts.json'
if not os.path.exists(voiceover_texts_path):
    raise FileNotFoundError(f"{voiceover_texts_path} niet gevonden! Genereer eerst voiceover_texts.json.")

with open(voiceover_texts_path, 'r', encoding='utf-8') as f:
    voiceover_texts = json.load(f)

# ---- 2. Initialiseert TTS met mannelijke, warme stem ----
# Bijvoorbeeld: tts_models/nl/mai/tacotron2-DDC ondersteunt NL, maar kies eventueel een andere warme mannenstem!
tts = TTS(model_name="tts_models/nl/mai/tacotron2-DDC", speaker_idx=None, progress_bar=False, gpu=False)

# ---- 3. Maak voiceover fragmenten ----
output_dir = "data/voiceovers"
os.makedirs(output_dir, exist_ok=True)
audio_fragments = []

for idx, text in enumerate(voiceover_texts):
    out_path = f"{output_dir}/scene_{idx+1}.wav"
    print(f"[INFO] Synthese scene {idx+1}: {text[:80]}...")
    # Synthese: 
    tts.tts_to_file(text=text, file_path=out_path)
    audio_fragments.append(AudioSegment.from_wav(out_path))

# ---- 4. Combineer alle audiofragmenten tot 1 voiceover ----
combined = sum(audio_fragments)
voiceover_combined_path = f"{output_dir}/voiceover_combined.wav"
combined.export(voiceover_combined_path, format="wav")
print(f"[SUCCESS] Voice-over aangemaakt: {voiceover_combined_path}")


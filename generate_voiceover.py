from TTS.api import TTS
import glob
import os

print("Zoek het nieuwste script...")
scripts = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
print("Gevonden scripts:", scripts)
if not scripts:
    raise Exception("GEEN scripts gevonden in data/scripts/!")

script_path = scripts[0]
print("Nieuwste script:", script_path)

with open(script_path, 'r') as f:
    text = f.read()

print("Script inhoud (eerste 200 tekens):", text[:200])

try:
    print("Initialiseer TTS...")
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
    print("TTS init gelukt.")
except Exception as e:
    print("FOUT bij initialiseren TTS:", e)
    raise

voice_path = f"data/voiceovers/{os.path.basename(script_path).replace('.txt','.wav')}"
print("Output voice file:", voice_path)

try:
    print("Start synthese...")
    tts.tts_to_file(text=text, file_path=voice_path)
    print("Synthese gelukt.")
except Exception as e:
    print("FOUT bij synthese:", e)
    raise

print(f"Voice-over gegenereerd in {voice_path}")

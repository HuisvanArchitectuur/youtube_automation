from TTS.api import TTS
import glob

# Zoek het nieuwste script
scripts = sorted(glob.glob('data/scripts/*.txt'), reverse=True)
script_path = scripts[0]

with open(script_path, 'r') as f:
    text = f.read()

tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
voice_path = f"data/voiceovers/{os.path.basename(script_path).replace('.txt','.wav')}"
tts.tts_to_file(text=text, file_path=voice_path)

print(f"Voice-over gegenereerd in {voice_path}")

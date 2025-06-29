import os
import glob
import json

# Lees voice-over en visual lijst
voice_files = sorted(glob.glob('data/voiceovers/*.wav'), reverse=True)
audio_path = voice_files[0]
output_path = 'data/videos/output.mp4'

with open('data/videos/visual_list.json', 'r') as f:
    visual_paths = json.load(f)

num_visuals = len(visual_paths)

# Bepaal audiolengte (in seconden)
import wave
with wave.open(audio_path, 'rb') as wav_file:
    frames = wav_file.getnframes()
    rate = wav_file.getframerate()
    duration = frames / float(rate)

# Duur per beeld (verdeel audio gelijkmatig over alle visuals)
duration_per_image = duration / num_visuals

# Maak een ffmpeg bestand met inputlijst
with open('data/videos/images.txt', 'w') as f:
    for path in visual_paths:
        f.write(f"file '{os.path.abspath(path)}'\n")
        f.write(f"duration {duration_per_image}\n")
    # Herhaal laatste beeld zodat de video niet te vroeg stopt
    f.write(f"file '{os.path.abspath(visual_paths[-1])}'\n")

# Zet alles om naar video
cmd = (
    f"ffmpeg -y -f concat -safe 0 -i data/videos/images.txt "
    f"-i '{audio_path}' -vsync vfr -pix_fmt yuv420p "
    f"-c:v libx264 -c:a aac -b:a 192k -shortest '{output_path}'"
)
os.system(cmd)

print(f"Video aangemaakt in {output_path}")

import os

os.makedirs('data/videos', exist_ok=True)
import os
import json
import glob
from pydub import AudioSegment

# 1. Laad visuals
visuals_file = 'data/videos/visual_list.json'
if not os.path.exists(visuals_file):
    raise FileNotFoundError(f"Visual list {visuals_file} bestaat niet!")
with open(visuals_file, 'r') as f:
    visual_paths = json.load(f)
if not visual_paths:
    raise Exception("Geen visuals gevonden in visual_list.json")

# 2. Pak nieuwste voiceover
voice_files = sorted(glob.glob('data/voiceovers/*.wav'), reverse=True)
if not voice_files:
    raise Exception("Geen voiceover gevonden in data/voiceovers/")
audio_path = voice_files[0]

# 3. Meet de lengte van de audio
audio = AudioSegment.from_wav(audio_path)
audio_length_sec = len(audio) / 1000  # in seconden

# 4. Bereken duur per visual
n_visuals = len(visual_paths)
img_duration = round(audio_length_sec / n_visuals, 2)
print(f"[DEBUG] {n_visuals} visuals, audio: {audio_length_sec:.2f} sec, duration per visual: {img_duration} sec")

# 5. Maak ffmpeg concat-bestand
concat_file = "data/videos/concat.txt"
with open(concat_file, "w") as f:
    for img in visual_paths:
        f.write(f"file '{os.path.abspath(img)}'\n")
        f.write(f"duration {img_duration}\n")
    # Zorg dat de laatste frame blijft staan tot audio klaar is
    f.write(f"file '{os.path.abspath(visual_paths[-1])}'\n")

# 6. Genereer video met beeldwissels
tmp_video = "data/videos/tmp_visuals.mp4"
cmd_img2vid = (
    f"ffmpeg -y -f concat -safe 0 -i {concat_file} "
    f"-vsync vfr -pix_fmt yuv420p -vf scale=940:528 -r 25 {tmp_video}"
)
print(f"[DEBUG] Run images->video: {cmd_img2vid}")
if os.system(cmd_img2vid) != 0:
    raise Exception("ffmpeg images->video faalde!")

# 7. Voeg audio toe aan de video
output_path = "data/videos/output.mp4"
cmd_final = (
    f"ffmpeg -y -i {tmp_video} -i {audio_path} "
    f"-c:v libx264 -c:a aac -shortest -pix_fmt yuv420p {output_path}"
)
print(f"[DEBUG] Run video+audio: {cmd_final}")
if os.system(cmd_final) != 0:
    raise Exception("ffmpeg video+audio faalde!")

print(f"Video aangemaakt in {output_path}")

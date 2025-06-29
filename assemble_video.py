import os
import json
import glob
from pydub import AudioSegment

# Zorg dat data/videos bestaat
os.makedirs("data/videos", exist_ok=True)

# 1. Laad alle visuals uit visual_list.json
visual_list_path = "data/videos/visual_list.json"
if not os.path.isfile(visual_list_path):
    raise FileNotFoundError(f"{visual_list_path} bestaat niet!")

with open(visual_list_path, 'r') as f:
    visual_paths = json.load(f)

if len(visual_paths) == 0:
    raise Exception("Geen afbeeldingen gevonden in visual_list.json!")

# 2. Pak het nieuwste voiceover-bestand (WAV)
voice_files = sorted(glob.glob('data/voiceovers/*.wav'), reverse=True)
if not voice_files:
    raise Exception("Geen voiceover gevonden in data/voiceovers/")
audio_path = voice_files[0]

# 3. Meet de lengte van de audio
audio = AudioSegment.from_wav(audio_path)
audio_length_sec = len(audio) / 1000  # ms naar seconden

# 4. Bereken de lengte van elk beeld in de video
n_visuals = len(visual_paths)
img_duration = audio_length_sec / n_visuals

print(f"[DEBUG] {n_visuals} visuals, audio: {audio_length_sec:.2f} sec, duration per visual: {img_duration:.2f} sec")

# 5. Maak een ffmpeg concat-list bestand
concat_file = "data/videos/concat.txt"
with open(concat_file, "w") as f:
    for img in visual_paths:
        f.write(f"file '{os.path.abspath(img)}'\n")
        f.write(f"duration {img_duration}\n")
    # Herhaal laatste frame zodat audio nooit voortijdig stopt
    f.write(f"file '{os.path.abspath(visual_paths[-1])}'\n")

# 6. Genereer een video met beeldwissels
tmp_video = "data/videos/tmp_visuals.mp4"
ffmpeg_images_cmd = (
    f"ffmpeg -y -f concat -safe 0 -i {concat_file} "
    f"-vsync vfr -pix_fmt yuv420p -vf scale=940:528 -r 25 {tmp_video}"
)
print("[DEBUG] Run images->video:", ffmpeg_images_cmd)
os.system(ffmpeg_images_cmd)

# 7. Voeg audio toe aan de video
output_path = "data/videos/output.mp4"
ffmpeg_final_cmd = (
    f"ffmpeg -y -i {tmp_video} -i {audio_path} "
    f"-c:v libx264 -c:a aac -shortest -pix_fmt yuv420p {output_path}"
)
print("[DEBUG] Run video+audio:", ffmpeg_final_cmd)
os.system(ffmpeg_final_cmd)

print(f"Video aangemaakt in {output_path}")

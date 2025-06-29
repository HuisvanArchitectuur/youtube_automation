import os
import json
import glob
from pydub import AudioSegment

# 1. Laad alle visuals uit visual_list.json
with open('data/videos/visual_list.json', 'r') as f:
    visual_paths = json.load(f)

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

# 5. Maak een ffmpeg concat-list bestand
concat_file = "data/videos/concat.txt"
with open(concat_file, "w") as f:
    for img in visual_paths:
        f.write(f"file '{os.path.abspath(img)}'\n")
        f.write(f"duration {img_duration}\n")
    # Herhaal laatste frame zodat audio niet voortijdig stopt
    f.write(f"file '{os.path.abspath(visual_paths[-1])}'\n")

# 6. Genereer een video met beeldwissels
tmp_video = "data/videos/tmp_visuals.mp4"
os.system(
    f"ffmpeg -y -f concat -safe 0 -i {concat_file} -vsync vfr -pix_fmt yuv420p -vf scale=940:528 {tmp_video}"
)

# 7. Voeg audio toe aan de video
output_path = "data/videos/output.mp4"
os.system(
    f"ffmpeg -y -i {tmp_video} -i {audio_path} -c:v libx264 -c:a aac -shortest -pix_fmt yuv420p {output_path}"
)

print(f"Video aangemaakt in {output_path}")

import os
import json
import glob
from pydub import AudioSegment

os.makedirs('data/videos', exist_ok=True)

# 1. Laad visuals
visuals_file = 'data/videos/visual_list.json'
if not os.path.exists(visuals_file):
    raise FileNotFoundError(f"Visual list {visuals_file} bestaat niet!")
with open(visuals_file, 'r') as f:
    visual_paths = json.load(f)
if not visual_paths:
    raise Exception("Geen visuals gevonden in visual_list.json")

# 2. Laad alle losse voiceover_scene_X.wav files (en check lengte)
voice_files = sorted(glob.glob('data/voiceovers/voiceover_scene_*.wav'))
if len(voice_files) != len(visual_paths):
    raise Exception(f"Mismatch tussen visuals ({len(visual_paths)}) en voiceovers ({len(voice_files)}). Check je pipeline.")

# 3. Voor elke scene: maak een kort mp4-tje van beeld + audio
scene_videos = []
for idx, (img, voice) in enumerate(zip(visual_paths, voice_files)):
    scene_video = f"data/videos/scene_{idx+1}.mp4"
    # Haal duur van audio in seconden
    audio = AudioSegment.from_wav(voice)
    duration = len(audio) / 1000.0
    # ffmpeg: één plaatje + audio, exact zo lang als audio
    cmd = (
        f"ffmpeg -y -loop 1 -i \"{img}\" -i \"{voice}\" "
        f"-c:v libx264 -t {duration} -pix_fmt yuv420p -vf scale=940:528 "
        f"-c:a aac -shortest -r 25 \"{scene_video}\""
    )
    print(f"[DEBUG] Maak scene-video: {cmd}")
    if os.system(cmd) != 0:
        raise Exception(f"ffmpeg scene {idx+1} faalde!")
    scene_videos.append(scene_video)

# 4. Maak concat-list voor alle scenes
concat_file = "data/videos/scenes_concat.txt"
with open(concat_file, "w") as f:
    for sv in scene_videos:
        f.write(f"file '{os.path.abspath(sv)}'\n")

# 5. Plak alles aan elkaar
output_path = "data/videos/output.mp4"
cmd_final = (
    f"ffmpeg -y -f concat -safe 0 -i {concat_file} -c copy {output_path}"
)
print(f"[DEBUG] Concateneer scenes: {cmd_final}")
if os.system(cmd_final) != 0:
    raise Exception("ffmpeg video concat faalde!")

print(f"Video aangemaakt in {output_path}")

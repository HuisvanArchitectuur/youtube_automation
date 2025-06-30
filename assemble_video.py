# assemble_video.py

import os
import json
import glob
from pydub import AudioSegment

# 📂 Paden
VISUAL_LIST_PATH = "data/videos/visual_list.json"
VOICEOVER_DIR = "data/voiceovers"
OUTPUT_DIR = "data/videos"
FINAL_OUTPUT = f"{OUTPUT_DIR}/output.mp4"
CONCAT_LIST = f"{OUTPUT_DIR}/scenes_concat.txt"

# ✅ Check bestanden
if not os.path.exists(VISUAL_LIST_PATH):
    raise FileNotFoundError(f"{VISUAL_LIST_PATH} not found!")

with open(VISUAL_LIST_PATH, "r", encoding="utf-8") as f:
    visual_paths = json.load(f)
if not visual_paths:
    raise Exception("❌ visual_list.json is empty.")

voice_files = sorted(glob.glob(f"{VOICEOVER_DIR}/voiceover_scene_*.wav"))
if len(voice_files) != len(visual_paths):
    raise Exception(f"Mismatch: {len(voice_files)} voice files vs {len(visual_paths)} visuals.")

# 🔁 Per scene: combineer visual + audio tot clip
scene_videos = []
for idx, (img, audio) in enumerate(zip(visual_paths, voice_files)):
    scene_path = f"{OUTPUT_DIR}/scene_{idx+1}.mp4"
    audio_duration = AudioSegment.from_wav(audio).duration_seconds

    ffmpeg_cmd = (
        f"ffmpeg -y -loop 1 -i \"{img}\" -i \"{audio}\" "
        f"-c:v libx264 -t {audio_duration:.2f} -pix_fmt yuv420p "
        f"-vf scale=940:528 -c:a aac -shortest -r 25 \"{scene_path}\""
    )

    print(f"[🎬] Rendering scene {idx+1}: {ffmpeg_cmd}")
    if os.system(ffmpeg_cmd) != 0:
        raise Exception(f"❌ FFmpeg failed for scene {idx+1}")

    scene_videos.append(scene_path)

# 📄 Concat list
with open(CONCAT_LIST, "w") as f:
    for scene in scene_videos:
        f.write(f"file '{os.path.abspath(scene)}'\n")

# 🧩 Samenvoegen
ffmpeg_concat_cmd = (
    f"ffmpeg -y -f concat -safe 0 -i {CONCAT_LIST} -c copy {FINAL_OUTPUT}"
)

print(f"[🧵] Concatenating scenes into final video...")
if os.system(ffmpeg_concat_cmd) != 0:
    raise Exception("❌ FFmpeg concat failed.")

print(f"✅ Final video assembled: {FINAL_OUTPUT}")

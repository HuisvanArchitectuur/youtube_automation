# assemble_video.py

import os
import json
import glob
from pydub import AudioSegment

# 📂 Paden
VISUAL_LIST_PATH = "data/videos/visual_list.json"
VOICEOVER_DIR = "data/voiceovers"
OUTPUT_VIDEO_PATH = "data/videos/output.mp4"
SCENE_DIR = "data/videos"
CONCAT_LIST_PATH = f"{SCENE_DIR}/scenes_concat.txt"

# 📄 Laad visuals
if not os.path.exists(VISUAL_LIST_PATH):
    raise FileNotFoundError(f"{VISUAL_LIST_PATH} not found!")
with open(VISUAL_LIST_PATH, "r", encoding="utf-8") as f:
    visuals = json.load(f)

# 🔊 Laad voiceovers
voice_files = sorted(glob.glob(f"{VOICEOVER_DIR}/voiceover_scene_*.wav"))
if len(visuals) != len(voice_files):
    raise Exception(f"❌ Mismatch between visuals ({len(visuals)}) and voiceovers ({len(voice_files)})")

# 🎬 Maak individuele clips
scene_paths = []
for idx, (img, audio) in enumerate(zip(visuals, voice_files)):
    duration = AudioSegment.from_wav(audio).duration_seconds
    scene_path = f"{SCENE_DIR}/scene_{idx+1}.mp4"

    cmd = (
        f"ffmpeg -y -loop 1 -i \"{img}\" -i \"{audio}\" "
        f"-c:v libx264 -t {duration} -pix_fmt yuv420p "
        f"-vf scale=940:528 -c:a aac -shortest -r 25 \"{scene_path}\""
    )
    print(f"[🔧] Generating scene {idx+1} with ffmpeg...")
    if os.system(cmd) != 0:
        raise Exception(f"❌ FFmpeg failed for scene {idx+1}")
    scene_paths.append(scene_path)

# 📜 Maak concat list
with open(CONCAT_LIST_PATH, "w") as f:
    for sp in scene_paths:
        f.write(f"file '{os.path.abspath(sp)}'\n")

# 🎞️ Plak alles samen
cmd_final = (
    f"ffmpeg -y -f concat -safe 0 -i \"{CONCAT_LIST_PATH}\" -c copy \"{OUTPUT_VIDEO_PATH}\""
)
print("[🎥] Merging scenes into final video...")
if os.system(cmd_final) != 0:
    raise Exception("❌ FFmpeg concat failed")

print(f"✅ Video created: {OUTPUT_VIDEO_PATH}")

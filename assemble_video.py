import os
import json
import glob
import subprocess
from pydub import AudioSegment

visuals_file = 'data/videos/visual_list.json'
voice_dir = 'data/voiceovers'

if not os.path.exists(visuals_file):
    raise FileNotFoundError(f"❌ Visual list missing: {visuals_file}")
with open(visuals_file, 'r') as f:
    visual_paths = json.load(f)
if not visual_paths:
    raise Exception("❌ visual_list.json is empty!")

voice_files = sorted(glob.glob(f'{voice_dir}/voiceover_scene_*.wav'))
if len(voice_files) != len(visual_paths):
    raise Exception(f"Mismatch: {len(visual_paths)} visuals vs {len(voice_files)} voiceovers.")

scene_videos = []
for idx, (img, voice) in enumerate(zip(visual_paths, voice_files)):
    scene_video = f"data/videos/scene_{idx+1}.mp4"
    audio = AudioSegment.from_wav(voice)
    duration = len(audio) / 1000.0

    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", img, "-i", voice,
        "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
        "-vf", "scale=940:528", "-c:a", "aac", "-shortest", "-r", "25", scene_video
    ]
    print(f"🎞️ Creating scene {idx+1}: {scene_video}")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(result.stderr.decode())
        raise Exception(f"❌ ffmpeg failed for scene {idx+1}")

    scene_videos.append(scene_video)

concat_file = "data/videos/scenes_concat.txt"
with open(concat_file, "w") as f:
    for sv in scene_videos:
        f.write(f"file '{os.path.abspath(sv)}'\n")

output_path = "data/videos/output.mp4"
cmd_final = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
    "-c", "copy", output_path
]
print(f"🎬 Final concat: {output_path}")
result = subprocess.run(cmd_final, capture_output=True)
if result.returncode != 0:
    print(result.stderr.decode())
    raise Exception("❌ Final video concat failed!")

print(f"✅ Final video saved: {output_path}")

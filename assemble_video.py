import os
import glob

image_path = 'data/videos/visual.jpg'
voice_files = sorted(glob.glob('data/voiceovers/*.wav'), reverse=True)
audio_path = voice_files[0]
output_path = 'data/videos/output.mp4'

cmd = (
    f'ffmpeg -y -loop 1 -i "{image_path}" -i "{audio_path}" -c:v libx264 -tune stillimage '
    f'-c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{output_path}"'
)
os.system(cmd)
print(f"Video aangemaakt in {output_path}")

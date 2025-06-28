import os

image_path = 'data/videos/visual.png'
audio_path = 'data/voiceovers/....mp3'
output_path = 'data/videos/output.mp4'

os.system(
    f'ffmpeg -loop 1 -i "{image_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k '
    f'-pix_fmt yuv420p -shortest "{output_path}"'
)

print("Video samengesteld!")

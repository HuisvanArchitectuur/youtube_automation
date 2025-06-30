import os
import json

folders = [
    "data",
    "data/scripts",
    "data/voiceovers",
    "data/videos",
    "data/thumbnails"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"[INIT] Folder ensured: {folder}")

# Topic placeholder
topic_path = "data/topic.json"
if not os.path.exists(topic_path):
    with open(topic_path, "w") as f:
        json.dump({"topic": "The rise of AI in daily life"}, f)
    print("[INIT] Default topic.json created.")

# Dummy script
script_path = "data/scripts/script.txt"
if not os.path.exists(script_path):
    with open(script_path, "w") as f:
        f.write("AI is changing how we work.\nIt’s reshaping every part of life.")
    print("[INIT] Dummy script.txt created.")

# Dummy voiceovers
voice_txt = "data/voiceovers/voiceover_texts.json"
if not os.path.exists(voice_txt):
    with open(voice_txt, "w") as f:
        json.dump(["AI is reshaping our world.", "Even your toaster might get smarter soon!"], f)
    print("[INIT] Dummy voiceover_texts.json created.")

# Fallback visual
fallback_img = "data/videos/fallback_1.jpg"
if not os.path.exists(fallback_img):
    from PIL import Image
    img = Image.new('RGB', (1280, 720), color='black')
    img.save(fallback_img)
    print("[INIT] Default fallback image created.")

print("[✅] Init complete.")

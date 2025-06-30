# generate_script.py

import json
import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

if not huggingface_token:
    raise ValueError("❌ HUGGINGFACE_API_KEY niet gevonden in .env of GitHub Secrets.")

generator = pipeline(
    "text-generation",
    model="tiiuae/falcon-7b-instruct",
    tokenizer="tiiuae/falcon-7b-instruct",
    use_auth_token=huggingface_token,
    device=0 if os.getenv("USE_CUDA", "0") == "1" else -1,
)

# Laad onderwerp
with open("data/topic.json", "r") as f:
    topic_data = json.load(f)

topic = topic_data.get("topic", "").strip()
if not topic:
    raise Exception("⚠️ Geen geldig onderwerp gevonden in topic.json")

prompt = f"""
Bedenk een origineel, trending en visueel boeiend script over: "{topic}" 
voor een YouTube Shorts video.

Regels:
- Elke scene bevat exact 2 zinnen
- Maximaal 8 woorden per zin
- Geen hashtags, geen cijfers, geen emoji's
- Wetenschappelijk correct of waargebeurd
- Visueel aantrekkelijk geformuleerd
- Maximaal 5 scenes (dus 5 regels)
- Zet elke scene op een nieuwe regel

⚠️ Alleen de regels van het script teruggeven, zonder extra uitleg.
"""

print(f"📥 Prompt naar model:\n{prompt}")

result = generator(prompt, max_new_tokens=250, do_sample=True, temperature=0.7)
script_output = result[0]['generated_text']

# Filter en splits regels
lines = [
    line.strip()
    for line in script_output.strip().split("\n")
    if line.strip() and len(line.split()) >= 4  # minimaal 2 korte zinnen
]

if len(lines) < 3:
    raise Exception("⚠️ Te weinig geldige zinnen gegenereerd.")

# Opslaan
os.makedirs("data/scripts", exist_ok=True)
script_path = "data/scripts/script.txt"
with open(script_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Script opgeslagen in {script_path}")

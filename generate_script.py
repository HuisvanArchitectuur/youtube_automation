# generate_script.py
import os
import json
from openai import OpenAIError
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_FILE = "data/topic.json"
SCRIPT_PATH = "data/scripts/script.txt"

# ⬇️ Prompt op basis van jouw wensen
with open(TOPIC_FILE, "r", encoding="utf-8") as f:
    topic_data = json.load(f)
    topic = topic_data.get("topic", "")

prompt = f"""
Je taak: schrijf een script voor een YouTube Shorts video over het onderwerp: "{topic}".
Regels:
- Gebruik maximaal 8 woorden per zin
- Maak het visueel en boeiend
- Gebruik geen hashtags, geen cijfers, geen emoji's
- Zorg dat het hele script wetenschappelijk klopt en op feiten gebaseerd is
- Geef elke zin op een nieuwe regel, max 10 regels

Alleen het script teruggeven, geen uitleg of formatting.
"""

try:
    print("🧠 Prompt sturen naar GPT...")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=300
    )

    script_raw = response['choices'][0]['message']['content'].strip()
    lines = [line.strip() for line in script_raw.split("\n") if line.strip()]
    
    # 🔎 Check op minimum aantal zinnen
    if len(lines) < 4:
        raise Exception("⚠️ Te weinig geldige zinnen gegenereerd.")

    # 📝 Opslaan
    os.makedirs(os.path.dirname(SCRIPT_PATH), exist_ok=True)
    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Script opgeslagen in {SCRIPT_PATH} ({len(lines)} zinnen)")

except OpenAIError as e:
    print(f"❌ OpenAI fout: {e}")
    raise
except Exception as e:
    print(f"❌ Andere fout bij scriptgeneratie: {e}")
    raise

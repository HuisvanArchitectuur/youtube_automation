# generate_topic.py
import os
import json
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# Init model (geen API key nodig!)
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Prompt voor topicgeneratie
prompt = (
    "Bedenk een origineel, trending en visueel boeiend onderwerp "
    "voor een YouTube Shorts video. Maximaal 8 woorden. "
    "Geen hashtags, geen cijfers — enkel het onderwerp."
)

# Genereer het topic
print("🚀 Genereer YouTube-topic...")
result = generator(prompt, max_length=20)[0]['generated_text']
topic = result.strip().strip('"')

# Opslaan
os.makedirs("data", exist_ok=True)
with open("data/topic.json", "w") as f:
    json.dump({"topic": topic}, f)

print(f"✅ Topic opgeslagen in data/topic.json: {topic}")

# generate_topic.py
import openai
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import random

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_OUTPUT = "data/topic.json"
TRENDING_OUTPUT = "data/trending_topics.json"

# Stap 1: Prompt
prompt = """
Generate 5 unique and engaging YouTube Shorts topics based on current global trends and evergreen viral subjects.

Each topic should be short, curiosity-driven, and ideal for a 60-second video.

Do not number them, and don't add explanations.

Examples:
- Why your brain can't resist sugar
- The mystery of black holes
- What if time stopped for 1 second
- AI that's smarter than humans
- How octopuses escape any trap
"""

# Stap 2: Vraag GPT-4 om onderwerpen
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200
    )
    result = response["choices"][0]["message"]["content"]
    topics = [t.strip("-• ").strip() for t in result.strip().split("\n") if t.strip()]
    print(f"✅ Topics generated: {topics}")
except Exception as e:
    print(f"⚠️ GPT-4 failed: {e}")
    topics = [
        "The strangest place on Earth",
        "What if humans had night vision",
        "Why cats always land on their feet",
        "Secrets of the Bermuda Triangle",
        "The truth about immortality"
    ]

# Stap 3: Save als lijst
os.makedirs(os.path.dirname(TRENDING_OUTPUT), exist_ok=True)
with open(TRENDING_OUTPUT, "w") as f:
    json.dump(topics, f, indent=2)

# Stap 4: Kies er één voor deze video
chosen = random.choice(topics)
with open(TOPIC_OUTPUT, "w") as f:
    json.dump({"topic": chosen, "generated_at": datetime.now().isoformat()}, f)

print(f"🎯 Selected topic: {chosen}")

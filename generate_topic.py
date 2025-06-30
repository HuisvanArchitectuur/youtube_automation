from transformers import pipeline
import json
import random
from pytrends.request import TrendReq
from datetime import datetime

# Load text-to-text model
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Setup Google Trends (global / US-based)
pytrends = TrendReq(hl='en-US', tz=360)

try:
    trends_df = pytrends.trending_searches(pn='united_states')  # Or 'global'
    trending_list = trends_df[0].tolist()[:5]
    print("📈 Trending topics from Google Trends:", trending_list)
except Exception as e:
    print(f"⚠️ Could not fetch trending topics ({e}). Using fallback list.")
    trending_list = [
        "AI replacing human jobs",
        "Mysterious ancient civilizations",
        "The future of space travel",
        "Why do we dream?",
        "Can animals sense earthquakes?",
        "Time travel paradoxes",
        "Dark matter mysteries",
        "Immortality science breakthroughs"
    ]

# Prompt for LLM to turn trends into video-friendly topics
prompt = (
    f"Generate 5 unique, interesting YouTube Shorts topics based on: {', '.join(trending_list)}.\n"
    "Just list the titles — no explanations, no numbering. Use a catchy, curiosity-driven style."
)

results = generator(prompt, max_length=100)
print("🧠 LLM output:", results)

topics_raw = results[0]['generated_text']
topics = [t.strip() for t in topics_raw.split('\n') if t.strip()]
print("✅ Parsed topics:", topics)

# Ensure at least 5 topics
while len(topics) < 5:
    topics.append(f"Generated Topic {len(topics)+1}")

# Save full list
with open("data/trending_topics.json", "w") as f:
    json.dump(topics, f, indent=2)

# Choose 1 topic to use
chosen_topic = random.choice(topics)
with open("data/topic.json", "w") as f:
    json.dump({"topic": chosen_topic, "generated_at": datetime.now().isoformat()}, f)

print(f"🎯 Selected topic for script: {chosen_topic}")

# generate_topic.py
import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_FILE = "data/topic.json"
os.makedirs(os.path.dirname(TOPIC_FILE), exist_ok=True)

prompt = (
    "Give me a short, viral YouTube Shorts topic idea in English related to futuristic AI or science. "
    "Only return the raw topic title, no hashtags, no explanations."
)

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.9,
    max_tokens=50
)

topic = response.choices[0].message.content.strip().strip('"')
with open(TOPIC_FILE, "w", encoding="utf-8") as f:
    json.dump({"topic": topic}, f)

print(f"🎯 Generated topic: {topic}")

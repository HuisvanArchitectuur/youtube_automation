# generate_topic.py
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPIC_FILE = "data/topic.json"
os.makedirs(os.path.dirname(TOPIC_FILE), exist_ok=True)

prompt = """
Come up with a unique and trending topic for a 60-second YouTube Shorts video.
The topic should be surprising, curious, and relate to science, technology, or human behavior.
Only return the topic sentence — no explanation, no hashtags.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9,
    max_tokens=50
)

topic = response['choices'][0]['message']['content'].strip().strip('"')
with open(TOPIC_FILE, 'w', encoding='utf-8') as f:
    json.dump({"topic": topic}, f)

print(f"🎯 Topic saved: {topic}")

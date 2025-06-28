import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Simpele prompt aan ChatGPT voor trending topics
prompt = "Noem 5 actuele trending onderwerpen over AI tools, tech-hacks of automatisering, elk in 1 zin."

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100
)

topics = response.choices[0].text.strip().split('\n')
with open('data/trending_topics.json', 'w') as f:
    import json
    json.dump(topics, f, indent=2)

print("Trending topics opgeslagen!")

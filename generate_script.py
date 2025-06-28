import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

with open('data/trending_topics.json') as f:
    topics = json.load(f)

# Kies eerste onderwerp (of random)
topic = topics[0]

prompt = (
    f"Schrijf een YouTube short script (max 60 seconden, humoristisch, pakkende intro, afsluiten met call-to-action) "
    f"over: '{topic}'. Maak het clickbaity en interessant, maar op waarheid gebaseerd."
)

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=300
)

script = response.choices[0].text.strip()
with open(f'data/scripts/{topic[:30]}.txt', 'w') as f:
    f.write(script)

print("Script gegenereerd!")

from transformers import pipeline
import json
import os
import random

generator = pipeline('text2text-generation', model='google/flan-t5-small')

with open('data/trending_topics.json') as f:
    topics = json.load(f)

topic = random.choice(topics)
print(f"Gekozen onderwerp: {topic}")

prompt = (
    f"Schrijf een virale YouTube short van max 60 seconden over: '{topic}'. "
    "Open met een sterke hook of verrassende vraag, gebruik clickbait-intro, humor en actuele feiten, "
    "bouw op naar een cliffhanger, en sluit af met een sterke call-to-action. "
    "Gebruik psychologisch bewezen technieken om mensen te laten blijven kijken. "
    "Wees feitelijk, maar maak het zo spannend mogelijk."
)

results = generator(prompt, max_length=300)
print("LLM output:", results)  # DEBUG

script = results[0]['generated_text']

script_file = f"data/scripts/{topic[:30].replace(' ', '_')}.txt"
with open(script_file, 'w') as f:
    f.write(script)

print(f"Script opgeslagen in {script_file}")

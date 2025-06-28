from transformers import pipeline
import json
import os

generator = pipeline('text-generation', model='google/flan-t5-small')

with open('data/trending_topics.json') as f:
    topics = json.load(f)

topic = topics[0]

prompt = (
    f"Schrijf een YouTube short script van max 60 seconden over: '{topic}'. "
    "Gebruik een pakkende clickbait-intro, humor, en sluit af met een call-to-action. "
    "Wees feitelijk, maar maak het zo spannend mogelijk."
)

results = generator(prompt, max_length=300)
script = results[0]['generated_text']

script_file = f'data/scripts/{topic[:30].replace(" ","_")}.txt'
with open(script_file, 'w') as f:
    f.write(script)

print(f"Script opgeslagen in {script_file}")

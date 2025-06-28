from transformers import pipeline
import json

generator = pipeline('text2text-generation', model='google/flan-t5-small')

prompt = (
    "Noem 5 trending onderwerpen over AI tools, tech-hacks of automatisering, in het Nederlands. Zet elk onderwerp op een aparte regel, alleen het onderwerp (dus geen nummering of extra uitleg)."
)

results = generator(prompt, max_length=100)
print("LLM output:", results)  # Debug

topics_raw = results[0]['generated_text']

# Splitsen op nieuwe regels, en lege regels eruit filteren
topics = [t.strip() for t in topics_raw.split('\n') if t.strip()]
print("Parsed topics:", topics)

# Indien minder dan 5, vul aan met dummy onderwerpen
while len(topics) < 5:
    topics.append(f"Onderwerp {len(topics)+1}")

with open('data/trending_topics.json', 'w') as f:
    json.dump(topics, f, indent=2)

print("Trending topics opgeslagen:", topics)

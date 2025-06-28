from transformers import pipeline
import json

# LLM voor onderwerpen genereren
generator = pipeline('text2text-generation', model='google/flan-t5-small')

prompt = "Noem 5 trending onderwerpen over AI tools, tech-hacks of automatisering, elk in 1 zin."

results = generator(prompt, max_length=100)
print("LLM output:", results)  # DEBUG

# Soms is de key 'generated_text', soms 'output'. Meestal 'generated_text' voor flan-t5-small.
topics_raw = results[0]['generated_text']
topics = topics_raw.split('\n')[1:6]  # Dit werkt als je model netjes per regel output geeft

with open('data/trending_topics.json', 'w') as f:
    json.dump(topics, f, indent=2)

print("Trending topics opgeslagen:", topics)

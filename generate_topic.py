from transformers import pipeline
import json

# LLM voor onderwerpen genereren
generator = pipeline('text-generation', model='meta-llama/Llama-2-7b-hf')

prompt = "Noem 5 trending onderwerpen over AI tools, tech-hacks of automatisering, elk in 1 zin."

results = generator(prompt, max_length=100)
topics = results[0]['generated_text'].split('\n')[1:6]

with open('data/trending_topics.json', 'w') as f:
    json.dump(topics, f, indent=2)

print("Trending topics opgeslagen:", topics)

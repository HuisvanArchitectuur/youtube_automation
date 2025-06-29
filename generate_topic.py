from transformers import pipeline
import json
from pytrends.request import TrendReq

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# Haal de top 5 trending onderwerpen van vandaag op via Google Trends NL
pytrends = TrendReq(hl='nl-NL', tz=360)
try:
    trends = pytrends.trending_searches(pn='netherlands')
except Exception as e:
    print(f"Trending topics niet beschikbaar (fout: {e}), gebruik fallback onderwerpen.")
    trends = None

if trends is not None:
    trending_list = trends[0].tolist()[:5]
else:
    trending_list = ["AI", "ChatGPT", "Google", "YouTube", "Automation"]
trending_list = trends[0].tolist()[:5]
print("Trending topics van Google Trends:", trending_list)

# LLM prompt, gebaseerd op echte trends
prompt = (
    f"Noem 5 trending onderwerpen gebaseerd op: {', '.join(trending_list)}. "
    "Zet elk onderwerp op een aparte regel, alleen het onderwerp (dus geen nummering of extra uitleg)."
)

results = generator(prompt, max_length=100)
print("LLM output:", results)  # Debug

topics_raw = results[0]['generated_text']

# Splitsen op nieuwe regels, lege regels eruit filteren
topics = [t.strip() for t in topics_raw.split('\n') if t.strip()]
print("Parsed topics:", topics)

# Indien minder dan 5, vul aan met dummy onderwerpen
while len(topics) < 5:
    topics.append(f"Onderwerp {len(topics)+1}")

with open('data/trending_topics.json', 'w') as f:
    json.dump(topics, f, indent=2)

print("Trending topics opgeslagen:", topics)

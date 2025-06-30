from transformers import pipeline
import json
import random
from pytrends.request import TrendReq
from datetime import datetime

# LLM pipeline
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Haal de top 5 trending onderwerpen op via Google Trends NL
pytrends = TrendReq(hl='nl-NL', tz=360)

try:
    trends_df = pytrends.trending_searches(pn='netherlands')
    trending_list = trends_df[0].tolist()[:5]
    print("📈 Trending topics van Google Trends:", trending_list)
except Exception as e:
    print(f"⚠️ Trending topics niet beschikbaar (fout: {e}), gebruik fallback onderwerpen.")
    trending_list = ["AI", "ChatGPT", "Ruimtevaart", "Bizarre feiten", "Natuurwonderen", "Grote uitvindingen", "Onsterfelijkheid", "Vergeten beschavingen"]

# Genereer 5 creatieve onderwerpen obv deze trends
prompt = (
    f"Noem 5 unieke, pakkende YouTube short onderwerpen gebaseerd op: {', '.join(trending_list)}.\n"
    "Geef alleen het onderwerp per regel – dus geen uitleg, geen nummering. "
    "Stijl: creatief, informatief, met een haakje (hook), geschikt voor virale shorts."
)

results = generator(prompt, max_length=100)
print("🧠 LLM output:", results)

topics_raw = results[0]['generated_text']

# Splits op nieuwe regels, filter lege regels
topics = [t.strip() for t in topics_raw.split('\n') if t.strip()]
print("✅ Verwerkte topics:", topics)

# Indien minder dan 5, vul aan met dummy onderwerpen
while len(topics) < 5:
    topics.append(f"Onderwerp {len(topics)+1}")

# Sla volledige lijst op
with open("data/trending_topics.json", "w") as f:
    json.dump(topics, f, indent=2)

# Kies 1 random topic voor deze video
chosen_topic = random.choice(topics)

# Sla geselecteerde topic op voor downstream script
with open("data/topic.json", "w") as f:
    json.dump({"topic": chosen_topic, "generated_at": datetime.now().isoformat()}, f)

print(f"🎯 Gekozen onderwerp: {chosen_topic}")

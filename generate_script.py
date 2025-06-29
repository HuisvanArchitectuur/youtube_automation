from transformers import pipeline
import json
import os

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# Laad de trending topics
with open('data/trending_topics.json') as f:
    topics = json.load(f)

# ---- 1. Kies 5 onderwerpen (of minder als er minder zijn) ----
selected_topics = topics[:5]

print(f"Geselecteerde onderwerpen: {selected_topics}")

# ---- 2. Bouw één prompt voor 5 korte scenes ----
prompt = (
    f"Schrijf een virale YouTube short script van maximaal 60 seconden, bestaande uit 5 scenes, elk gebaseerd op één van deze onderwerpen: {', '.join(selected_topics)}. "
    "Voor elke scene: "
    "Open met een sterke hook of verrassende vraag, gebruik clickbait-intro, humor en actuele feiten, "
    "bouw op naar een cliffhanger, en sluit af met een sterke call-to-action. "
    "Gebruik psychologisch bewezen technieken om mensen te laten blijven kijken. "
    "Wees feitelijk, maar maak het zo spannend mogelijk. "
    "Zet elke scene op een aparte regel, alleen de tekst van de scene (geen nummering of uitleg)."
)

results = generator(prompt, max_length=350)
print("LLM output:", results)  # DEBUG

script_raw = results[0]['generated_text']

# ---- 3. Scenes opsplitsen per regel ----
scenes = [s.strip() for s in script_raw.split('\n') if s.strip()]

# ---- 4. Scriptbestand opslaan ----
script_file = f"data/scripts/{'_'.join([t[:10].replace(' ', '_') for t in selected_topics])}.txt"
with open(script_file, 'w') as f:
    for scene in scenes:
        f.write(scene + '\n')

print(f"Script opgeslagen in {script_file}")

from transformers import pipeline
import json
import os

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# Laad trending topics (zorg dat deze wetenschappelijk/factueel zijn)
with open('data/trending_topics.json') as f:
    topics = json.load(f)

# Kies max 5 onderwerpen
selected_topics = topics[:5]

print(f"Geselecteerde onderwerpen: {selected_topics}")

# Prompt met focus op wetenschappelijke/fact-based content
prompt = (
    f"Schrijf een virale, feitelijke YouTube short script van max 60 seconden, opgedeeld in 5 scènes, "
    f"elk gebaseerd op één van deze onderwerpen: {', '.join(selected_topics)}.\n"
    "Voor elke scène:\n"
    "- Begin met een verrassende hook of vraag (clickbait, spannend of actueel)\n"
    "- Verwerk recente feiten of wetenschappelijke inzichten (vermeld jaartal/bron als je die weet)\n"
    "- Voeg humor toe, bouw op naar een cliffhanger\n"
    "- Eindig met een krachtige call-to-action\n"
    "- Gebruik psychologisch bewezen technieken om kijkers te boeien\n"
    "- Wees feitelijk en vermeld geen dingen die je niet zeker weet; als iets onbekend is, wees transparant\n"
    "Zet elke scène op een aparte regel, zonder nummering of extra uitleg. Houd het begrijpelijk voor jongeren. "
    "Maak het inspirerend, kort en super engaging. Schrijf alleen de tekst van de scène, geen introducties of afsluitingen."
)

results = generator(prompt, max_length=350)
print("LLM output:", results)  # DEBUG

script_raw = results[0]['generated_text']

# Split scenes (op nieuwe regel)
scenes = [s.strip() for s in script_raw.split('\n') if s.strip()]

# Opslaan als scriptbestand
output_name = '_'.join([t[:10].replace(' ', '_') for t in selected_topics])
script_file = f"data/scripts/{output_name}.txt"
with open(script_file, 'w', encoding='utf-8') as f:
    for scene in scenes:
        f.write(scene + '\n')

print(f"[INFO] Script opgeslagen in {script_file}")

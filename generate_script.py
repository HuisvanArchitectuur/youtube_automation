from transformers import pipeline 
import json
import os

generator = pipeline('text2text-generation', model='google/flan-t5-small')

# 1. Laad trending topics
with open('data/trending_topics.json') as f:
    topics = json.load(f)

selected_topics = topics[:5]
print(f"Geselecteerde onderwerpen: {selected_topics}")

# 2. **Super duidelijke prompt voor dia-per-dia voiceover**
prompt = (
    f"Schrijf een virale, feitelijke YouTube short script van max 60 seconden, verdeeld in 5 losse scènes,"
    f" elk gebaseerd op één van deze onderwerpen: {', '.join(selected_topics)}.\n"
    "Voor elke scène: schrijf 1 krachtige, zelfstandige, directe zin die door de voice-over wordt uitgesproken."
    " Gebruik een verrassende hook, recente feiten of wetenschappelijke inzichten (vermeld jaar/bron als bekend), humor, cliffhanger, of call-to-action."
    " Gebruik psychologische technieken om kijkers vast te houden. Vermijd herhaling, wees concreet en geloofwaardig, overdrijf niet."
    " Geen nummering, geen uitleg, geen verwijzingen naar afbeeldingen of foto's."
    " Schrijf elke scène op een nieuwe regel. Alleen de tekst die de voice-over moet zeggen."
)

results = generator(prompt, max_length=350)
print("LLM output:", results)  # DEBUG

script_raw = results[0]['generated_text']

# 3. **Split scenes exact per regel**
scenes = [s.strip() for s in script_raw.split('\n') if s.strip()]

# 4. **Opslaan als scriptbestand**
output_name = '_'.join([t[:10].replace(' ', '_') for t in selected_topics])
script_file = f"data/scripts/{output_name}.txt"
with open(script_file, 'w', encoding='utf-8') as f:
    for scene in scenes:
        f.write(scene + '\n')

print(f"[INFO] Script opgeslagen in {script_file}")

# ==== FACTCHECK STAP (optioneel, kan je aan/uit zetten) ====
fact_checker = pipeline('text2text-generation', model='google/flan-t5-small')

with open(script_file, 'r', encoding='utf-8') as f:
    script_content = f.read()

factcheck_prompt = (
    "Hier is een YouTube short script, gesplitst in scenes:\n"
    f"{script_content}\n"
    "Voor elke scene: "
    "1. Zijn de genoemde feiten recent en waarheidsgetrouw? (ja/nee) "
    "2. Vermeld twijfel, overdrijving of fictie. "
    "3. Suggesties voor feitelijke verbetering?"
    " Zet het antwoord per scene op een nieuwe regel."
)

factcheck_results = fact_checker(factcheck_prompt, max_length=300)
factcheck_output = factcheck_results[0]['generated_text']

factcheck_file = script_file.replace('.txt', '_factcheck.txt')
with open(factcheck_file, 'w', encoding='utf-8') as f:
    f.write(factcheck_output)

print(f"[INFO] Factcheck output opgeslagen in {factcheck_file}")

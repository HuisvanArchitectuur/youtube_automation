import os

# Overzicht van je mappenstructuur
folders = [
    "data/scripts",
    "data/voiceovers",
    "data/videos",
    "data/thumbnails"
]

# Maak de mappen aan en zet een .gitkeep erin
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    gitkeep_path = os.path.join(folder, ".gitkeep")
    with open(gitkeep_path, "w") as f:
        pass  # Leeg bestand, puur om map zichtbaar te houden in git

# trending_topics.json leeg initialiseren als hij nog niet bestaat
topics_json = "data/trending_topics.json"
if not os.path.exists(topics_json):
    with open(topics_json, "w") as f:
        f.write("[]")

print("✅ Alle data-mappen en .gitkeep-bestanden zijn aangemaakt!")

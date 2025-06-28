import os

# Overzicht van je mappenstructuur
folders = [
    "data/scripts",
    "data/voiceovers",
    "data/videos",
    "data/thumbnails"
]

def debug_folder(path):
    print(f"\n🟦 Inhoud van {path}:")
    if os.path.exists(path):
        if os.path.isdir(path):
            for entry in os.listdir(path):
                print("   ", entry)
        else:
            print(f"   LET OP: {path} bestaat al als BESTAND, niet als map!")
    else:
        print("   Bestaat niet.")

# Debug: toon inhoud van data/ voordat je iets aanmaakt
debug_folder("data")

# Maak de mappen aan en zet een .gitkeep erin
for folder in folders:
    try:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Map aangemaakt of al aanwezig: {folder}")
    except Exception as e:
        print(f"❌ FOUT bij aanmaken van {folder}: {e}")
    gitkeep_path = os.path.join(folder, ".gitkeep")
    with open(gitkeep_path, "w") as f:
        pass  # Leeg bestand, puur om map zichtbaar te houden in git
    # Debug: check na iedere map
    debug_folder(folder)

# trending_topics.json leeg initialiseren als hij nog niet bestaat
topics_json = "data/trending_topics.json"
if not os.path.exists(topics_json):
    with open(topics_json, "w") as f:
        f.write("[]")

print("\n✅ Alle data-mappen en .gitkeep-bestanden zijn aangemaakt!")
debug_folder("data")

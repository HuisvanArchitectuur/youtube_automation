import requests
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
script_path = "data/scripts/..."  # kies meest recente script
voiceover_path = "data/voiceovers/..."  # geef outputnaam

with open(script_path, 'r') as f:
    text = f.read()

url = "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID"  # vervang VOICE_ID met je gewenste stem
headers = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}
data = {
    "text": text,
    "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
}
response = requests.post(url, headers=headers, json=data)
with open(voiceover_path, "wb") as f:
    f.write(response.content)

print("Voice-over gegenereerd!")

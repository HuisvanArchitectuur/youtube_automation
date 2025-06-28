import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

with open('data/trending_topics.json') as f:
    topics = json.load(f)

topic = topics[0]

headers = {
    "Authorization": PEXELS_API_KEY
}

url = f"https://api.pexels.com/v1/search?query={topic}&per_page=1"
response = requests.get(url, headers=headers)
data = response.json()

image_url = data['photos'][0]['src']['large']
img_data = requests.get(image_url).content

visual_path = f"data/videos/visual.jpg"
with open(visual_path, 'wb') as handler:
    handler.write(img_data)

print(f"Visual opgeslagen als {visual_path}")

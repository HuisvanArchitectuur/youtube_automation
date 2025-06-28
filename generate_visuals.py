import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = "AI visualisatie van het onderwerp: ..."  # Zelfde als topic, eventueel script samenvatten

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
)
image_url = response['data'][0]['url']
# Download plaatje
import requests
img_data = requests.get(image_url).content
with open('data/videos/visual.png', 'wb') as handler:
    handler.write(img_data)

print("Visual gemaakt!")

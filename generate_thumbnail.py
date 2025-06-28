import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
prompt = "Felle clickbait thumbnail voor het onderwerp: ..."  # Vul titel of topic in

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1280x720"
)
image_url = response['data'][0]['url']
import requests
img_data = requests.get(image_url).content
with open('data/thumbnails/thumb.png', 'wb') as handler:
    handler.write(img_data)

print("Thumbnail gegenereerd!")

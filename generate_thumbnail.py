from PIL import Image, ImageDraw, ImageFont
import os

visual_path = 'data/videos/visual.jpg'
thumbnail_path = 'data/thumbnails/thumb.png'

image = Image.open(visual_path).convert("RGB")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 60)  # Zorg dat je Arial.ttf hebt, anders andere font gebruiken.

text = "KIJK DIT!"  # Maak dynamisch op basis van je onderwerp of video titel

width, height = image.size
textwidth, textheight = draw.textsize(text, font=font)
x = (width - textwidth) // 2
y = height - textheight - 20

draw.rectangle([(x-20, y-20), (x+textwidth+20, y+textheight+20)], fill="yellow")
draw.text((x, y), text, font=font, fill="black")
image.save(thumbnail_path)

print(f"Thumbnail opgeslagen als {thumbnail_path}")

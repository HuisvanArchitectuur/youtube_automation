from PIL import Image, ImageDraw, ImageFont
import os

visual_path = 'data/videos/visual.jpg'
thumbnail_path = 'data/thumbnails/thumb.png'

image = Image.open(visual_path).convert("RGB")
draw = ImageDraw.Draw(image)

# Gebruik een standaard Arial font, of verander pad als je iets anders wilt
try:
    font = ImageFont.truetype("arial.ttf", 60)
except OSError:
    font = ImageFont.load_default()

text = "KIJK DIT!"  # Maak dynamisch indien gewenst

# Gebruik textbbox om textgrootte te bepalen
bbox = draw.textbbox((0, 0), text, font=font)
textwidth = bbox[2] - bbox[0]
textheight = bbox[3] - bbox[1]
width, height = image.size
x = (width - textwidth) // 2
y = height - textheight - 20

draw.rectangle(
    [(x-20, y-20), (x+textwidth+20, y+textheight+20)],
    fill="yellow"
)
draw.text((x, y), text, font=font, fill="black")

image.save(thumbnail_path)
print(f"Thumbnail opgeslagen als {thumbnail_path}")

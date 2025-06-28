from PIL import Image, ImageDraw, ImageFont
import os

visual_path = 'data/videos/visual.jpg'
thumbnail_path = 'data/thumbnails/thumb.png'

# Open afbeelding en converteer naar RGB
image = Image.open(visual_path).convert("RGB")
draw = ImageDraw.Draw(image)

# Gebruik Arial als mogelijk, anders fallback naar DejaVuSans of default font
try:
    font = ImageFont.truetype("arial.ttf", 60)
except OSError:
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 60)
    except OSError:
        font = ImageFont.load_default()

text = "KIJK DIT!"  # Maak dynamisch op basis van je onderwerp of video titel

width, height = image.size
textwidth, textheight = draw.textsize(text, font=font)
x = (width - textwidth) // 2
y = height - textheight - 20

# Gele rechthoek achter de tekst voor betere zichtbaarheid
draw.rectangle(
    [(x-20, y-20), (x+textwidth+20, y+textheight+20)],
    fill="yellow"
)
draw.text((x, y), text, font=font, fill="black")

image.save(thumbnail_path)

print(f"✅ Thumbnail opgeslagen als {thumbnail_path}")

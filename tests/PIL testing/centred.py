from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

img = Image.new("RGB", (1024, 720), "black")
def text(text, color, position):
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 100)
    draw.text((text_x, text_y), str(text), font=myFont, fill=color, anchor="mm")
    img.putpixel((text_x, text_y), (255,0,0))
text_x = int((img.width) / 3)
text_y = int((img.height) / 3)
text(text=124, color=(255,255,255), position=(text_x, text_y))
img.show()
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import random

def create_rounded_rectangle(image, size, corner_radius, color, position, scale_factor=3):
    width, height = size
    scaled_size = (width * scale_factor, height * scale_factor)
    scaled_radius = corner_radius * scale_factor

    # centre on position, rather than top left
    position = int(position[0] - width/2), int(position[1] - height/2)
    
    # Create a scaled-up image
    rectangle = Image.new('RGBA', scaled_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)
    
    # Draw the rounded rectangle on the scaled image
    draw.rounded_rectangle(
        [(0, 0), scaled_size],
        radius=scaled_radius,
        fill=color
    )
    
    # Downscale the image to the target size to apply anti-aliasing
    rounded_rectangle = rectangle.resize(size, Image.LANCZOS)
    image.paste(rounded_rectangle, position, rounded_rectangle)

def text(text, color, position, font_size):
    draw = ImageDraw.Draw(im)
    myFont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
    draw.text(position, str(text), font=myFont, fill=color, anchor="mm")
    position = tuple(map(int, position))
    im.putpixel(position, (255,0,0))



def text_aligned_right(image, text, font_size, color, position):
    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)

    # drawing text size 
    bbox = draw.textbbox((0,0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = position[0] - text_width
    y = position[1] - text_height/2

    draw.text((x,y), text, fill=color, font_size=font_size, font=font)

start = time.time()
im = Image.open("images/backgrounds/pacific.png")
im = im.filter(ImageFilter.GaussianBlur(radius=5.0))
width, height = im.size
end = time.time()
print(end-start)


def user_card(username: str):
    # Example usage:
    size = (1000, 200)
    middle_width = int((width - size[0])/2)
    corner_radius = 50
    color = (0, 0, 0, 150)
    position = (width/2, 125) #centers horizontally

    create_rounded_rectangle(im, size, corner_radius, color, position)

    text(username, (255,255,255), (width/2, position[1]-size[1] * 3/20), (size[1]/2.5))
    text("Last seen today", (200,200,200), (width/2, position[1]+size[1] * 9/40), (size[1]/5))

def level_card(level: int, percentage:int):
    size = (2000, 150)
    corner_radius = 75
    background_color = (0, 0, 0, 150)
    position = (width/2, 350) #centers horizontally

    create_rounded_rectangle(im, size, corner_radius, background_color, position)

    progress_bar_size = (int((size[0] * 31/40)), int(size[1]/3))
    progress_bar_position = (width/2, position[1])
    #progress bar background
    create_rounded_rectangle(im, progress_bar_size, corner_radius, (0,0,0), progress_bar_position)
    #progress bar foreground
    filled_bar_size = (849,int(size[1]/3))
    filled_bar_position = (width/2 - (progress_bar_size[0] - filled_bar_size[0])/2 - 1, progress_bar_position[1])
    create_rounded_rectangle(im, filled_bar_size, corner_radius, (255,255,255), filled_bar_position) # correct size

    #percentage
    text_aligned_right(im, "60%", (size[1]/3.3), (255,255,255), (filled_bar_position[0] + filled_bar_size[0]/2 - size[1] / 20 + 105, progress_bar_position[1] - size[1]/20 - 2)) 
    #current level
    text(str(level), (255,255,255), (width/2-850, progress_bar_position[1]), (size[1]/2))
    #next level
    text(str(level+1), (255,255,255), (width/2+850, progress_bar_position[1]), (size[1]/2))
    #Percentile
    #text("149,201 XP", (200,200,200), (width/2, position[1] - 50), (size[1]/5))
    #centred_text(im, "149,201 XP", (size[1]/5), (200,200,200), (width/2, position[1] - 65))
    #XP amount
    #text("Top 52%", (200,200,200), (width/2, position[1] + 50), (size[1]/6))
    #centred_text(im, "Top 52%", (size[1]/6), (200,200,200), (width/2, position[1] + 60))

def kill_card(kills):
    #background
    size = (600, 300)
    corner_radius = 50
    position = (int((width - size[0])/4), 630)
    create_rounded_rectangle(im, size, corner_radius, (0,0,0,150), position)

    # kill text
    text("Kills", (0,255,0), (position[0], position[1] - 90), 55)
    #centred_text(im, "Kills", 75, (0,255,0), (position[0], position[1] - size[1]/4))

    # kill count
    text(str(kills), (0,255,0), (position[0], position[1] + 10), 125)
    #centred_text(im, str(kills), 125, (0,255,0), (position[0], position[1] + size[1]/15))
    text("Top 5%", (200,200,200), (position[0], position[1] + 100), 50)

    im.putpixel(position, (255,0,0))


def death_card(deaths):
    #background
    size = (600, 300)
    corner_radius = 50
    position = (int(width/2), 630)
    create_rounded_rectangle(im, size, corner_radius, (0,0,0,150), position)

    # death text
    text("Kills", (255,0,0), (position[0], position[1] - 90), 55)
    #centred_text(im, "Kills", 75, (0,255,0), (position[0], position[1] - size[1]/4))

    # death count
    if str(deaths)[0] == 1:
        text(str(deaths), (255,0,0), (position[0] - 100, position[1] + 10), 125)
    else:
        text(str(deaths), (255,0,0), (position[0], position[1] + 10), 125)
    #centred_text(im, str(kills), 125, (0,255,0), (position[0], position[1] + size[1]/15))
    text("Top 5%", (200,200,200), (position[0], position[1] + 100), 50)

    im.putpixel(position, (255,0,0))

def kdr_card(kills):
    #background
    size = (600, 300)
    corner_radius = 50
    position = ((3 * width + size[0]) / 4, 630)
    create_rounded_rectangle(im, size, corner_radius, (0,0,0,150), position)


user_card(" EpicEfeathers")
level_card(15, 56)
kill_card(random.randint(1, 999))
death_card(100)
kdr_card(100)


#create_rounded_rectangle(im, (100, 40), 10, (255, 255, 255), position=(int(width/2),20))
im.show()
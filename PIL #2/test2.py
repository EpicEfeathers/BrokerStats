from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import random
import time
from fontTools.ttLib import TTCollection

OPACITY = 200
LEFT_TEXT = 1160
RIGHT_TEXT = 1880
RIGHT_Y_POSITION = 75
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"


# cards
SIZE = (500, 250)
TOP_Y_POSITION = 335
SPACING = int((1120 - (2*SIZE[0]))/3)
LEFT = SPACING + SIZE[1]
RIGHT = (1120 - SIZE[1]) - SPACING


def draw_text(text, color, position, font_size, index, anchor):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size, index=index)
    draw.text(position, str(text), font=font, fill=color,anchor=anchor)

def text_bold(text, color, position, font_size, anchor):
    draw_text(text, color, position, font_size, 10, anchor=anchor)

def text(text, color, position, font_size, anchor):
    draw_text(text, color, position, font_size, 0, anchor=anchor)

def text_narrow(text, color, position, font_size, anchor):
    draw_text(text, color, position, font_size, 7, anchor=anchor)

def get_random_background():
    folder_path = "PIL #2/backgrounds"
    png_files = [file for file in os.listdir(folder_path)]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path)
    im = im.filter(ImageFilter.GaussianBlur(radius=5.0))

    return im

def logo(im):
    logo = Image.open("PIL #2/wb_logo.png")

    logo = logo.resize((150,134), Image.LANCZOS).convert("RGBA")

    im.paste(logo, (73,38), logo)

def create_right_background(im):
    shape = [(1120, 0), (1920, 1080)]
    size = shape[1][0] - shape[0][0], shape[1][1] - shape[0][1]
    print(size)
    
    # Create rectangle in 'RGBA' mode for transparency support
    rectangle = Image.new('RGBA', size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(rectangle)
    
    draw.rectangle([(0, 0), (800, 1080)], fill=(0, 0, 0, OPACITY))
    
    # Paste the rectangle onto the image with transparency
    im.paste(rectangle, (shape[0][0], shape[0][1]), rectangle)


def profile_pic(im):
    profile_pic = Image.open("PIL #2/profile_pic.png")

    profile_pic = profile_pic.resize((256,256), Image.LANCZOS).convert("RGBA")

    mask_size = (profile_pic.size[0]*4, profile_pic.size[1]*4)
    mask = Image.new("L", mask_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)

    mask = mask.resize(profile_pic.size, Image.LANCZOS)

    circular_img = Image.new("RGBA", profile_pic.size, (0, 0, 0, 0))
    circular_img.paste(profile_pic, (0,0), mask)

    im.paste(circular_img, (1392,RIGHT_Y_POSITION), circular_img)

def user_name(username:str, time_played:str):
    Y_POSITION = RIGHT_Y_POSITION + 300
    # username
    text_bold(text=username, color=(255,255,255), position=(1520,Y_POSITION), font_size=50, anchor="mm")
    # time played
    text_narrow(text=f"{time_played} hours", color=(255,255,255), position=(1520,Y_POSITION + 50), font_size=50, anchor="mm")


def damage_dealt(damage:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 430
    # description
    text_narrow(text="Damage Dealt:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # damage dealt
    text_bold(text=damage, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def kdr(kdr:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 560
    # description
    text_narrow(text="Kills / Death:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kdr
    text_bold(text=kdr, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def kpm(kpm:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 690
    # description
    text_narrow(text="Kills / Min:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kpm
    text_bold(text=kpm, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def level(level:str, percentage:str, xp:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 820
    # level
    text_bold(text=f"Level {level}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=55, anchor="lm")
    # percent to next level
    text_narrow(text=f"{percentage}% to next level", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 50), font_size=50, anchor="lm")
    # XP
    text_narrow(text=f"XP: {xp}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 100), font_size=50, anchor="lm")
    # percentile
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

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

def create_backgrounds():
    # row 1
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION))
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION))
    # row 2
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + SPACING + SIZE[1]))
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + SPACING + SIZE[1]))
    # row 3
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + 2*(SPACING + SIZE[1])))
    create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + 2*(SPACING + SIZE[1])))

def kill_card(kills:str, percentile:str):
    LEFT_POSITION = LEFT - (SIZE[0]/2) + 30
    text_narrow(text=f"Kills:", color=(255,255,255), position=(LEFT_POSITION, TOP_Y_POSITION - 60), font_size=55, anchor="lm")
    text_bold(text=kills, color=(255,255,255), position=(LEFT_POSITION, TOP_Y_POSITION), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(LEFT_POSITION, TOP_Y_POSITION + 60), font_size=40, anchor="lm")

def deaths_card(kills:str, percentile:str):
    RIGHT_POSITION = RIGHT - (SIZE[0]/2) + 30
    text_narrow(text=f"Deaths:", color=(255,255,255), position=(RIGHT_POSITION, TOP_Y_POSITION - 60), font_size=55, anchor="lm")
    text_bold(text=kills, color=(255,255,255), position=(RIGHT_POSITION, TOP_Y_POSITION), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_POSITION, TOP_Y_POSITION + 60), font_size=40, anchor="lm")

def classic_wins(wins:str, percentile:str):
    LEFT_POSITION = LEFT - (SIZE[0]/2) + 30
    text_narrow(text=f"Classic Wins:", color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1]) - 60), font_size=55, anchor="lm")
    text_bold(text=wins, color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1])), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1]) + 60), font_size=40, anchor="lm")

def br_wins(wins:str, percentile:str):
    RIGHT_POSITION = RIGHT - (SIZE[0]/2) + 30
    text_narrow(text=f"BR Wins:", color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1]) - 60), font_size=55, anchor="lm")
    text_bold(text=wins, color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1])), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + SPACING + SIZE[1]) + 60), font_size=40, anchor="lm")

def killsELO(elo:str, percentile:str):
    LEFT_POSITION = LEFT - (SIZE[0]/2) + 30
    text_narrow(text=f"Kills ELO:", color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1])) - 60), font_size=55, anchor="lm")
    text_bold(text=elo, color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1]))), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(LEFT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1])) + 60), font_size=40, anchor="lm")

def gamesELO(elo:str, percentile:str):
    RIGHT_POSITION = RIGHT - (SIZE[0]/2) + 30
    text_narrow(text=f"Games ELO:", color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1])) - 60), font_size=55, anchor="lm")
    text_bold(text=elo, color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1]))), font_size=55, anchor="lm")
    text_narrow(text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_POSITION, (TOP_Y_POSITION + 2*(SPACING + SIZE[1])) + 60), font_size=40, anchor="lm")


im = get_random_background()

logo(im)
create_right_background(im)
profile_pic(im)
user_name("EpicEfeathers", "35")

damage_dealt("140,032", "58")
kdr("1.40", "40")
kpm("1.8", "39")
level(level="23", percentage="48.5", xp="6,123", percentile="46")

create_backgrounds()
kill_card("2,450", "15.5")
deaths_card("2,450", "15.5")
classic_wins("105", "85")
br_wins("2", "90")
killsELO("1650", "31")
gamesELO("2014", "10")

im.show()
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import random
from fontTools.ttLib import TTCollection
import requests

# get values from main_stat_page
import functions

OPACITY = functions.OPACITY
LEFT_TEXT = functions.LEFT_TEXT
RIGHT_TEXT = functions.RIGHT_TEXT
RIGHT_Y_POSITION = functions.RIGHT_Y_POSITION
FONT_PATH = functions.FONT_PATH

def logo(im):
    profile_pic = Image.open("image_creation/wb_logo.png")

    profile_pic = profile_pic.resize((256,256), Image.LANCZOS).convert("RGBA")

    im.paste(profile_pic, (1392,75), profile_pic)

def lb_type(im):
    Y_POSITION = RIGHT_Y_POSITION + 300
    functions.text_bold(im, text="XP Leaderboard", color=(255,255,255), position=(1520,Y_POSITION), font_size=50, anchor="mm")

def create_background(im):
    SIZE = (1040, 80)
    POSITIONX = 40 + SIZE[0]/2
    positionY = 1080 - 40 - 10 - SIZE[1]/2

    RIGHT_X_POSITION = 1120 - 300

    for i in range(7):
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(POSITIONX, positionY))

        functions.text_bold(im, (10-i), (200,200,200), position=(40+20, positionY), font_size=50, anchor="lm")
        if i != 0:
            functions.text_bold(im, "EpicEfeathers", (255,255,255), position=(40+70, positionY), font_size=50, anchor="lm")
        else:
            functions.text_bold(im, "EpicEfeathers", (255,255,255), position=(40+98, positionY), font_size=50, anchor="lm")

        functions.text_bold(im, "2,001,400", (255,255,255), position=(RIGHT_X_POSITION, positionY), font_size=50, anchor="mm")

        positionY -= (SIZE[1] + 10)

    functions.text(im, "XP", (255,255,255), position=(RIGHT_X_POSITION, positionY), font_size=50, anchor="mt")




im = functions.get_random_background()
functions.create_right_background(im)
functions.bottom_bar(im)
logo(im)
lb_type(im)

create_background(im)

#response = requests.get("https://wbapi.wbpjs.com/players/ranking/xp?limit=10").json()
im.show()
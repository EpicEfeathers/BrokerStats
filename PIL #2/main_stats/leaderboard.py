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
    profile_pic = Image.open("PIL #2/wb_logo.png")

    profile_pic = profile_pic.resize((256,256), Image.LANCZOS).convert("RGBA")

    im.paste(profile_pic, (1392,75), profile_pic)

def lb_type(im):
    Y_POSITION = RIGHT_Y_POSITION + 300
    functions.text_bold(im, text="XP Leaderboard", color=(255,255,255), position=(1520,Y_POSITION), font_size=50, anchor="mm")

def create_background():
    pass







im = functions.get_random_background()
functions.create_right_background(im)
logo(im)
lb_type(im)

#response = requests.get("https://wbapi.wbpjs.com/players/ranking/xp?limit=10").json()
im.show()
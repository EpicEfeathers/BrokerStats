from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import random
from fontTools.ttLib import TTCollection

import functions

OPACITY = functions.OPACITY
LEFT_TEXT = functions.LEFT_TEXT
RIGHT_TEXT = functions.RIGHT_TEXT
RIGHT_Y_POSITION = functions.RIGHT_Y_POSITION
FONT_PATH = functions.FONT_PATH

# cards
SIZE = (500, 250)
TOP_Y_POSITION = 295
SPACING = int((1120 - (2*SIZE[0]))/3)
LEFT = SPACING + SIZE[1]
RIGHT = (1120 - SIZE[1]) - SPACING


def logo(im):
    logo = Image.open("PIL #2/wb_logo.png")

    logo = logo.resize((150,134), Image.LANCZOS).convert("RGBA")

    im.paste(logo, (73,18), logo)


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

def user_name(im, username:str, time_played:str):
    Y_POSITION = RIGHT_Y_POSITION + 300
    # username
    functions.text_bold(im, text=username, color=(255,255,255), position=(1520,Y_POSITION), font_size=50, anchor="mm")
    # time played
    functions.text_narrow(im, text=f"{time_played} hours", color=(255,255,255), position=(1520,Y_POSITION + 50), font_size=50, anchor="mm")


def damage_dealt(im, damage:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 430
    # description
    functions.text_narrow(im, text="Damage Dealt:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # damage dealt
    functions.text_bold(im, text=damage, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def kdr(im, kdr:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 560
    # description
    functions.text_narrow(im, text="Kills / Death:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kdr
    functions.text_bold(im, text=kdr, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def kpm(im, kpm:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 690
    # description
    functions.text_narrow(im, text="Kills / Min:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kpm
    functions.text_bold(im, text=kpm, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def level(im, level:str, percentage:str, xp:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 820
    # level
    functions.text_bold(im, text=f"Level {level}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=55, anchor="lm")
    # percent to next level
    functions.text_narrow(im, text=f"{percentage}% to next level", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 50), font_size=50, anchor="lm")
    # XP
    functions.text_narrow(im, text=f"XP: {xp}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 100), font_size=50, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=40, anchor="rm")

def create_backgrounds(im):
    # row 1
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION))
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION))
    # row 2
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + SPACING + SIZE[1]))
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + SPACING + SIZE[1]))
    # row 3
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + 2*(SPACING + SIZE[1])))
    functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + 2*(SPACING + SIZE[1])))

def create_card(im, info:str, percentile:str, category:str, column:int, row:int):
    if column == 0:
        x_pos = LEFT - (SIZE[0]/2) + 30
    else:
        x_pos = RIGHT - (SIZE[0]/2) + 30

    y_pos = (TOP_Y_POSITION + row*(SPACING + SIZE[1]))

    functions.text_narrow(im, text=f"{category}:", color=(255,255,255), position=(x_pos, y_pos - 60), font_size=55, anchor="lm")
    functions.text_bold(im, text=info, color=(255,255,255), position=(x_pos, y_pos), font_size=55, anchor="lm")
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(x_pos, y_pos + 60), font_size=40, anchor="lm")


def kill_card(im, kills:str, percentile:str):
    create_card(im, kills, percentile, "Kills", 0, 0)

def deaths_card(im, deaths:str, percentile:str):
    create_card(im, deaths, percentile, "Deaths", 1, 0)

def classic_wins(im, wins:str, percentile:str):
    create_card(im, wins, percentile, "Classic Wins", 0, 1)

def br_wins(im, wins:str, percentile:str):
    create_card(im, wins, percentile, "BR Wins", 1, 1)

def killsELO(im, elo:str, percentile:str):
    create_card(im, elo, percentile, "Kills ELO", 0, 2)

def gamesELO(im, elo:str, percentile:str):
    create_card(im, elo, percentile, "Games ELO", 1, 2)

def create_stat_card():
    im = functions.get_random_background()

    logo(im)
    functions.create_right_background(im)
    functions.bottom_bar(im)
    profile_pic(im)
    user_name(im, "EpicEfeathers", "35")

    damage_dealt(im, "140,032", "58")
    kdr(im, "1.40", "40")
    kpm(im, "1.8", "39")
    level(im, level="23", percentage="48.5", xp="6,123", percentile="46")

    create_backgrounds(im)
    kill_card(im, "2,450", "15.5")
    deaths_card(im, "2,450", "15.5")
    classic_wins(im, "105", "85")
    br_wins(im, "2", "90")
    killsELO(im, "1650", "31")
    gamesELO(im, "2014", "10")

    im.show()

create_stat_card()
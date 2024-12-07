from PIL import Image, ImageDraw
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import functions

OPACITY = functions.OPACITY
LEFT_TEXT = functions.LEFT_TEXT
RIGHT_TEXT = functions.RIGHT_TEXT
RIGHT_Y_POSITION = functions.RIGHT_Y_POSITION
FONT_PATH = functions.FONT_PATH

# cards
SIZE = (500, 250)
TOP_Y_POSITION = 335 #295
SPACING = int((1120 - (2*SIZE[0]))/3)
LEFT = SPACING + SIZE[1]
RIGHT = (1120 - SIZE[1]) - SPACING
LOGO_SIZE = (150,134)
PROFILE_PIC_SIZE = (256, 256)


def logo(im):
    logo = Image.open("image_creation/wb_logo.png")

    logo = logo.resize(LOGO_SIZE, Image.LANCZOS).convert("RGBA")

    im.paste(logo, (73,36), logo)

    functions.text_bold(im=im, text="Squad Stats", color=(255, 255, 255), position=(250, 103), font_size=75, anchor="lm")


def profile_pic(im, profile_picture, wb_logo:bool):
    if wb_logo:
        profile_picture = functions.resize_logo(profile_picture)
    else:
        profile_picture = profile_picture.resize(PROFILE_PIC_SIZE, Image.LANCZOS).convert("RGBA")

    mask_size = (profile_picture.size[0]*4, profile_picture.size[1]*4)
    mask = Image.new("L", mask_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)

    mask = mask.resize(profile_picture.size, Image.LANCZOS)

    circular_img = Image.new("RGBA", profile_picture.size, (0, 0, 0, 0))
    circular_img.paste(profile_picture, (0,0), mask)

    im.paste(circular_img, (1392,RIGHT_Y_POSITION), circular_img)

def squad_name(im, squad:str):
    Y_POSITION = RIGHT_Y_POSITION + 300
    # username
    color = (156,156,248)  
    functions.text_bold(im, text=squad, color=color, position=(1520,Y_POSITION), font_size=80, anchor="mm")

def squad_members(im, member_count:str, active_member_count:str):
    Y_POSITION = RIGHT_Y_POSITION + 400
    functions.text_narrow(im, text="Squad Members:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kdr
    functions.draw_member_text(im=im, text1=str(member_count), text2=f" ({str(active_member_count)} active last week)", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION+60), font_size=55, anchor="lm")

# all the kdr related text
def kdr(im, kdr:str, kills_needed:str, deaths_to_avoid:str):
    Y_POSITION = RIGHT_Y_POSITION + 534
    # description
    functions.text_narrow(im, text="Squad Kills / Death:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kdr
    functions.text_bold(im, text=kdr, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")



# all the kpm related text
def kpm(im, kpm:str):
    Y_POSITION = RIGHT_Y_POSITION + 667
    # description
    functions.text_narrow(im, text="Squad Kills / Min:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kpm
    functions.text_bold(im, text=kpm, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")

# all the level related text
def level(im, level:str, xp:str):
    Y_POSITION = RIGHT_Y_POSITION + 800
    # level
    functions.text_narrow(im, text="Avg Squad Level:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=50, anchor="lm")
    # kpm
    functions.text_bold(im, text=level, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 60), font_size=55, anchor="lm")
    # XP
    functions.text_narrow(im, text=f"Total XP: {xp}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 120), font_size=50, anchor="lm")

# creates the card backgrounds on the image
def create_backgrounds(im):
    for height in range(3):
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))

# the base function to create a card text on the image
def create_card(im, info:str, category:str, column:int, row:int):
    if column == 0:
        x_pos = LEFT - (SIZE[0]/2) + 30
    else:
        x_pos = RIGHT - (SIZE[0]/2) + 30
    y_pos = TOP_Y_POSITION + row*(SPACING + SIZE[1])

    functions.text_narrow(im, text=f"{category}:", color=(255,255,255), position=(x_pos, y_pos - 30), font_size=55, anchor="lm")
    functions.text_bold(im, text=info, color=(255,255,255), position=(x_pos, y_pos+30), font_size=55, anchor="lm")

def kill_card(im, kills:str):
    create_card(im, kills, "Total Kills", 0, 0)

def deaths_card(im, deaths:str):
    create_card(im, deaths, "Total Deaths", 1, 0)

def classic_wins(im, wins:str):
    create_card(im, wins, "Total Classic Wins", 0, 1)

def br_wins(im, wins:str):
    create_card(im, wins, "Total BR Wins", 1, 1)

def killsELO(im, elo:str):
    create_card(im, elo, "Avg Kills ELO", 0, 2)

def gamesELO(im, elo:str):
    create_card(im, elo, "Avg Games ELO", 1, 2)


def create_stat_card(stats: dict, profile_image):
    im = functions.get_random_background()


    logo(im)
    functions.create_right_background(im)
    functions.bottom_bar(im)
    if profile_image:
        profile_pic(im, Image.open("image_creation/profile_pic.png"), False)
    else:
        profile_pic(im, Image.open("image_creation/wb_logo.png"), True)

    squad_name(im, stats['squad'])

    kills_needed, deaths_to_avoid = functions.calculate_kdr_changes(int(stats['kills']), int(stats['deaths']))
    squad_members(im, stats["member_count"], stats["active_players"])
    kdr(im, str(round(float(stats['kdr']), 1)), kills_needed, deaths_to_avoid)
    kpm(im, str(round(float(stats['kpm']), 1)))
    level(im, stats['level'], xp=functions.format_large_number(stats['xp']))

    create_backgrounds(im)
    kill_card(im, functions.format_large_number(stats['kills']))
    deaths_card(im, functions.format_large_number(stats['deaths']))
    classic_wins(im, functions.format_large_number(stats['classic wins']))
    br_wins(im, functions.format_large_number(stats['br wins']))
    killsELO(im, stats['kills_elo'])
    gamesELO(im, stats["games_elo"])


    return im
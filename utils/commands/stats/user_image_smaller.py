from PIL import Image, ImageDraw, ImageFilter
import functions
import os
import random

OPACITY = 200
LEFT_TEXT = 870
RIGHT_TEXT = 1410
RIGHT_Y_POSITION = 56
FONT_PATH = "HelveticaNeue.ttc"

# cards
SIZE = (375, 188)
TOP_Y_POSITION = 251 #295
SPACING = int((840 - (2*SIZE[0]))/3)
LEFT = SPACING + SIZE[1]
RIGHT = (840 - SIZE[1]) - SPACING
LOGO_SIZE = (113,101)
PROFILE_PIC_SIZE = (192, 192)

def get_random_background():
    folder_path = "utils/commands/stats"
    png_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path)
    #im = im.filter(ImageFilter.GaussianBlur(radius=5.0))
    
    return im

def create_right_background(im):
    shape = [(840, 0), (1440, 810)]
    size = shape[1][0] - shape[0][0], shape[1][1] - shape[0][1]
    
    # Create rectangle in 'RGBA' mode for transparency support
    rectangle = Image.new('RGBA', size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(rectangle)
    
    draw.rectangle([(0, 0), (600, 810)], fill=(0, 0, 0, OPACITY))
    
    # Paste the rectangle onto the image with transparency
    im.paste(rectangle, (shape[0][0], shape[0][1]), rectangle)

def resize_logo(im):
    profile_pic = im.resize((169,169), Image.LANCZOS).convert("RGBA")
    #profile_pic = im.resize((225,225), Image.LANCZOS).convert("RGBA")

    new_size = (192, 192)
    #new_size = (256, 256)
    background = Image.new('RGBA', new_size, (0, 0, 0, 0))

    #centers old image on new image
    x = (new_size[0] - profile_pic.size[0]) // 2
    y = (new_size[1] - profile_pic.size[1]) // 2

    background.paste(profile_pic, (x, y))

    return background

def logo(im):
    logo = Image.open("image_creation/wb_logo.png")

    logo = logo.resize(LOGO_SIZE, Image.LANCZOS).convert("RGBA")

    im.paste(logo, (55,27), logo)

    functions.text_bold(im=im, text="User Stats", color=(255, 255, 255), position=(188, 77), font_size=56, anchor="lm")


def profile_pic(im, profile_picture, wb_logo:bool):
    if wb_logo:
        profile_picture = resize_logo(profile_picture)
    else:
        profile_picture = profile_picture.resize(PROFILE_PIC_SIZE, Image.LANCZOS).convert("RGBA")

    mask_size = (profile_picture.size[0]*4, profile_picture.size[1]*4)
    mask = Image.new("L", mask_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, mask_size[0], mask_size[1]), fill=255)

    mask = mask.resize(profile_picture.size, Image.LANCZOS)

    circular_img = Image.new("RGBA", profile_picture.size, (0, 0, 0, 0))
    circular_img.paste(profile_picture, (0,0), mask)

    im.paste(circular_img, (1044,RIGHT_Y_POSITION), circular_img)

def user_name(im, squad:str, username:str, time_played:str, steam:bool):
    Y_POSITION = RIGHT_Y_POSITION + 225
    # username
    if steam:
        color = (245,179,62)
    else:
        color=(255,255,255)
    functions.draw_colored_text(im=im, text1=squad, text2=f" {username}", color1=(156,156,248), color2=color, position=(1140, Y_POSITION), font_size=38, index=10, anchor="mm")
    # time played
    functions.text_narrow(im, text=f"{time_played}", color=(255,255,255), position=(1140,Y_POSITION + 38), font_size=38, anchor="mm")

# all the kdr related text
def kdr(im, kdr:str, percentile:str, kills_needed:str, deaths_to_avoid:str):
    Y_POSITION = RIGHT_Y_POSITION + 323
    # description
    #functions.text_narrow(im, text="Kills / Death:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")
    # kdr
    functions.text_bold(im, text=kdr, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 45), font_size=41, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=30, anchor="rm")

    # kd calculations
    functions.text_narrow(im, text=f"{kills_needed} kills to advance", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 90), font_size=38, anchor="lm")
    functions.text_narrow(im, text=f"{deaths_to_avoid} kills to avoid", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 128), font_size=38, anchor="lm")

# all the kpm related text
def kpm(im, kpm:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 509
    # description
    #functions.text_narrow(im, text="Kills / Min:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")
    # kpm
    functions.text_bold(im, text=kpm, color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 45), font_size=41, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=30, anchor="rm")

# all the level related text
def level(im, level:str, percentage:str, xp:str, percentile:str):
    Y_POSITION = RIGHT_Y_POSITION + 615
    # level
    functions.text_bold(im, text=f"Level {level}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=41, anchor="lm")
    # percent to next level
    functions.text_narrow(im, text=f"{percentage} to next level", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 38), font_size=38, anchor="lm")
    # XP
    functions.text_narrow(im, text=f"XP: {xp}", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION + 75), font_size=38, anchor="lm")
    # percentile
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(RIGHT_TEXT,Y_POSITION), font_size=30, anchor="rm")

# creates the card backgrounds on the image
def create_backgrounds(im):
    for height in range(3):
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=10, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))

# the base function to create a card text on the image
def create_card(im, info:str, percentile:str, category:str, column:int, row:int):
    if column == 0:
        x_pos = LEFT - (SIZE[0]/2) + 23
    else:
        x_pos = RIGHT - (SIZE[0]/2) + 23

    y_pos = TOP_Y_POSITION + row*(SPACING + SIZE[1])

    #functions.text_narrow(im, text=f"{category}:", color=(255,255,255), position=(x_pos, y_pos - 45), font_size=41, anchor="lm")
    functions.text_bold(im, text=info, color=(255,255,255), position=(x_pos, y_pos), font_size=41, anchor="lm")
    functions.text_narrow(im, text=f"Top {percentile}%", color=(255,255,255), position=(x_pos, y_pos + 45), font_size=30, anchor="lm")

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


def create_stat_card(stats: dict, profile_image):
    im = get_random_background()


    '''logo(im)
    create_right_background(im)
    if profile_image:
        profile_pic(im, Image.open("image_creation/profile_pic.png"), False)
    else:
        profile_pic(im, Image.open("image_creation/wb_logo.png"), True)'''

    steam = stats.get('steam', False)
    user_name(im, stats['squad'], stats["nick"], functions.time_since_last_seen(stats['time']), steam)

    kills_needed, deaths_to_avoid = functions.calculate_kdr_changes(int(stats['kills'].replace(",","")), int(stats['deaths'].replace(",","")))
    kdr(im, str(round(float(stats['kills / death']), 1)), "??", kills_needed, deaths_to_avoid)
    kpm(im, str(round(float(stats['kills / min']), 1)), "??")
    level(im, stats['level'], percentage=stats['progressPercentage'], xp=functions.format_large_number(stats['xp']), percentile=stats["xpPercentile"])

    #create_backgrounds(im)
    kill_card(im, stats['kills'], "??")
    deaths_card(im, stats['deaths'], "??")
    classic_wins(im, stats['classic mode wins'], "??")
    br_wins(im, stats['battle royale wins'], "??")
    killsELO(im, stats['killsELO'], stats["killsEloPercentile"])
    gamesELO(im, stats["gamesELO"], stats["gamesEloPercentile"])

    print(stats)

    return im
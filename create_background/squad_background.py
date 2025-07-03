from PIL import Image, ImageDraw, ImageFilter
import os

import background_functions

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
LOGO_SIZE = (85,85)
PROFILE_PIC_SIZE = (192, 192)

def get_background(path, blur:bool):
    im = Image.open(path)
    im = im.resize((1440, 810), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(radius=5.0))
    
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
    logo = Image.open("create_background/images/wb_logo.png")

    logo = logo.resize(LOGO_SIZE, Image.LANCZOS).convert("RGBA")

    background_functions.create_rounded_rectangle(image=im, size=(780,100), corner_radius=25, color=(0,0,0,OPACITY), position=(420, 79))
    im.paste(logo, (55, int(79 - LOGO_SIZE[1]/2) + 2), logo)
    background_functions.text_bold(im=im, text="Squad Overview", color=(255, 255, 255), position=(LEFT - (SIZE[0]/2) + 125, 77), font_size=45, anchor="lm")


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

# Squad Members
def squad_members(im):
    Y_POSITION = RIGHT_Y_POSITION + 300
    background_functions.text_narrow(im, text="Squad Members:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=39, anchor="lm")


# all the kdr related text
def kdr(im):
    Y_POSITION = RIGHT_Y_POSITION + 401
    background_functions.text_narrow(im, text="Squad Kills / Death:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")
# coin title
def coins(im):
    Y_POSITION = RIGHT_Y_POSITION + 500
    background_functions.text_narrow(im, text="Total Coings:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")

# all the kpm related text
'''def kpm(im):
    Y_POSITION = RIGHT_Y_POSITION + 500
    background_functions.text_narrow(im, text="Squad Kills / Min:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")'''

def level(im):
    Y_POSITION = RIGHT_Y_POSITION + 600
    background_functions.text_narrow(im, text="Avg Squad Level:", color=(255,255,255), position=(LEFT_TEXT,Y_POSITION), font_size=38, anchor="lm")

# creates the card backgrounds on the image
def create_backgrounds(im):
    for height in range(3):
        #old radius 10
        background_functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=25, color=(0,0,0,OPACITY), position=(LEFT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))
        background_functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=25, color=(0,0,0,OPACITY), position=(RIGHT,TOP_Y_POSITION + height*(SPACING+SIZE[1])))

# the base function to create a card text on the image
def create_card(im, category:str, column:int, row:int):
    if column == 0:
        x_pos = LEFT - (SIZE[0]/2) + 23
    else:
        x_pos = RIGHT - (SIZE[0]/2) + 23

    y_pos = TOP_Y_POSITION + row*(SPACING + SIZE[1])

    background_functions.text_narrow(im, text=f"{category}:", color=(255,255,255), position=(x_pos, y_pos - 25), font_size=41, anchor="lm")

def kill_card(im):
    create_card(im, "Total Kills", 0, 0)

def deaths_card(im):
    create_card(im, "Total Deaths", 1, 0)

def classic_wins(im):
    create_card(im, "Total Classic Wins", 0, 1)

def br_wins(im):
    create_card(im, "Total BR Wins", 1, 1)

def killsELO(im):
    create_card(im, "Avg Kills ELO", 0, 2)

def gamesELO(im):
    create_card(im, "Avg Games ELO", 1, 2)


def create_stat_card(file_path, file_name):
    im = get_background(file_path, True)

    logo(im)
    create_right_background(im)

    profile_pic(im, Image.open("create_background/images/wb_logo.png"), True)

    squad_members(im)
    kdr(im)
    coins(im)
    #kpm(im)
    level(im)

    create_backgrounds(im)
    kill_card(im)
    deaths_card(im)
    classic_wins(im)
    br_wins(im)
    killsELO(im)
    gamesELO(im)

    im.save(f"create_background/outputted_backgrounds/{file_name}")

folder_path = "create_background/backgrounds"
for filename in os.listdir(folder_path):
    if filename != ".DS_Store":
        file_path = os.path.join(folder_path, filename)
        create_stat_card(file_path, filename)
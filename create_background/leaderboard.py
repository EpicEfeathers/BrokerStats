from PIL import Image, ImageDraw, ImageFilter
import random

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import functions

OPACITY = 200
LEFT_TEXT = 870
RIGHT_TEXT = 1410
FONT_PATH = "HelveticaNeue.ttc"

IMAGE_SIZE = (600, 810)

# cards
SIZE = (508, 57) # (820, 57)
STEP = SIZE[1] + 5
PLACEMENT_SIZE = (62, 57)
#MIDDLE_CARD_POS = SIZE[0] / 2 + 10
TOP_Y_POSITION = SIZE[1]/2 + 180

def get_random_background(blur:bool):
    folder_path = "create_background/backgrounds"
    png_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path)
    im = im.resize(IMAGE_SIZE, Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(radius=5.0))
    
    return im

def title(im):
    Y_POSITION1 = 60
    functions.create_rounded_rectangle(image=im, size=(484, 80), corner_radius=25, color=(0,0,0,OPACITY), position=(IMAGE_SIZE[0]/2, Y_POSITION1))
    functions.text_bold(im=im, text="Lifetime Leaderboard", color=(255, 255, 255), position=(IMAGE_SIZE[0]/2, Y_POSITION1-2), font_size=45, anchor="mm")

    Y_POSITION2 = 135
    functions.create_rounded_rectangle(image=im, size=(270, 55), corner_radius=15, color=(0,0,0,OPACITY), position=(IMAGE_SIZE[0]/2, Y_POSITION2))
    #functions.text_bold(im=im, text="Tactical Shotgun", color=(255, 255, 255), position=(IMAGE_SIZE[0]/2, Y_POSITION2), font_size=32, anchor="mm")

    

# creates the card backgrounds on the image
def create_backgrounds(im):
    for height in range(10):
        functions.create_rounded_rectangle(image=im, size=SIZE, corner_radius=15, color=(0,0,0,OPACITY), position=(336,TOP_Y_POSITION + height*(STEP)))
        functions.create_rounded_rectangle(image=im, size=PLACEMENT_SIZE, corner_radius=15, color=(0,0,0,OPACITY), position=(41,TOP_Y_POSITION + height*(STEP)))
        #functions.text_bold(im, f"{height+11}", (200,200,200), (41, TOP_Y_POSITION + height*(STEP)), 36, "mm")
        #functions.text_narrow(im, "EpicEfeathers", (255,255,255), (100, TOP_Y_POSITION + height*(STEP)), 34, "lm")
        #functions.text(im, "120", (255,255,255), (IMAGE_SIZE[0]-30, TOP_Y_POSITION + height*(STEP)), 36, "rm")


def create_stat_card():
    im = get_random_background(True)
    
    create_backgrounds(im)
    title(im)

    im.show()

create_stat_card()
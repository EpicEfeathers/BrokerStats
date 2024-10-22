from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import random
from io import BytesIO
import discord
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta

OPACITY = 200
LEFT_TEXT = 1160
RIGHT_TEXT = 1880
RIGHT_Y_POSITION = 75
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"

def draw_text(im, text, color, position, font_size, index, anchor):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size, index=index)
    draw.text(position, str(text), font=font, fill=color,anchor=anchor)

def draw_colored_text(im, text1, text2, color1, color2, position, font_size, index, anchor):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size, index=index)
    
    # Calculate the total width of the combined text (text1 + text2)
    bbox_text1 = draw.textbbox((0, 0), text1, font=font)
    bbox_text2 = draw.textbbox((0, 0), text2, font=font)
    
    total_width = (bbox_text1[2] - bbox_text1[0]) + (bbox_text2[2] - bbox_text2[0])
    total_height = max(bbox_text1[3] - bbox_text1[1], bbox_text2[3] - bbox_text2[1])

    # Adjust position if anchor is "mm" (middle-middle)
    if anchor == "mm":
        # Center the text on the given position
        centered_position = (position[0] - total_width // 2, position[1] - total_height // 2)
    else:
        centered_position = position

    draw.text(centered_position, text1, font=font, fill=color1, anchor="lt")
    
    new_position = (centered_position[0] + (bbox_text1[2] - bbox_text1[0]), centered_position[1])
    draw.text(new_position, text2, font=font, fill=color2, anchor="lt")

def text_bold(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 10, anchor=anchor)

def text(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 0, anchor=anchor)

def text_narrow(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 7, anchor=anchor)

def get_random_background():
    folder_path = "image_creation/backgrounds"
    png_files = [file for file in os.listdir(folder_path)]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path)
    im = im.filter(ImageFilter.GaussianBlur(radius=5.0))

    return im

def create_right_background(im):
    shape = [(1120, 0), (1920, 1080)]
    size = shape[1][0] - shape[0][0], shape[1][1] - shape[0][1]
    
    # Create rectangle in 'RGBA' mode for transparency support
    rectangle = Image.new('RGBA', size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(rectangle)
    
    draw.rectangle([(0, 0), (800, 1080)], fill=(0, 0, 0, OPACITY))
    
    # Paste the rectangle onto the image with transparency
    im.paste(rectangle, (shape[0][0], shape[0][1]), rectangle)

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

def bottom_bar(im):
    '''shape = [(0, 1040), (1120, 1080)]
    size = shape[1][0] - shape[0][0], shape[1][1] - shape[0][1]
    
    # Create rectangle in 'RGBA' mode for transparency support
    rectangle = Image.new('RGBA', size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(rectangle)
    
    draw.rectangle([(0, 0), (1120, 40)], fill=(0, 0, 0, OPACITY))
    
    # Paste the rectangle onto the image with transparency
    im.paste(rectangle, (shape[0][0], shape[0][1]), rectangle)'''

    #text(im, "By EpicEfeathers", (255,255,255), (1900, 1060), 35, anchor="rm")
    pass

def calculate_kdr_changes(kills, deaths):
    kdr = kills/deaths
    rounded = round(kdr, 1)

    kills_needed = math.ceil(((rounded + 0.05) * deaths) - kills)

    deaths_avoid = math.floor((kills / (rounded - 0.05))) - deaths + 1

    return kills_needed, deaths_avoid

def time_since_last_seen(timestamp: int):
    now = datetime.now()
    last_played = datetime.fromtimestamp(timestamp)
    delta = relativedelta(now, last_played)

    if delta.years > 0:
        return f"Last seen {delta.years} year{'s' if delta.years > 1 else ''} ago"
    elif delta.months > 0:
        return f"Last seen {delta.months} month{'s' if delta.months > 1 else ''} ago"
    elif delta.days > 0:
        return f"Last seen {delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.hours > 0:
        return f"Last seen {delta.hours} hour{'s' if delta.hours > 1 else ''} ago"
    elif delta.minutes > 0:
        return f"Last seen {delta.minutes} minute{'s' if delta.minutes > 1 else ''} ago"
    else:
        return "Online now"


def convert_to_discord(im):
    with BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        
        return discord.File(fp=image_binary, filename='image.png')
    
def resize_logo(im):
    profile_pic = im.resize((225,225), Image.LANCZOS).convert("RGBA")

    new_size = (256, 256)
    background = Image.new('RGBA', new_size, (0, 0, 0, 0))

    #centers old image on new image
    x = (new_size[0] - profile_pic.size[0]) // 2
    y = (new_size[1] - profile_pic.size[1]) // 2

    background.paste(profile_pic, (x, y))

    return background

def format_large_number(number):
    return f"{number:,}"
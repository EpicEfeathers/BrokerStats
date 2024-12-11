from datetime import datetime, timezone
import math
import os
import random

from dateutil.relativedelta import relativedelta
from io import BytesIO

def calculate_kdr_changes(kills, deaths):
    """
    Calculated needs KILLS and DEATHS to next KDR change
    """
    kdr = kills/deaths
    rounded = round(kdr, 1)

    kills_needed = math.ceil(((rounded + 0.05) * deaths) - kills)

    deaths_avoid = math.floor((kills / (rounded - 0.05))) - deaths + 1

    return kills_needed, deaths_avoid

def convert_to_discord(surface):
    """Converts image to discord file"""
    image_stream = BytesIO()
    surface.write_to_png(image_stream)  # Write to the BytesIO object
    image_stream.seek(0)

    return image_stream

def format_large_number(number):
    return f"{number:,}"

def get_random_background(folder_path):
    """
    Chooses a random image (background)
    """
    png_files = [file for file in os.listdir(folder_path) if file.endswith('.png')]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)

    #im = Image.open("/Users/elingrell/Downloads/background1.png")

    return image_path

def uid_to_creation_date(uid):
    """Takes account UID and output account creation date"""    
    # The first 8 characters represent the timestamp
    timestamp = int(uid[:8], 16)

    # Convert the timestamp to a datetime object
    account_creation_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    formatted_date = account_creation_date.strftime("%m/%d/%Y")
    
    days_ago = (datetime.now(timezone.utc) - account_creation_date).days
    return f"{formatted_date} ({days_ago} days ago)"

def time_since_last_seen(timestamp: int):
    """
    Formats time since player was last online
    """
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
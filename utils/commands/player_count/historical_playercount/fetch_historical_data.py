import requests
import pandas as pd
import io
import time
from datetime import datetime

import matplotlib.pyplot as plt

FIRST_TIME = 1741129650

def half_hours_to_x_values(timestamps: list):
    """Formats half hour timestamps to number of hours ago"""
    current_half_hour = round((round(time.time()) - FIRST_TIME)/60/30) # get current half hour timestamp

    timestamps = timestamps[::4] # returns every fourth item (only want to display how many hours ago every two hours)
    for i, timestamp in enumerate(timestamps): # format :D
        timestamps[i] = f"{round((current_half_hour - timestamp)/2)} hours ago"

    if timestamps[-1] == "0 hours ago": # prettier formatting basically
        timestamps[-1] = "Now"

    return timestamps

def get_playercount(df, region, type):

    region_filter = {
        "Asia": r"(?i)As",
        "Europe": r"(?i)Eu",
        "NA": r"(?i)(?<!AS_|EU_)Dead_City|USA|NA"
    }

    if region.lower() == "worldwide": # if want to find total playercount
        playercount = df.drop(columns=['Timestamp']).tail(49).sum(axis=1).reset_index(drop=True) # Drop removes column 'Timestamp'. .sum(axis=1) sums the row. .reset_index resets the index (so x-values goes from 0-48). 49 values as want to include beginning & end
        title = region.capitalize()

    elif region in region_filter and type == "region": # if looking for a whole region's player count
        playercount = df.filter(regex=region_filter[region], axis=1).tail(49).sum(axis=1).reset_index(drop=True)
        title = region.capitalize()

    else: # if anything else
        servers = { 
            'Australia Battle Royale': 'AS_BATTLE_ROYALE',
            'Australia Dead City': 'AS_DEAD_CITY', 
            'Europe 4V4': 'EU_4V4', 
            'Europe Battle Royale': 'EU_BATTLE_ROYALE', 
            'Europe Dead City': 'EU_DEAD_CITY',
            'NA Dead City': 'DEAD_CITY'
        }

        region_name = servers.get(region, region.replace(" ", "_").upper())
        playercount = df[region_name].tail(49).reset_index(drop=True) # resets index (so x-values goes from 0-48). 49 values as want to include beginning & end

        if region in ['Asia', 'Australia', 'Europe', 'India', 'Japan', 'Russia', 'USA', 'USA_West']:
            title = f"{region.capitalize()} Classic"
        else:
            title = region.capitalize()

    return playercount, title


def get_data(region, type):
    """
    Fetches player count based on a specific region and server type (region or just specific server)
    """

    data = requests.get("https://raw.githubusercontent.com/EpicEfeathers/wb/main/data/playercount.csv").text

    df = pd.read_csv(io.StringIO(data)) # convert to pandas dataframe

    timestamps = list(df['Timestamp'].tail(49)) # get last 49 values. 49 values as want to include beginning & end
    timestamps = half_hours_to_x_values(timestamps)


    playercount, title = get_playercount(df, region, type)

    return playercount, timestamps, title
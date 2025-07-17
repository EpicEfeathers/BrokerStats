from bs4 import BeautifulSoup
import asyncio
from datetime import datetime, timezone

import json

async def get_all_data(session):
    '''
    Gets the cached data (for every squad)
    '''
    #data_url = "https://raw.githubusercontent.com/EpicEfeathers/wb/refs/heads/main/squad_info/squad_data.json"
    data_url = "https://raw.githubusercontent.com/EpicEfeathers/wb/refs/heads/main/data/squad_data.json"


    async with session.get(data_url) as response:
        return await response.json(content_type=None) # skips checking if it's JSON, just assumes it is

def extract_squad(all_data, squad_name):
    '''
    Gets the specific squad's data from all the squad data
    '''
    try:
        return all_data[squad_name]
    except KeyError:
        print(f"KeyError. Could not find squad '{squad_name}' in the cached data.")


async def get_data(session, squad_name):
    '''
    Gets data for a specific squad
    '''
    all_data = await get_all_data(session)
    squad_data = extract_squad(all_data, squad_name)
    
    return squad_data
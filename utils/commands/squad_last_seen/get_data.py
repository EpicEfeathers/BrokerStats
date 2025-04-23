import requests, aiohttp
from datetime import datetime, timezone
from utils import functions

import pyperclip

def get_squad_users(squad: str):
    users = requests.get(f"https://wbapi.wbpjs.com/squad/getSquadMembers?squadName={squad}").json()

    uids = [user["uid"] for user in users]

    return uids

async def get_user_data(session, uid):
    async with session.get(f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}") as resp:
        data = await resp.json()
    #data = requests.get(f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}").json()

    username = data["nick"]
    time_last_seen = datetime.fromtimestamp(data["time"], tz=timezone.utc) # GMT timezone
    formatted_time = time_last_seen.strftime("%b %d %Y, %H:%M")
    
    return {"username": username, 
            "formatted_time": formatted_time,
            "timestamp": data["time"] # timestamp
    }


async def get_all_data(uids):
    users_data = []
    async with aiohttp.ClientSession() as session:
        for uid in uids:
            users_data.append(await get_user_data(session, uid))

    return users_data


def sort_data(sort_type, data):
    if sort_type == "sort_asc":
        sorted_data = sorted(data, key=lambda x: x["username"].lower())
    elif sort_type == "sort_desc":
        sorted_data = sorted(data, key=lambda x: x["username"].lower(), reverse=True)
    elif sort_type == "sort_recent":
        sorted_data = sorted(data, key=lambda x: x["timestamp"], reverse=True)
    elif sort_type == "sort_oldest":
        sorted_data = sorted(data, key=lambda x: x["timestamp"])

    return sorted_data

def create_code_block(users_data:list, start_index, end_index):
    code_block = ""

    max_username_length = max([len(user["username"]) for user in users_data])

    end_index = min(end_index, len(users_data)) # make sure doesn't overflow data length
    for user in users_data[start_index:end_index]:
        code_block = code_block + f"\n[0;34m{user["username"]}{" " * (max_username_length-len(user["username"]))}   [0;37m{user["formatted_time"]}   [0;36m{functions.time_since_last_seen(user["timestamp"])}"

    code_block = f"```ansi\n[1;37mUsername{" " * (max_username_length-len("username"))}   Last seen (GMT)      Time ago\n{code_block}```" # convert to discord format

    return code_block

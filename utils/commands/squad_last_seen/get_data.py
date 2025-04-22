import requests
from datetime import datetime, timezone
from utils import functions

def get_squad_users(squad: str):
    users = requests.get(f"https://wbapi.wbpjs.com/squad/getSquadMembers?squadName={squad}").json()

    uids = [user["uid"] for user in users]

    return uids

def get_user_data(uid):
    data = requests.get(f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}").json()

    username = data["nick"]
    time_last_seen = datetime.fromtimestamp(data["time"], tz=timezone.utc) # GMT timezone
    formatted_time = time_last_seen.strftime("%b %d %Y, %H:%M")
    
    return {"username": username, 
            "formatted_time": formatted_time,
            "timestamp": data["time"] # timestamp
    }


def create_code_block(uids:list):
    code_block = ""

    users_data = []
    for uid in uids:
        users_data.append(get_user_data(uid))

    max_username_length = max([len(user["username"]) for user in users_data])
    for user in users_data:
        code_block = code_block + f"\n[0;34m{user["username"]}{" " * (max_username_length-len(user["username"]))}   [0;37m{user["formatted_time"]}   [0;36m{functions.time_since_last_seen(user["timestamp"])}"

    code_block = f"```ansi\n[1;37mUsername{" " * (max_username_length-len("username"))}   Last seen (GMT)      Time ago\n{code_block}```" # convert to discord format

    return code_block

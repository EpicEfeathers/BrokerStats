import requests

def get_user(uid):
    response = requests.get(f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}").json()

    steam = response["steam"]
    squad = response["squad"]
    level = response["level"]
    xp_percent = requests.get(f"https://wbapi.wbpjs.com/players/percentile/xp?uid={uid}").json()

    print(f"Steam: {steam}\nSquad: {squad}\nLevel: {level} {round(xp_percent, 2)}%")


get_user("609aa68ed142afe952202c5c")
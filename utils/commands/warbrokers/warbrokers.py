import requests

def fetch_playercount():
    return requests.get("https://warbrokers.io/players_online.php").text

def fetch_squad_number():
    squads = requests.get("https://wbapi.wbpjs.com/squad/getSquadList").json()
    
    return len(squads)

def return_warbrokers_stats():
    return f"Warbrokers\nOnline players: {fetch_playercount()}\nTotal Weapons: {22+5+7+5}\nTotal Maps: {27+10+2}\nTotal Cosmetics: 5107"

print(fetch_squad_number())
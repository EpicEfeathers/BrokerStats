import requests

PLAYER_COUNT_LINK = "https://warbrokers.io/players_online.php"

def fetch_playercount():
    return requests.get(PLAYER_COUNT_LINK).text

def return_warbrokers_stats():
    return f"Warbrokers\nOnline players: {fetch_playercount()}\nTotal Weapons: {22+5+7+5}\nTotal Maps: {27+10+2}\nTotal Cosmetics: 5107"

print(return_warbrokers_stats())
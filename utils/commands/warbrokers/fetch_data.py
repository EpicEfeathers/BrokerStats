import requests

def fetch_total_players():
    return requests.get("https://warbrokers.io/player_count.php").text

def fetch_playercount():
    return requests.get("https://warbrokers.io/players_online.php").text

def fetch_data():
    return fetch_total_players(), fetch_playercount()
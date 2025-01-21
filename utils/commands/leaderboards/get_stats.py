import requests
from bs4 import BeautifulSoup

daily_overall_items = {"Total Kills": "top0", "Classic Mode Wins": "top1"}
lifetime_overall_items = {"XP": "top0", "Total Kills": "top1", "BR Wins": "top2"}
weapons = {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}
vehicles = {"Tank LVL 1": "top0", "Tank LVL 2": "top1", "Tank LVL 3": "top2", "Apc LVL 1": "top3", "Apc LVL 2": "top4", "Apc LVL 3": "top5", "Heli LVL 1": "top6", "Heli LVL 2": "top7", "Heli LVL 3": "top8", "Jet (1 Fin)": "top9", "Jet (2 Fin)": "top10"}

def getItems(name, items, link):
    """
    Returns top users for wins and total kills
    """
    id = items[name]
    data = requests.get(link).text

    soup = BeautifulSoup(data, 'html.parser')
    vehicle_data = soup.find('div', id=id)

    entries = vehicle_data.find_all(class_='top-grid-index-number')

    results = []
    for index_div in entries:
        content_item = index_div.find_next_sibling('div', class_='top-grid-content-item') # gets div element with name
        value_div = content_item.find_next_sibling('div', class_='top-grid-content-value') # gets div element with # of kills/wins

        name = content_item.find('a').text.strip() # extracts name from div
        value = value_div.text.strip() # extract # of kills/wins from div
        results.append((name, value))

    return results

def getDailyOverall(item):
    return (getItems(item, daily_overall_items, "https://stats.warbrokers.io/top/daily?type=overall"))

def getDailyWeaponKills(item):
    return (getItems(item, weapons, "https://stats.warbrokers.io/top/daily?type=weaponKills"))

def getDailyVehicleKills(item):
    return (getItems(item, vehicles, "https://stats.warbrokers.io/top/daily?type=vehicleKills"))

def getDailyLongestKills(item):
    return (getItems(item, weapons, "https://stats.warbrokers.io/top/daily?type=longestWeaponKills"))



def getLifetimeOverall(item):
    return (getItems(item, lifetime_overall_items, "https://stats.warbrokers.io/top/overall"))

def getLifetimeWeaponKills(item):
    return (getItems(item, weapons, "https://stats.warbrokers.io/top/killsPerWeapon"))

def getLifetimeVehicleKills(item):
    return (getItems(item, vehicles, "https://stats.warbrokers.io/top/killsPerVehicle"))

def getLifetimeDamageDealt(item):
    return (getItems(item, weapons, "https://stats.warbrokers.io/top/damageDealt"))

def getLifetimeLongestKills(item):
    return (getItems(item, weapons, "https://stats.warbrokers.io/top/longestKills"))
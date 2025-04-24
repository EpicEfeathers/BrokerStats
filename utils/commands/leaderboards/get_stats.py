from bs4 import BeautifulSoup

daily_overall_items = {"Total Kills": "top0", "Classic Mode Wins": "top1"}
lifetime_overall_items = {"XP": "top0", "Total Kills": "top1", "BR Wins": "top2"}
weapons = {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}
vehicles = {"Tank LVL 1": "top0", "Tank LVL 2": "top1", "Tank LVL 3": "top2", "Apc LVL 1": "top3", "Apc LVL 2": "top4", "Apc LVL 3": "top5", "Heli LVL 1": "top6", "Heli LVL 2": "top7", "Heli LVL 3": "top8", "Jet (1 Fin)": "top9", "Jet (2 Fin)": "top10"}

async def getItems(session, item, link):
    async with session.get(link) as resp:
        data = await resp.text()
    soup = BeautifulSoup(data, "html.parser")

    # Find the leaderboard container
    sections = soup.findAll("div", class_="top-grid-content") # get all relevant sections

    for section in sections:
        weapon_name = section.find("div", class_="top-grid-content-header-name").text.strip()

        if weapon_name != item: # check if is correct weapon / vehicle / leaderboard item
            continue

        players = section.findAll("div", class_="top-grid-content-item")
        values = section.findAll("div", class_="top-grid-content-value")


        leaderboard = [(player.text.strip(), value.text.strip()) for player, value in zip(players, values)]

    return leaderboard

async def getDailyOverall(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/daily?type=overall"))

async def getDailyWeaponKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/daily?type=weaponKills"))

async def getDailyVehicleKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/daily?type=vehicleKills"))

async def getDailyLongestKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/daily?type=longestWeaponKills"))



async def getLifetimeOverall(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/overall"))

async def getLifetimeWeaponKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/killsPerWeapon"))

async def getLifetimeVehicleKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/killsPerVehicle"))

async def getLifetimeDamageDealt(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/damageDealt"))

async def getLifetimeLongestKills(session, item):
    return await (getItems(session, item, "https://stats.warbrokers.io/top/longestKills"))
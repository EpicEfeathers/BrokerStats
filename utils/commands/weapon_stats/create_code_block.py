import requests
import pyperclip
import random

WEAPONS = {'p09': 'Air Strike', 'p11': 'BGM', 'p61': 'AR', 'p62': 'AK', 'p63': 'Pistol', 'p64': 'Hunting', 'p65': 'RPG', 'p66': 'Shotgun', 'p67': 'Sniper', 'p68': 'SMG', 'p69': 'Homing', 'p71': 'Grenade', 'p76': 'Knife', 'p78': 'Revolver', 'p79': 'Minigun', 'p80': 'GL', 'p81': 'Smoke Grenade', 'p88': 'Fists', 'p89': 'VSS', 'p90': '.50', 'p91': 'MG Turret', 'p92': 'Crossbow', 'p93': 'SCAR', 'p94': 'Tac Shotty', 'p95': 'VEK', 'p96': 'Desert', 'p97': 'Auto Pistol', 'p98': 'LMG', 'p99': 'KBAR', 'p100': 'Mace', 'p101': 'Rubber Chicken', 'p102': 'Butterfly', 'p103': 'Chainsaw', 'p104': 'AK SMG', 'p105': 'Auto Sniper', 'p108': 'Healing Pistol', 'p110': 'Implosion', 'p111': 'Laser Trip Mine', 'p112': 'Concussion', 'p126': 'G3A3'}

def get_stats():
    data = requests.get("https://wbapi.wbpjs.com/players/getPlayer?uid=5a4d14e9bfea71227e1fc4bf").json()
    #data = {'uid': '609aa68ed142afe952202c5c', 'nick': 'EpicEfeathers', 'nicklower': 'epicefeathers', 'level': 141, 'xp': 3178015, 'coins': 1964, 'squad': 'BOT', 'killsELO': 1727.02, 'gamesELO': 1968.97, 'wins': {'m07': 5, 'm00': 995, 'm11': 3, 'm08': 5, 'm10': 11}, 'losses': {'m00': 687, 'm10': 5, 'm08': 4, 'm07': 1}, 'number_of_jumps': 179860, 'scuds_launched': 14, 'zombie_kills': 0, 'zombie_deaths': 0, 'zombie_wins': 0, 'self_destructs': {'v40': 8, 'v30': 442, 'v41': 9}, 'distance_driven': {'v30': 311829.2639, 'v00': 1726.83033, 'v40': 31127.448978, 'v02': 1883.23076, 'v10': 9477.13525, 'v13': 1587.804, 'v41': 40016.771056, 'v01': 1124.69447, 'v23': 16.7683, 'v11': 1728.3543, 'v21': 4938.723578, 'v12': 224.3899, 'v22': 1556.7076, 'v20': 1119.8181}, 'distance_driven_count': {'v30': 2349, 'v00': 13, 'v40': 28, 'v02': 12, 'v10': 48, 'v13': 3, 'v41': 35, 'v01': 9, 'v23': 1, 'v11': 17, 'v21': 12, 'v12': 2, 'v22': 5, 'v20': 7}, 'kills_per_vehicle': {'v30': 21388, 'v01': 12, 'v50': 19, 'v10': 23, 'v00': 13, 'v02': 5, 'v11': 7, 'v12': 1, 'v41': 11, 'v40': 5}, 'shots_fired_unzoomed': {'p61': 27465, 'p126': 1298, 'p09': 374, 'p11': 537, 'p63': 1320, 'p101': 42846, 'p105': 76, 'p71': 4487, 'p68': 67267, 'p52': 34, 'p69': 220, 'p58': 52, 'p75': 144, 'p88': 220, 'p97': 1783, 'p62': 20085, 'p104': 1830, 'p65': 95, 'p96': 89, 'p111': 6, 'p81': 132, 'p76': 16060, 'p66': 6822, 'p67': 592, 'p93': 598, 'p80': 115, 'p94': 144, 'p64': 8, 'p92': 72, 'p78': 1422, 'p89': 100, 'p91': 118, 'p55': 24, 'p82': 15, 'p56': 205, 'p53': 177, 'p103': 21, 'p57': 106, 'p112': 404, 'p85': 27, 'p59': 45, 'p110': 2227, 'p90': 350, 'p99': 26, 'p54': 15, 'p79': 65, 'p98': 186, 'p95': 12, 'p86': 114, 'p83': 76, 'p87': 240, 'p84': 59, 'p60': 4}, 'shots_fired_zoomed': {'p61': 58807, 'p126': 2021, 'p105': 3449, 'p68': 57032, 'p63': 537, 'p67': 15805, 'p97': 2112, 'p65': 368, 'p62': 28495, 'p96': 44, 'p66': 6012, 'p93': 1143, 'p92': 655, 'p78': 2719, 'p89': 255, 'p75': 173, 'p91': 1858, 'p55': 63, 'p58': 25, 'p53': 1049, 'p56': 60, 'p57': 329, 'p101': 1, 'p94': 117, 'p95': 153, 'p98': 467, 'p52': 50, 'p104': 1554, 'p112': 71, 'p64': 241, 'p59': 54, 'p60': 1, 'p99': 5, 'p54': 11, 'p85': 3, 'p79': 796, 'p87': 306, 'p82': 3, 'p84': 136, 'p110': 3, 'p86': 1, 'p80': 4}, 'shots_hit_unzoomed': {'p61': 6829, 'p126': 293, 'p09': 841, 'p63': 449, 'p11': 454, 'p101': 780, 'p71': 1488, 'p68': 12668, 'p105': 20, 'p69': 99, 'p58': 19, 'p65': 69, 'p96': 15, 'p75': 47, 'p111': 4, 'p62': 4770, 'p66': 1635, 'p67': 239, 'p93': 121, 'p88': 16, 'p80': 16, 'p64': 4, 'p94': 31, 'p92': 30, 'p78': 626, 'p89': 15, 'p56': 100, 'p53': 58, 'p52': 19, 'p112': 302, 'p76': 157, 'p97': 158, 'p55': 8, 'p104': 310, 'p103': 1, 'p110': 1168, 'p59': 3, 'p90': 161, 'p85': 6, 'p79': 15, 'p98': 91, 'p95': 4, 'p86': 75, 'p83': 57, 'p87': 5, 'p54': 5, 'p84': 2, 'p57': 41, 'p82': 6, 'p60': 1, 'p99': 1}, 'shots_hit_zoomed': {'p61': 14207, 'p126': 415, 'p105': 1270, 'p68': 13136, 'p63': 202, 'p67': 7651, 'p65': 232, 'p62': 6605, 'p96': 14, 'p66': 1253, 'p93': 349, 'p92': 161, 'p89': 42, 'p91': 279, 'p75': 18, 'p56': 23, 'p57': 118, 'p94': 37, 'p78': 1523, 'p52': 25, 'p104': 287, 'p112': 45, 'p64': 82, 'p55': 21, 'p97': 384, 'p53': 340, 'p60': 1, 'p59': 4, 'p79': 281, 'p98': 97, 'p95': 28, 'p54': 6, 'p87': 2, 'p110': 1, 'p80': 2}, 'damage_dealt': {'p61': 172333.33281, 'p105': 67702.331, 'p126': 5943.48364, 'p09': 28865.05423, 'p63': 7945.2066, 'p11': 189880.63777, 'p101': 153000, 'p68': 254251.32395, 'p71': 192163.79165, 'p69': 28791.6194, 'p67': 1166467.236, 'p58': 1302.0003, 'p65': 75395.3105, 'p96': 1077.42271, 'p75': 974.71754, 'p62': 123548.35529, 'p111': 958.6736, 'p66': 10821.96703, 'p93': 3156.36309, 'p88': 120, 'p80': 330.4343, 'p64': 3001.4575, 'p94': 279.5414, 'p92': 34500, 'p78': 80886.13767, 'p89': 173.0456, 'p91': 238.81225, 'p56': 289, 'p53': 829.45906, 'p57': 24.07265, 'p52': 3380.214, 'p104': 5253.9328, 'p112': 4950.693791, 'p76': 35375, 'p55': 1816.382, 'p97': 4783.9627, 'p60': 324.0861, 'p103': 600, 'p110': 2399.9840961, 'p59': 57.3835, 'p90': 20340, 'p85': 473.896, 'p79': 406.17802, 'p98': 1273.02, 'p95': 37.412, 'p86': 2291.9164, 'p83': 1200, 'p87': 107.5545, 'p54': 99.4762, 'p84': 22.2, 'p82': 32.5557, 'p99': 375}, 'damage_received': {'p62': 511751.24796, 'p61': 684817.76989, 'p95': 104655.9295, 'p63': 6257.1767, 'p71': 189587.007759, 'p104': 400767.53616, 'p09': 76539.00974, 'p105': 102962.5, 'p67': 911535.005, 'p68': 425111.8291, 'p93': 253888.78896, 'p126': 80733.97281, 'p78': 21590.8193, 'p56': 8937.1173, 'p92': 57375, 'p65': 29205.2204, 'p94': 23826.67311, 'p64': 67333.4876, 'p83': 7358.8423, 'p84': 7765.8762, 'p75': 9096.4533, 'p111': 32374.6193, 'p53': 12816.1443, 'p11': 126847.8542, 'p97': 23725.6319, 'p52': 14331.0375, 'p89': 75715.0278, 'p55': 18594.8849, 'p58': 14075.1213, 'p112': 16530.907555, 'p87': 3966.4265, 'p85': 2482.1142, 'p79': 28254.24363, 'p96': 10357.273, 'p66': 39458.37833, 'p80': 10593.712, 'p76': 8250, 'p90': 98186.255, 'p98': 18769.8559, 'p82': 1789.7146, 'p57': 8385.07371, 'p54': 3210.8405, 'p69': 9306.733, 'p101': 4500, 'p110': 4390.4022597, 'p103': 1800, 'p74': 961.464, 'p59': 1317.957, 'p86': 7322.0897, 'p88': 150, 'p91': 3510.9015, 'p60': 1888.2261, 'p99': 20625, 'p100': 150, 'p102': 380}, 'kills_per_weapon': {'p61': 3252, 'p105': 484, 'p126': 98, 'p09': 165, 'p101': 543, 'p68': 5414, 'p71': 355, 'p69': 25, 'p65': 144, 'p62': 2177, 'p63': 101, 'p66': 300, 'p67': 6220, 'p93': 54, 'p64': 23, 'p94': 3, 'p92': 191, 'p78': 516, 'p89': 8, 'p11': 244, 'p96': 2, 'p75': 4, 'p91': 19, 'p88': 1, 'p52': 11, 'p112': 6, 'p76': 111, 'p58': 3, 'p97': 34, 'p55': 9, 'p56': 4, 'p104': 109, 'p103': 1, 'p53': 7, 'p90': 93, 'p111': 1, 'p79': 2, 'p98': 16, 'p95': 1, 'p86': 10, 'p83': 5, 'p99': 1, 'p87': 1}, 'deaths': {'p62': 944, 'p61': 1102, 'p95': 215, 'p71': 247, 'p104': 828, 'p105': 164, 'p67': 1917, 'p93': 434, 'p126': 168, 'p68': 926, 'p92': 152, 'p94': 44, 'p75': 15, 'p111': 53, 'p97': 45, 'p11': 209, 'p87': 5, 'p79': 41, 'p89': 136, 'p96': 16, 'p64': 93, 'p53': 14, 'p76': 19, 'p66': 78, 'p90': 131, 'p63': 12, 'p80': 10, 'p78': 26, 'p98': 23, 'p09': 147, 'p84': 9, 'p52': 12, 'p55': 21, 'p112': 14, 'p65': 24, 'p56': 7, 'p58': 11, 'p57': 5, 'p101': 9, 'p91': 2, 'p85': 1, 'p54': 2, 'p103': 2, 'p99': 36, 'p69': 3, 'p86': 4, 'p60': 2, 'p83': 1, 'p102': 2, 'p110': 1, 'p74': 1}, 'headshots': {'p61': 8681, 'p126': 200, 'p105': 778, 'p63': 365, 'p68': 12655, 'p62': 4571, 'p96': 10, 'p66': 1632, 'p67': 5864, 'p93': 150, 'p64': 56, 'p94': 29, 'p78': 1435, 'p89': 30, 'p75': 5, 'p91': 147, 'p53': 18, 'p104': 317, 'p57': 91, 'p97': 274, 'p56': 12, 'p55': 5, 'p59': 2, 'p90': 78, 'p52': 4, 'p79': 5, 'p98': 40, 'p95': 1}, 'banned': False, 'steam': True, 'time': 1744901120, 'joinTime': 1728158106}
    return data

# USE FUINCTIONS IN FINAL CODE
# AHIAHFOFH
# HSIGHW EG
# HSH W
def format_large_number(number):
    return f"{int(number):,}"


text = ""

class positions:
    weapon_name = 0
    kills = 38
    longest = 35
    accuracy = 48
    damage = 66

def convert_weapon_names(data, WEAPONS):
    """
    Removes non-player weapons,
    converts names to human readable
    """

    converted = {}
    for weapon, weapon_name in WEAPONS.items():
        if weapon in data.keys():
            converted[weapon_name] = data[weapon]
        else:
            converted[weapon_name] = 0

    print(converted)
    sorted_data = dict(sorted(converted.items()))
    print(sorted_data)

    return sorted_data

def generate_bar_chart():
    pass


def write_text_at_position(text, text_to_add, x, y, alignment):
    text = text.split("\n")

    while len(text) < y + 1:
        text.append("")



    if alignment[0] == "r":
        if len(text[y]) < x:
            text[y] += (" " * (x - len(text_to_add) - len(text[y])))
            text[y] += text_to_add

    elif alignment[0] == "l":
        text[y] += (" " * x)
        text[y] += text_to_add

    return ("\n").join(text)

def convert_to_discord(text):
    text = f'''```ansi
                   Kills
    {text}```
    '''

    return text

data = get_stats()
kills_data = data.get("kills_per_weapon")
converted_data = convert_weapon_names(kills_data, WEAPONS)

for y, weapon in enumerate(converted_data):
    text = write_text_at_position(text, f"[2;32m{weapon}", positions.weapon_name, 1 + y, "l")
    text = write_text_at_position(text, f"[2;37m{str(format_large_number(converted_data[weapon]))}", positions.kills, 1 + y, "r")
    text = write_text_at_position(text, "█" *random.randint(3, 3), 4, 1 + y, "l")

'''damage_data = data.get("damage_dealt")
converted_data = convert_weapon_names(damage_data, WEAPONS)
for y, weapon in enumerate(converted_data):
    #text = write_text_at_position(text, weapon, positions.weapon_name, 1 + y, "l")
    text = write_text_at_position(text, str(round(converted_data[weapon])), positions.damage, 1 + y, "r")'''


text = convert_to_discord(text)

print(text)


pyperclip.copy(text)

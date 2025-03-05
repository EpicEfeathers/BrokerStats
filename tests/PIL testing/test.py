import pprint

maps = {
    "Area 15 Base": 21,
    "Area 15 Bunker": 22,
    "City Point": 13,
    "Cologne": 44,
    "Desert": 0,
    "Escape": 6,
    "Flooded": 4,
    "Frontier": 31,
    "Goldmine": 47,
    "Goldmine V2": 49,
    "Heist": 32,
    "Kitchen": 29,
    "Moonbase": 20,
    "Northwest": 1,
    "Office": 3,
    "Pacific": 2,
    "Remagen": 8,
    "Siege": 39,
    "Skullisland": 24,
    "Southwest": 7,
    "Spacestation": 38,
    "Temple": 5,
    "The Somme": 15,
    "Tomb": 14,
    "Tribute": 18,
    "Cyber Tribute": 19,
    "Zen Garden": 43,
    "Containers": 37,
    "Crisscross": 40,
    "Dwarfsdungeon": 28,
    "Hanger": 25,
    "Pyramid": 36,
    "Quarry": 27,
    "Sniper Alley": 35,
    "Snipers Only": 41,
    "Three Lane": 34,
    "Tower Of Power": 33,
}

new_maps = {}
for key, value in maps.items():
    new_maps[value] = key

pprint.pprint(new_maps)
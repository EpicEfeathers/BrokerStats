import discord
import math

PAGE_SIZE = 25

category = {"dailyOverall": {"Total Kills": "top0", "Classic Mode Wins": "top1"}, "dailyWeaponKills": {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}, "dailyVehicleKills": {"Tank LVL 1": "top0", "Tank LVL 2": "top1", "Tank LVL 3": "top2", "Apc LVL 1": "top3", "Apc LVL 2": "top4", "Apc LVL 3": "top5", "Heli LVL 1": "top6", "Heli LVL 2": "top7", "Heli LVL 3": "top8", "Jet (1 Fin)": "top9", "Jet (2 Fin)": "top10"}, "dailyLongestWeaponKills": {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}, "lifetimeOverall": {"XP": "top0", "Total Kills": "top1", "BR Wins": "top2"}, "lifetimeWeaponKills": {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}, "lifetimeVehicleKills": {"Tank LVL 1": "top0", "Tank LVL 2": "top1", "Tank LVL 3": "top2", "Apc LVL 1": "top3", "Apc LVL 2": "top4", "Apc LVL 3": "top5", "Heli LVL 1": "top6", "Heli LVL 2": "top7", "Heli LVL 3": "top8", "Jet (1 Fin)": "top9", "Jet (2 Fin)": "top10"}, "lifetimeWeaponDamage": {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}, "lifetimeLongestKills": {"AR Rifle": "top0", "AK Rifle": "top1", "SCAR": "top2", "Sniper": "top3", ".50 Cal Sniper": "top4", "Hunting": "top5", "SMG": "top6", "VEK": "top7", "VSS": "top8", "Shotgun": "top9", "Tactical Shotgun": "top10", "Crossbow": "top11", "LMG": "top12", "Minigun": "top13", "Revolver": "top14", "Pistol": "top15", "Knife": "top16", "Rubber Chicken": "top17", "Grenade": "top18", "G. Launcher": "top19", "Laser Trip Mine": "top20", "RPG": "top21", "Air Strike": "top22", "BGM": "top23", "Homing": "top24", "MG Turret": "top25", "Fists": "top26"}}

TIMEOUT = 180

class Dropdown(discord.ui.Select):
    def __init__(self, category:list, num, type_:str, selected):
        items = list(category.items())
        self.type_ = type_
        options = [discord.SelectOption(label=item_name, default=(item_name==selected)) for (item_name, item_id) in (items[(num-1)*PAGE_SIZE:num*PAGE_SIZE])] # sets correct item to selected, adds rest to dropdown

        super().__init__(min_values=1, max_values=1, options=options, row=1) # select min and max 1 value (only select one thing), custom options, row is 1

    async def callback(self, interaction: discord.Interaction):
        from utils.commands.leaderboards.daily import daily
        from utils.commands.leaderboards.lifetime import lifetime

        types = {
            "dailyOverall": lambda: daily.daily_overall,
            "dailyWeaponKills": lambda: daily.daily_weapon_kills,
            "dailyVehicleKills": lambda: daily.daily_vehicle_kills,
            "dailyLongestWeaponKills": lambda: daily.daily_longest_kills,
            "lifetimeOverall": lambda: lifetime.lifetime_overall,
            "lifetimeVehicleKills": lambda: lifetime.lifetime_vehicle_kills,
            "lifetimeWeaponKills": lambda: lifetime.lifetime_weapon_kills,
            "lifetimeWeaponDamage": lambda: lifetime.lifetime_weapon_damage,
            "lifetimeLongestKills": lambda: lifetime.lifetime_longest_kills
        }
        
        stat_card, view = await types[self.type_]()(self.values[0])

        await interaction.response.defer()
        await interaction.edit_original_response(content="", attachments=[stat_card], view=view)

class Counter(discord.ui.View):
    def __init__(self, type_:int, selected:str):
        super().__init__(timeout=TIMEOUT)
        self.category = category[type_]
        self.num = 1
        self.type_ = type_

        self.dropdown = Dropdown(self.category, self.num, type_, selected)
        self.add_item(self.dropdown)

        self.right.disabled = len(self.category) <= 25

        self.response = None

        button_mapping = {"dailyOverall": "daily?type=overall", "dailyWeaponKills": "daily?type=weaponKills", "dailyVehicleKills": "daily?type=vehicleKills", "dailyLongestWeaponKills": "daily?type=longestWeaponKills", "lifetimeOverall": "overall", "lifetimeWeaponKills": "killsPerWeapon", "lifetimeVehicleKills": "killsPerVehicle", "lifetimeWeaponDamage": "damageDealt", "lifetimeLongestKills": "longestKills"}
        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/top/{button_mapping[self.type_]}"))
        #self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/players/{uid}")) Not available yet
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))


    async def on_timeout(self) -> None:
        if self.response:
            self.dropdown.placeholder = 'This command has timed out!'

            for option in self.dropdown.options:
                option.default = False # without this, default overrides placeholder

            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.url is None:
                    item.disabled = True
                elif not isinstance(item, discord.ui.Button):
                    item.disabled = True

            await self.response.edit(view=self)

    @discord.ui.button(emoji="<:left_arrow:1301174573051416618>", style=discord.ButtonStyle.blurple, row=2, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num > 1:
            self.num -=1

        await self.update(interaction)

    # right button
    @discord.ui.button(emoji="<:right_arrow:1301174594581037088>", style=discord.ButtonStyle.blurple, row=2)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num < math.ceil(len(self.category)/25):
            self.num +=1

        await self.update(interaction)

    async def update(self, interaction):
        user_items = list(self.category.items())
        self.dropdown.options = [discord.SelectOption(label=item_name) for (item_name, item_id) in (user_items[(self.num-1)*PAGE_SIZE : self.num*PAGE_SIZE])]

        self.left.disabled = self.num == 1
        self.right.disabled = self.num == math.ceil((len(self.category)/25))

        await interaction.response.edit_message(view=self)
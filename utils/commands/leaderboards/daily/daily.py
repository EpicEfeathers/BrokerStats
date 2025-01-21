import discord
import traceback
from utils.commands.leaderboards import views, create_image, get_stats

img_path = "utils/commands/leaderboards/daily/backgrounds"

async def daily_overall(item_name):
    data = get_stats.getDailyOverall(item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("dailyOverall", item_name) # creating view
    
    return stat_card, view

async def daily_weapon_kills(weapon_name):
    data = get_stats.getDailyWeaponKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("dailyWeaponKills", weapon_name) # creating view

    return stat_card, view

async def daily_vehicle_kills(vehicle_name):
    data = get_stats.getDailyVehicleKills(vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("dailyVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def daily_longest_kills(weapon_name):
    data = get_stats.getDailyLongestKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("dailyLongestWeaponKills", weapon_name) # creating view
    
    return stat_card, view
import discord
import traceback
from utils.commands.leaderboards import views, create_image, get_stats

img_path = "utils/commands/leaderboards/backgrounds"

async def daily_overall(original_user_id, item_name):
    data = get_stats.getDailyOverall(item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Overall", subcategory=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "dailyOverall", item_name) # creating view
    
    return stat_card, view

async def daily_weapon_kills(original_user_id, weapon_name):
    data = get_stats.getDailyWeaponKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Kills (Round)", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "dailyWeaponKills", weapon_name) # creating view

    return stat_card, view

async def daily_vehicle_kills(original_user_id, vehicle_name):
    data = get_stats.getDailyVehicleKills(vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Kills (Round)", subcategory=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "dailyVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def daily_longest_kills(original_user_id, weapon_name):
    data = get_stats.getDailyLongestKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Longest", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "dailyLongestWeaponKills", weapon_name) # creating view
    
    return stat_card, view
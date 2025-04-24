import discord
import traceback
from utils.commands.leaderboards import views, create_image, get_stats

img_path = "utils/commands/leaderboards/backgrounds"

async def daily_overall(session, original_user_id, item_name):
    data = await get_stats.getDailyOverall(session, item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Overall", subcategory=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "dailyOverall", item_name) # creating view
    
    return stat_card, view

async def daily_weapon_kills(session, original_user_id, weapon_name):
    data = await get_stats.getDailyWeaponKills(session, weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Kills (Round)", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "dailyWeaponKills", weapon_name) # creating view

    return stat_card, view

async def daily_vehicle_kills(session, original_user_id, vehicle_name):
    data = await get_stats.getDailyVehicleKills(session, vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Kills (Round)", subcategory=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "dailyVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def daily_longest_kills(session, original_user_id, weapon_name):
    data = await get_stats.getDailyLongestKills(session, weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Daily Longest", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "dailyLongestWeaponKills", weapon_name) # creating view
    
    return stat_card, view
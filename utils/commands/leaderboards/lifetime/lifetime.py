import discord
import traceback
from utils.commands.leaderboards import create_image, get_stats, views

img_path = "utils/commands/leaderboards/backgrounds"

async def lifetime_overall(original_user_id, item_name):
    data = get_stats.getLifetimeOverall(item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Overall", subcategory=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "lifetimeOverall", item_name) # creating view
    
    return stat_card, view

async def lifetime_weapon_kills(original_user_id, weapon_name):
    data = get_stats.getLifetimeWeaponKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Kills (Round)", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "lifetimeWeaponKills", weapon_name) # creating view

    return stat_card, view

async def lifetime_vehicle_kills(original_user_id, vehicle_name):
    data = get_stats.getLifetimeVehicleKills(vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Kills (Round)", subcategory=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "lifetimeVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def lifetime_weapon_damage(original_user_id, weapon_name):
    data = get_stats.getLifetimeDamageDealt(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Damage", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "lifetimeWeaponDamage", weapon_name) # creating view
    
    return stat_card, view

async def lifetime_longest_kills(original_user_id, weapon_name):
    data = get_stats.getLifetimeLongestKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Longest", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(original_user_id, "lifetimeLongestKills", weapon_name) # creating view
    
    return stat_card, view
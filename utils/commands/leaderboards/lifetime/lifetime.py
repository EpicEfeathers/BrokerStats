import discord
import traceback
from utils.commands.leaderboards import create_image, get_stats, views

img_path = "utils/commands/leaderboards/backgrounds"

async def lifetime_overall(session, original_user_id, item_name):
    data = await get_stats.getLifetimeOverall(session, item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Overall", subcategory=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "lifetimeOverall", item_name) # creating view
    
    return stat_card, view

async def lifetime_weapon_kills(session, original_user_id, weapon_name):
    data = await get_stats.getLifetimeWeaponKills(session, weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Kills (Round)", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "lifetimeWeaponKills", weapon_name) # creating view

    return stat_card, view

async def lifetime_vehicle_kills(session, original_user_id, vehicle_name):
    data = await get_stats.getLifetimeVehicleKills(session, vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Kills (Round)", subcategory=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "lifetimeVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def lifetime_weapon_damage(session, original_user_id, weapon_name):
    data = await get_stats.getLifetimeDamageDealt(session, weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Damage", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "lifetimeWeaponDamage", weapon_name) # creating view
    
    return stat_card, view

async def lifetime_longest_kills(session, original_user_id, weapon_name):
    data = await get_stats.getLifetimeLongestKills(session, weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category="Lifetime Longest", subcategory=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter(session, original_user_id, "lifetimeLongestKills", weapon_name) # creating view
    
    return stat_card, view
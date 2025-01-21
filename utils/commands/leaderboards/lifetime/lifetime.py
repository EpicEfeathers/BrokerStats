import discord
import traceback
from utils.commands.leaderboards import create_image, get_stats, views

img_path = "utils/commands/leaderboards/lifetime/backgrounds"

async def lifetime_overall(item_name):
    data = get_stats.getLifetimeOverall(item_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=item_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("lifetimeOverall", item_name) # creating view
    
    return stat_card, view

async def lifetime_weapon_kills(weapon_name):
    data = get_stats.getLifetimeWeaponKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("lifetimeWeaponKills", weapon_name) # creating view

    return stat_card, view

async def lifetime_vehicle_kills(vehicle_name):
    data = get_stats.getLifetimeVehicleKills(vehicle_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=vehicle_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("lifetimeVehicleKills", vehicle_name) # creating view

    return stat_card, view

async def lifetime_weapon_damage(weapon_name):
    data = get_stats.getLifetimeDamageDealt(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("lifetimeWeaponDamage", weapon_name) # creating view
    
    return stat_card, view

async def lifetime_longest_kills(weapon_name):
    data = get_stats.getLifetimeLongestKills(weapon_name) # getting necessary data
    stat_card = discord.File(fp=create_image.create_stats_card(data=data, category=weapon_name, img_path=img_path), filename="stat_card.png") # creating stat card
    view = views.Counter("lifetimeLongestKills", weapon_name) # creating view
    
    return stat_card, view
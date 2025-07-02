# Discord imports
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
import traceback
from aiohttp import ClientSession, ClientTimeout

import commands as my_commands
from utils.monitor_pi import monitor_stats
from utils.database_stuff import functions as db_functions
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

activity = discord.Activity(name = "my activity", type = discord.ActivityType.custom, state = "Shooting bots")
intents = discord.Intents().default()

GUILDS = [discord.Object(id=1295425214020194304), discord.Object(id=901934922997055499)]
SQUAD_LIST_URL = "https://wbapi.wbpjs.com/squad/getSquadList"

# Mybot class
class Mybot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, activity: discord.Activity):
        super().__init__(command_prefix="", intents=intents, activity=activity)
        self.session = None
        #self.tree = app_commands.CommandTree(self)
        #self.squad_list

    # sets commands to just the official server (so no 1 hour wait) CHANGE UPON RELEASE
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        for guild in GUILDS:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

        self.session = ClientSession() # setting here, as must be in async function


    async def close(self): # override discord's base closing method (to close aiohttp session)
        print("Shutting down...")

        await super().close()  # need this! shuts down bot

        await self.session.close() # closes aiohttp session


    @tasks.loop(hours=5.0)
    async def get_squads(self):
        url = "https://wbapi.wbpjs.com/squad/getSquadList"

        #async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        try:
            async with self.session.get(url, timeout=ClientTimeout(total=10)) as response:
                self.squad_list = await response.json()
        except asyncio.TimeoutError:
            print("Getting squad list timed out. Falling back to default list.")
            self.squad_list = ['-HCM-', '-Rebel-', '.INJ', '@__@', '@_@', '^_^AURA', '<DEVILS>', '<KILL>', '$$$', '007', '00N', '4GE', '50.CAL', '9Ine', 'a-10s', 'ABC', 'ACE', 'ACES', 'ACWB', 'AHK', 'AI', 'ALASKA', 'Alex140', 'ALPHA', 'America', 'AOS', 'APEX', 'APG', 'APG-JR', 'Aplpha', 'ARRAKIS', 'Arrow', 'AURORA', 'AUS', 'AusNZ', 'AWM', 'B.I.G', 'B0NK', 'Babayaga', 'BATFISH', 'BEAST', 'BEKAS', 'Best', 'besteod', 'BETA', 'BLAST', 'BLOON', 'BoA', 'BOT', 'BROS', 'BTB', 'Bully', 'BUMS', 'Buster', 'CAESAR', 'CANADA', 'Castilla', 'CCS', 'Charcoal', 'Chicken', 'COA', 'CODENAME', 'Cometer', 'Corgi', 'CraZy', 'CRO', 'D.J', 'Delta', 'DELTA_1', 'DEUS', 'DEV', 'DEVIL', 'DEVILS', 'DIABLO', 'Doggy', 'DOOFIE', 'DUBOS', 'DUCK', 'DUST', 'DUTCH', 'Dynamic', 'Eagles', 'Eclipse', 'EDF', 'EDG8', 'EK', 'ELLAS', 'ENFORCE', 'EP3R', 'ESP', 'Exile', 'F.C.', 'FA', 'Falcons', 'FAM', 'FEMBOY', 'FIGHTER', 'FIGHTERS', 'FISH', 'FLAMES', 'FORCE', 'Friends', 'FROZEN', 'FSB', 'FTW', 'FUMBLE', 'FUNCTION', 'Fuse', 'Fussel', 'GBros', 'generals', 'Ghost', 'ghosts_', 'GIGN', 'GINGER', 'Gladiat', 'GLORY', 'GO_SBKN!', 'GOC', 'GSG-9', 'GUEST', 'Guests', 'H.M.S', 'HAKER', 'HAMMER', 'HAZARD', 'HellWall', 'HF', 'Homies', 'HOT', 'HP', 'HRD', 'HRT', 'HSG', 'Hunter', 'ICE', 'ICED', 'IHS', 'IMMORTAL', 'INJ.', 'INSANE', 'ISR', 'issam', 'Japan', 'JDM', 'JOJO', 'JUSTICE', 'K-12', 'K.B.9', 'K.I.A.', 'KA-52', 'KDR', 'killeres', 'Kinetic', 'Korea_', 'KSK', 'KVLT', 'LEG1ON', 'LEGENDS', 'LEGION', 'LEO', 'Lokivile', 'LONGSHOT', "LOR'D", 'Love', 'LP', 'M.E.G', 'MAFIA', 'Maun', 'MED', 'mexicans', 'MIB', 'MKVI', 'MONKAAA', 'MoW', 'MPP', 'MURICA', 'musters', 'MZR', 'nachos', 'NANDOS', 'neavy', 'NEPTUNE', 'NERDS', 'NEURO', 'NK-Zone', 'nomuhyun', 'NRA', 'NRG', 'Nucleus', 'NWP', 'NX-01', 'OBJECT', 'OMEGA', 'ORANGE', 'OTSG', 'OUTLAW', 'P.T.S.D', 'PAIN', 'PANZER', 'Patate', 'PCrewAUS', 'PENTEST', 'Phantom', 'PHP', 'Pingu', 'PLG', 'PMC', 'POG', 'PoIar', 'POKE', 'Polar', 'POW', 'Predator', 'PROBOIZ', 'PROTOGEN', 'PSE', 'RaB', 'RANGERS', 'RAT', 'Rawleak', 'REAL', 'Reaper', 'RedFlys', 'Relaxman', 'REX', 'RG4L', 'ROGUE', 'RoX', 'RPG', 'RU$', 'RUS', 'RWS', 'S.T', 'SAS', 'saveTF2', 'SAVIOR', 'Scorpio', 'SCREAM', 'Scythe', 'SEAL', 'SFMF', 'Shadow', 'SHD', 'SHERB', 'SHFT', 'SIGMA', 'Sine', 'SK', 'Skittles', 'Skynet', 'Slavs', 'SoH', 'SOLDERS', 'sorpox', 'SOSI', 'SpecOps', 'SPED', 'Spetsnaz', 'sq33427', 'sq93488', 'Squadles', 'SSR', 'STAR', 'State', 'strength', 'STRIKE', 'STRIKER', 'Summer', 'SupR', 'SVEN', 't_and_co', 'TACOS', 'Tank', 'TEA', 'TEK', 'tff', 'THAI', 'the_c.f.', 'THEBOYZ', 'TheEnd', 'Thunder', 'TLN', 'TopGun', 'TopHat', 'totati', 'TotNA', 'Toxic', 'Tradie', 'TRUCK', 'U.S.A', 'U.S.S', 'UMS', 'USA_TACO', 'USS', 'uwu<3', 'VANGAURD', 'Vertex', 'VEX', 'Vortex', 'vortexs', 'VVV', 'W.S', 'Waffles', 'WarBroke', 'Warzone', 'WBTeam', 'WCS', 'what', 'WoH', 'WOLF', 'Wolves', 'YOS']

    '''@tasks.loop(minutes=30)
    async def update_pi_stats(self):
        message_id = 1304199817278259274  # Replace with the message ID you want to edit
        channel_id = 1304092651083141120  # Replace with the channel ID of the message

        # Get the channel and the message
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        file, embed = monitor_stats()
        await message.edit(embed=embed)

        print("Updated Pi Stats")'''


bot = Mybot(intents=intents,activity=activity)

# When bot boots
@bot.event
async def on_ready():
    try:
        bot.get_squads.start()
        #bot.update_pi_stats.start()
    except Exception as e: # if running already
        print(e)
        pass
    print(f"Successfully logged in as \033[1m{bot.user}\033[0m")    
    
my_commands.stats(bot)
my_commands.linkstats(bot)
my_commands.squad(bot)
my_commands.leaderboard(bot)
my_commands.help(bot)
my_commands.faq(bot)
my_commands.broker_stats(bot)
my_commands.player_count(bot)
my_commands.mapper(bot)
my_commands.warbrokers(bot)
my_commands.weapon_stats(bot)
my_commands.trends(bot)
my_commands.last_seen(bot)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        user_id = interaction.user.id
        db_functions.add_message_to_uid(user_id)

# error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    print(f"\033[91m{error}\033[0m")

    traceback.print_exception(type(error), error, error.__traceback__) # prints full traceback

    error_message = ":exclamation: An error occured while processing the request. If this error continues, please report it through the support server. https://discord.gg/8r52JxkJez"
    if interaction.response.is_done(): # if the command has already been responded too
        await interaction.followup.send(error_message)
    else:
        await interaction.response.send_message(error_message, ephemeral=True)

# CHANGE SECRET ON RELEASE
# HEY YOUUUUUUUU - CHANGELOG IN DISCORD + VERSION NUMBER :P
client.run('client secret')#, log_handler = handler)
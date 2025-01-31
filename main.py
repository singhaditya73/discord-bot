import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from cogs.crypto import Crypto
from cogs.competition import Competition
from cogs.basic_commands import BasicCommand  
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def setup_hook():
    await bot.add_cog(Crypto(bot)) 
    await bot.add_cog(Competition(bot)) 
    await bot.add_cog(BasicCommand(bot)) 

bot.setup_hook = setup_hook

# Run the bot
bot.run(TOKEN)


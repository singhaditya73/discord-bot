import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from cogs.crypto import Crypto
from cogs.competition import Competition
from cogs.basic_commands import BasicCommand  # Corrected the filename and class name

# Load environment variables from .env file
load_dotenv()

# Load token from environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Remove the default help command (if you want to customize your help command)
bot.remove_command('help')

# Load the cogs when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Setup hook to add cogs
async def setup_hook():
    await bot.add_cog(Crypto(bot))  # Add the Crypto cog
    await bot.add_cog(Competition(bot))  # Add the Competition cog
    await bot.add_cog(BasicCommand(bot))  # Add the BasicCommand cog (corrected class name)

# Assign setup hook to the bot
bot.setup_hook = setup_hook

# Run the bot
bot.run(TOKEN)


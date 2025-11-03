import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all cogs
async def load_cogs():
    cogs = ['moderation', 'utility', 'custom_commands', 'ai_chat']
    for cog in cogs:
        try:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog} cog')
        except Exception as e:
            print(f'Failed to load {cog}: {e}')

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    print(f'Bot is in {len(bot.guilds)} servers')
    await load_cogs()

# Keep bot alive on Replit
keep_alive()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))

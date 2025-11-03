import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_cogs():
    cogs = ['moderation', 'utility', 'custom_commands', 'ai_chat', 'music']
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
    
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))

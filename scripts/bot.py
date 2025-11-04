import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    await bot.load_extension('scripts.cogs.moderation')
    await bot.load_extension('scripts.cogs.utility')
    await bot.load_extension('scripts.cogs.custom_commands')
    await bot.load_extension('scripts.cogs.ai_chat')
    await bot.load_extension('scripts.cogs.music')
    await bot.load_extension('scripts.cogs.welcomer')
    print('[v0] All cogs loaded successfully!')

@bot.event
async def on_ready():
    print(f'[v0] {bot.user} is now online!')
    print(f'[v0] Bot is in {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Game(name="/help | Joey's Bot"))
    
    try:
        synced = await bot.tree.sync()
        print(f'[v0] Synced {len(synced)} slash commands to Discord!')
        print('[v0] Commands should appear when you type / in Discord')
        print('[v0] Note: It may take up to 1 hour for Discord to update commands globally')
    except Exception as e:
        print(f'[v0] Failed to sync commands: {e}')

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore command not found errors
    else:
        print(f'[v0] Error: {error}')
        await ctx.send(f"An error occurred: {str(error)}")

async def main():
    async with bot:
        await load_extensions()
        TOKEN = os.getenv('DISCORD_TOKEN')
        if not TOKEN:
            print('[v0] ERROR: DISCORD_TOKEN not found in environment variables!')
            return
        await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

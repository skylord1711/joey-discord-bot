import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
@bot.event
async def on_ready():
    print(f'[v0] {bot.user} is now online!')
    print(f'[v0] Bot is in {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Game(name="!help | Joey's Bot"))
    
    # Load all cogs
    await bot.load_extension('scripts.cogs.moderation')
    await bot.load_extension('scripts.cogs.music')
    await bot.load_extension('scripts.cogs.utility')
    await bot.load_extension('scripts.cogs.custom_commands')
    await bot.load_extension('scripts.cogs.ai_chat')
    print('[v0] All cogs loaded successfully!')

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore command not found errors
    else:
        print(f'[v0] Error: {error}')
        await ctx.send(f"❌ An error occurred: {str(error)}")

# Run the bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print('[v0] ERROR: DISCORD_BOT_TOKEN not found in environment variables!')
    else:
        bot.run(TOKEN)

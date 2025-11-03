import discord
from discord.ext import commands
import json
import os

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_file = 'scripts/custom_commands.json'
        self.custom_commands = self.load_commands()

    def load_commands(self):
        """Load custom commands from file"""
        if os.path.exists(self.commands_file):
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        return {}

    def save_commands(self):
        """Save custom commands to file"""
        with open(self.commands_file, 'w') as f:
            json.dump(self.custom_commands, f, indent=4)

    @commands.command(name='addcmd')
    @commands.has_permissions(manage_guild=True)
    async def addcmd(self, ctx, trigger, *, response):
        """Add a custom command"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.custom_commands:
            self.custom_commands[guild_id] = {}
        
        self.custom_commands[guild_id][trigger] = response
        self.save_commands()
        await ctx.send(f"✅ Custom command `{trigger}` added!")

    @commands.command(name='delcmd')
    @commands.has_permissions(manage_guild=True)
    async def delcmd(self, ctx, trigger):
        """Delete a custom command"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.custom_commands and trigger in self.custom_commands[guild_id]:
            del self.custom_commands[guild_id][trigger]
            self.save_commands()
            await ctx.send(f"✅ Custom command `{trigger}` deleted!")
        else:
            await ctx.send(f"❌ Custom command `{trigger}` not found!")

    @commands.command(name='listcmds')
    async def listcmds(self, ctx):
        """List all custom commands"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.custom_commands or not self.custom_commands[guild_id]:
            return await ctx.send("📝 No custom commands set up yet!")
        
        embed = discord.Embed(title="📝 Custom Commands", color=discord.Color.blue())
        for trigger, response in self.custom_commands[guild_id].items():
            embed.add_field(name=f"!{trigger}", value=response[:100], inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen for custom command triggers"""
        if message.author.bot:
            return
        
        if not message.content.startswith('!'):
            return
        
        guild_id = str(message.guild.id)
        trigger = message.content[1:].split()[0]
        
        if guild_id in self.custom_commands and trigger in self.custom_commands[guild_id]:
            response = self.custom_commands[guild_id][trigger]
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(CustomCommands(bot))

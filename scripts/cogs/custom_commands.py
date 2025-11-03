import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_file = 'scripts/custom_commands.json'
        self.custom_commands = self.load_commands()

    def load_commands(self):
        if os.path.exists(self.commands_file):
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        return {}

    def save_commands(self):
        with open(self.commands_file, 'w') as f:
            json.dump(self.custom_commands, f, indent=4)

    @app_commands.command(name='addcmd', description='Add a custom command')
    @app_commands.describe(trigger='Command trigger word', response='Command response')
    async def addcmd(self, interaction: discord.Interaction, trigger: str, response: str):
        if not interaction.user.guild_permissions.manage_guild:
            return await interaction.response.send_message("❌ You need Manage Server permission!", ephemeral=True)
        
        guild_id = str(interaction.guild.id)
        if guild_id not in self.custom_commands:
            self.custom_commands[guild_id] = {}
        
        self.custom_commands[guild_id][trigger] = response
        self.save_commands()
        await interaction.response.send_message(f"✅ Custom command `{trigger}` added!")

    @app_commands.command(name='delcmd', description='Delete a custom command')
    @app_commands.describe(trigger='Command trigger word to delete')
    async def delcmd(self, interaction: discord.Interaction, trigger: str):
        if not interaction.user.guild_permissions.manage_guild:
            return await interaction.response.send_message("❌ You need Manage Server permission!", ephemeral=True)
        
        guild_id = str(interaction.guild.id)
        if guild_id in self.custom_commands and trigger in self.custom_commands[guild_id]:
            del self.custom_commands[guild_id][trigger]
            self.save_commands()
            await interaction.response.send_message(f"✅ Custom command `{trigger}` deleted!")
        else:
            await interaction.response.send_message(f"❌ Custom command `{trigger}` not found!", ephemeral=True)

    @app_commands.command(name='listcmds', description='List all custom commands')
    async def listcmds(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        if guild_id not in self.custom_commands or not self.custom_commands[guild_id]:
            return await interaction.response.send_message("📝 No custom commands set up yet!")
        
        embed = discord.Embed(title="📝 Custom Commands", color=discord.Color.blue())
        for trigger, response in self.custom_commands[guild_id].items():
            embed.add_field(name=f"/{trigger}", value=response[:100], inline=False)
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
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

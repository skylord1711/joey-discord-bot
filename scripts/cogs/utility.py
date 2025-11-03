import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Check bot latency')
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

    @app_commands.command(name='serverinfo', description='Get server information')
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='userinfo', description='Get user information')
    @app_commands.describe(member='The member to get info about')
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"👤 {member.name}", color=member.color)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Roles", value=len(member.roles) - 1, inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='avatar', description="Get a user's avatar")
    @app_commands.describe(member='The member to get avatar from')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"🖼️ {member.name}'s Avatar", color=member.color)
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='remind', description='Set a reminder')
    @app_commands.describe(minutes='Time in minutes', message='Reminder message')
    async def remind(self, interaction: discord.Interaction, minutes: int, message: str):
        await interaction.response.send_message(f"⏰ I'll remind you in {minutes} minutes: {message}")
        await asyncio.sleep(minutes * 60)
        await interaction.followup.send(f"⏰ {interaction.user.mention} Reminder: {message}")

    @app_commands.command(name='poll', description='Create a poll')
    @app_commands.describe(question='The poll question', options='Options separated by commas (max 10)')
    async def poll(self, interaction: discord.Interaction, question: str, options: str):
        option_list = [opt.strip() for opt in options.split(',')]
        
        if len(option_list) > 10:
            return await interaction.response.send_message("❌ Maximum 10 options allowed!", ephemeral=True)
        if len(option_list) < 2:
            return await interaction.response.send_message("❌ Need at least 2 options!", ephemeral=True)
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = discord.Embed(title=f"📊 {question}", color=discord.Color.blue())
        for i, option in enumerate(option_list):
            embed.add_field(name=f"{reactions[i]} Option {i+1}", value=option, inline=False)
        
        await interaction.response.send_message(embed=embed)
        poll_msg = await interaction.original_response()
        for i in range(len(option_list)):
            await poll_msg.add_reaction(reactions[i])

    @app_commands.command(name='roll', description='Roll dice')
    @app_commands.describe(dice='Dice format (e.g., 2d6)')
    async def roll(self, interaction: discord.Interaction, dice: str = "1d6"):
        try:
            rolls, sides = map(int, dice.split('d'))
            if rolls > 100 or sides > 1000:
                return await interaction.response.send_message("❌ Too many rolls or sides!", ephemeral=True)
            
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            
            await interaction.response.send_message(f"🎲 Rolling {dice}: {results}\n**Total: {total}**")
        except:
            await interaction.response.send_message("❌ Invalid format! Use NdN (e.g., 2d6)", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))

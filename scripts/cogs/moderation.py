import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warned_users = {}

    @app_commands.command(name='kick', description='Kick a member from the server')
    @app_commands.describe(member='The member to kick', reason='Reason for kicking')
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("❌ You don't have permission to kick members!", ephemeral=True)
        
        await member.kick(reason=reason)
        embed = discord.Embed(title="👢 Member Kicked", color=discord.Color.orange())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='ban', description='Ban a member from the server')
    @app_commands.describe(member='The member to ban', reason='Reason for banning')
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("❌ You don't have permission to ban members!", ephemeral=True)
        
        await member.ban(reason=reason)
        embed = discord.Embed(title="🔨 Member Banned", color=discord.Color.red())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unban', description='Unban a user by their ID')
    @app_commands.describe(user_id='The ID of the user to unban')
    async def unban(self, interaction: discord.Interaction, user_id: str):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("❌ You don't have permission to unban members!", ephemeral=True)
        
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"✅ Unbanned {user.name}#{user.discriminator}")

    @app_commands.command(name='mute', description='Timeout a member')
    @app_commands.describe(member='The member to mute', duration='Duration in minutes', reason='Reason for muting')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int = 10, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to mute members!", ephemeral=True)
        
        await member.timeout(timedelta(minutes=duration), reason=reason)
        embed = discord.Embed(title="🔇 Member Muted", color=discord.Color.blue())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unmute', description='Remove timeout from a member')
    @app_commands.describe(member='The member to unmute')
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to unmute members!", ephemeral=True)
        
        await member.timeout(None)
        await interaction.response.send_message(f"✅ {member.mention} has been unmuted!")

    @app_commands.command(name='warn', description='Warn a member')
    @app_commands.describe(member='The member to warn', reason='Reason for warning')
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to warn members!", ephemeral=True)
        
        if member.id not in self.warned_users:
            self.warned_users[member.id] = []
        self.warned_users[member.id].append(reason)
        
        embed = discord.Embed(title="⚠️ Member Warned", color=discord.Color.yellow())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Warnings", value=len(self.warned_users[member.id]), inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='warnings', description='Check warnings for a member')
    @app_commands.describe(member='The member to check warnings for')
    async def warnings(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        warnings = self.warned_users.get(member.id, [])
        
        if not warnings:
            await interaction.response.send_message(f"✅ {member.mention} has no warnings!")
        else:
            embed = discord.Embed(title=f"⚠️ Warnings for {member.name}", color=discord.Color.yellow())
            for i, warning in enumerate(warnings, 1):
                embed.add_field(name=f"Warning {i}", value=warning, inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name='clear', description='Delete messages')
    @app_commands.describe(amount='Number of messages to delete (max 100)')
    async def clear(self, interaction: discord.Interaction, amount: int = 10):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ You don't have permission to manage messages!", ephemeral=True)
        
        amount = min(amount, 100)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🗑️ Deleted {len(deleted)} messages!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    bot.tree.add_command(Moderation(bot).kick)
    bot.tree.add_command(Moderation(bot).ban)
    bot.tree.add_command(Moderation(bot).unban)
    bot.tree.add_command(Moderation(bot).mute)
    bot.tree.add_command(Moderation(bot).unmute)
    bot.tree.add_command(Moderation(bot).warn)
    bot.tree.add_command(Moderation(bot).warnings)
    bot.tree.add_command(Moderation(bot).clear)

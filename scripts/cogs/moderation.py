import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warned_users = {}  # Store warnings

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server"""
        await member.kick(reason=reason)
        embed = discord.Embed(title="👢 Member Kicked", color=discord.Color.orange())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server"""
        await member.ban(reason=reason)
        embed = discord.Embed(title="🔨 Member Banned", color=discord.Color.red())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        """Unban a user by their ID"""
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user.name}#{user.discriminator}")

    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 10, *, reason="No reason provided"):
        """Timeout a member (duration in minutes)"""
        await member.timeout(timedelta(minutes=duration), reason=reason)
        embed = discord.Embed(title="🔇 Member Muted", color=discord.Color.blue())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Remove timeout from a member"""
        await member.timeout(None)
        await ctx.send(f"✅ {member.mention} has been unmuted!")

    @commands.command(name='warn')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member"""
        if member.id not in self.warned_users:
            self.warned_users[member.id] = []
        self.warned_users[member.id].append(reason)
        
        embed = discord.Embed(title="⚠️ Member Warned", color=discord.Color.yellow())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Warnings", value=len(self.warned_users[member.id]), inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='warnings')
    async def warnings(self, ctx, member: discord.Member = None):
        """Check warnings for a member"""
        member = member or ctx.author
        warnings = self.warned_users.get(member.id, [])
        
        if not warnings:
            await ctx.send(f"✅ {member.mention} has no warnings!")
        else:
            embed = discord.Embed(title=f"⚠️ Warnings for {member.name}", color=discord.Color.yellow())
            for i, warning in enumerate(warnings, 1):
                embed.add_field(name=f"Warning {i}", value=warning, inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Delete messages (default 10, max 100)"""
        amount = min(amount, 100)
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🗑️ Deleted {len(deleted) - 1} messages!")
        await msg.delete(delay=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

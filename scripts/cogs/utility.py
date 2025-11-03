import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """Get server information"""
        guild = ctx.guild
        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get user information"""
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member.name}", color=member.color)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Roles", value=len(member.roles) - 1, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Get user's avatar"""
        member = member or ctx.author
        embed = discord.Embed(title=f"🖼️ {member.name}'s Avatar", color=member.color)
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='remind')
    async def remind(self, ctx, time: int, *, message):
        """Set a reminder (time in minutes)"""
        await ctx.send(f"⏰ I'll remind you in {time} minutes: {message}")
        await asyncio.sleep(time * 60)
        await ctx.send(f"⏰ {ctx.author.mention} Reminder: {message}")

    @commands.command(name='poll')
    async def poll(self, ctx, question, *options):
        """Create a poll (max 10 options)"""
        if len(options) > 10:
            return await ctx.send("❌ Maximum 10 options allowed!")
        if len(options) < 2:
            return await ctx.send("❌ Need at least 2 options!")
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = discord.Embed(title=f"📊 {question}", color=discord.Color.blue())
        for i, option in enumerate(options):
            embed.add_field(name=f"{reactions[i]} Option {i+1}", value=option, inline=False)
        
        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(reactions[i])

    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message):
        """Make the bot say something"""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='embed')
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, title, *, description):
        """Create an embed message"""
        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
        embed.set_footer(text=f"Created by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name='roll')
    async def roll(self, ctx, dice: str = "1d6"):
        """Roll dice (format: NdN, e.g., 2d6)"""
        try:
            rolls, sides = map(int, dice.split('d'))
            if rolls > 100 or sides > 1000:
                return await ctx.send("❌ Too many rolls or sides!")
            
            import random
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            
            await ctx.send(f"🎲 Rolling {dice}: {results}\n**Total: {total}**")
        except:
            await ctx.send("❌ Invalid format! Use NdN (e.g., 2d6)")

async def setup(bot):
    await bot.add_cog(Utility(bot))

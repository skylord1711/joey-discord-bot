import discord
from discord.ext import commands

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channels = {}  # Store welcome channel IDs per guild

    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel = None):
        """Set the welcome channel"""
        channel = channel or ctx.channel
        self.welcome_channels[ctx.guild.id] = channel.id
        await ctx.send(f"✅ Welcome channel set to {channel.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Welcome new members"""
        guild = member.guild
        
        # Check if welcome channel is set
        if guild.id not in self.welcome_channels:
            return
        
        channel = guild.get_channel(self.welcome_channels[guild.id])
        if not channel:
            return
        
        # Create welcome embed
        embed = discord.Embed(
            title="👋 Welcome to the server!",
            description=f"Hey {member.mention}, welcome to **{guild.name}**!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Member Count", value=f"You are member #{guild.member_count}!", inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.set_footer(text=f"ID: {member.id}")
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Say goodbye to leaving members"""
        guild = member.guild
        
        if guild.id not in self.welcome_channels:
            return
        
        channel = guild.get_channel(self.welcome_channels[guild.id])
        if not channel:
            return
        
        embed = discord.Embed(
            title="👋 Goodbye!",
            description=f"**{member.name}** has left the server.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Member Count", value=f"We now have {guild.member_count} members.", inline=False)
        
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcomer(bot))

import discord
from discord import app_commands
from discord.ext import commands

class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channels = {}
        self.welcome_images = {}

    @app_commands.command(name="setwelcome", description="Set the welcome channel")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setwelcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the welcome channel"""
        self.welcome_channels[interaction.guild.id] = channel.id
        await interaction.response.send_message(f"✅ Welcome channel set to {channel.mention}!", ephemeral=True)

    @app_commands.command(name="setwelcomeimage", description="Set the custom welcome image URL")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setwelcomeimage(self, interaction: discord.Interaction, image_url: str):
        """Set the custom welcome image"""
        self.welcome_images[interaction.guild.id] = image_url
        await interaction.response.send_message(f"✅ Welcome image set! Use /testwelcome to preview.", ephemeral=True)

    @app_commands.command(name="testwelcome", description="Test the welcome message")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def testwelcome(self, interaction: discord.Interaction):
        """Test the welcome message with your own user"""
        await interaction.response.defer(ephemeral=True)
        
        if interaction.guild.id not in self.welcome_channels:
            await interaction.followup.send("❌ Please set a welcome channel first with /setwelcome", ephemeral=True)
            return
        
        channel = interaction.guild.get_channel(self.welcome_channels[interaction.guild.id])
        if not channel:
            await interaction.followup.send("❌ Welcome channel not found!", ephemeral=True)
            return
        
        embed = self._create_welcome_embed(interaction.user, interaction.guild)
        await channel.send(embed=embed)
        await interaction.followup.send(f"✅ Test welcome message sent to {channel.mention}!", ephemeral=True)

    def _create_welcome_embed(self, member: discord.Member, guild: discord.Guild):
        """Create the custom welcome embed matching the user's design"""
        embed = discord.Embed(
            title="# • Welcome to Joeys Server!",
            description=(
                f"Hey there {member.mention} — welcome to the community! 👋❤️ We're thrilled to have you join us.\n\n"
                f"🤝 **Take a moment to introduce yourself!**\n"
                f"Share a little about yourself — your hobbies, interests, or what brought you to this server!\n\n"
                f"📜 **Before diving in, please check out our server rules.**\n"
                f"They help keep the vibe positive and fun for everyone. You can find them here: <#rules>\n\n"
                f"🎉 **We're super excited to have you with us and can't wait to get to know you better.**\n"
                f"Enjoy your stay and make yourself at home!"
            ),
            color=0x2B2D31  # Dark gray to match Discord's dark theme
        )
        
        if guild.id in self.welcome_images:
            embed.set_image(url=self.welcome_images[guild.id])
        
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Welcome new members with custom message"""
        guild = member.guild
        
        # Check if welcome channel is set
        if guild.id not in self.welcome_channels:
            return
        
        channel = guild.get_channel(self.welcome_channels[guild.id])
        if not channel:
            return
        
        embed = self._create_welcome_embed(member, guild)
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

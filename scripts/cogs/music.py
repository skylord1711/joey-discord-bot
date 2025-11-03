import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import asyncio

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    def get_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    @app_commands.command(name='join', description='Join your voice channel')
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message("❌ You need to be in a voice channel!", ephemeral=True)
        
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"🎵 Joined {channel.name}!")

    @app_commands.command(name='play', description='Play a song from YouTube')
    @app_commands.describe(url='YouTube URL or search query')
    async def play(self, interaction: discord.Interaction, url: str):
        if not interaction.guild.voice_client:
            if not interaction.user.voice:
                return await interaction.response.send_message("❌ You need to be in a voice channel!", ephemeral=True)
            await interaction.user.voice.channel.connect()

        await interaction.response.defer()
        
        try:
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            
            if interaction.guild.voice_client.is_playing():
                self.get_queue(interaction.guild.id).append(player)
                await interaction.followup.send(f"📝 Added to queue: **{player.title}**")
            else:
                interaction.guild.voice_client.play(player, after=lambda e: self.play_next(interaction))
                await interaction.followup.send(f"🎵 Now playing: **{player.title}**")
        except Exception as e:
            await interaction.followup.send(f"❌ Error playing song: {str(e)}")

    def play_next(self, interaction):
        queue = self.get_queue(interaction.guild.id)
        if queue:
            player = queue.pop(0)
            interaction.guild.voice_client.play(player, after=lambda e: self.play_next(interaction))

    @app_commands.command(name='pause', description='Pause the current song')
    async def pause(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("⏸️ Paused!")
        else:
            await interaction.response.send_message("❌ Nothing is playing!", ephemeral=True)

    @app_commands.command(name='resume', description='Resume the paused song')
    async def resume(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("▶️ Resumed!")
        else:
            await interaction.response.send_message("❌ Nothing is paused!", ephemeral=True)

    @app_commands.command(name='skip', description='Skip the current song')
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("⏭️ Skipped!")
        else:
            await interaction.response.send_message("❌ Nothing is playing!", ephemeral=True)

    @app_commands.command(name='stop', description='Stop playing and clear the queue')
    async def stop(self, interaction: discord.Interaction):
        self.queue[interaction.guild.id] = []
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("⏹️ Stopped and cleared queue!")
        else:
            await interaction.response.send_message("❌ Nothing is playing!", ephemeral=True)

    @app_commands.command(name='leave', description='Leave the voice channel')
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("👋 Left the voice channel!")
        else:
            await interaction.response.send_message("❌ Not in a voice channel!", ephemeral=True)

    @app_commands.command(name='queue', description='Show the current music queue')
    async def show_queue(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild.id)
        if not queue:
            return await interaction.response.send_message("📝 Queue is empty!")
        
        embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
        for i, player in enumerate(queue, 1):
            embed.add_field(name=f"{i}.", value=player.title, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='volume', description='Change the player volume')
    @app_commands.describe(volume='Volume level (0-100)')
    async def volume(self, interaction: discord.Interaction, volume: int):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message("❌ Not connected to a voice channel!", ephemeral=True)
        
        if volume < 0 or volume > 100:
            return await interaction.response.send_message("❌ Volume must be between 0 and 100!", ephemeral=True)
        
        interaction.guild.voice_client.source.volume = volume / 100
        await interaction.response.send_message(f"🔊 Volume set to {volume}%")

async def setup(bot):
    await bot.add_cog(Music(bot))

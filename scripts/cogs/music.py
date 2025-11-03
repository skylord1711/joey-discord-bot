import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Suppress noise about console usage from errors
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

    @commands.command(name='join')
    async def join(self, ctx):
        """Join your voice channel"""
        if not ctx.author.voice:
            return await ctx.send("❌ You need to be in a voice channel!")
        
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🎵 Joined {channel.name}!")

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        """Play a song from YouTube"""
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            
            if ctx.voice_client.is_playing():
                self.get_queue(ctx.guild.id).append(player)
                await ctx.send(f"📝 Added to queue: **{player.title}**")
            else:
                ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
                await ctx.send(f"🎵 Now playing: **{player.title}**")

    def play_next(self, ctx):
        """Play the next song in queue"""
        queue = self.get_queue(ctx.guild.id)
        if queue:
            player = queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused!")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the paused song"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed!")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped!")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop playing and clear the queue"""
        self.queue[ctx.guild.id] = []
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("⏹️ Stopped and cleared queue!")

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Leave the voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Left the voice channel!")

    @commands.command(name='queue')
    async def show_queue(self, ctx):
        """Show the current queue"""
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            return await ctx.send("📝 Queue is empty!")
        
        embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
        for i, player in enumerate(queue, 1):
            embed.add_field(name=f"{i}.", value=player.title, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        """Change the player volume (0-100)"""
        if not ctx.voice_client:
            return await ctx.send("❌ Not connected to a voice channel!")
        
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"🔊 Volume set to {volume}%")

async def setup(bot):
    await bot.add_cog(Music(bot))

import discord
from discord.ext import commands
from gtts import gTTS
import yt_dlp
import asyncio
import os
import tempfile
from cogs.ui import MusicControls

yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {'options': '-vn'}

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {}

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = asyncio.Queue()
        return self.queues[guild_id]

    async def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        if queue.empty():
            return
        url, title = await queue.get()
        await self._play_url(ctx, url)

    async def _play_url(self, ctx, url):
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            title = data.get('title', url)
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice = ctx.guild.voice_client

            def after_play(e):
                asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop)

            voice.play(player, after=after_play)
            embed = discord.Embed(title="🎵 Reproduciendo", description=f"**{title}**", color=0xff8c00)
            await ctx.send(embed=embed, view=MusicControls(ctx))
        except Exception as e:
            print(e)
            await ctx.send("Error al reproducir la canción.")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.reply(f'Conectado exitosamente al canal: {channel}')
        else:
            await ctx.reply('Debes estar en un canal para poder conectarme.')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply("Me he desconectado del canal correctamente.")
        else:
            await ctx.reply("No estoy en ningun canal.")

    @commands.command()
    async def tts(self, ctx, *, text: str):
        if not ctx.author.voice:
            await ctx.send("Debes estar en un canal de voz para usar el comando TTS.")
            return
        voice = ctx.guild.voice_client
        channel = ctx.author.voice.channel
        if voice is None:
            voice = await channel.connect()
        elif voice.channel != channel:
            await ctx.send(f"El bot ya está en {voice.channel.name}.")
            return
        tts = gTTS(text=text, lang='es')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
        voice.play(discord.FFmpegPCMAudio(tmpfile.name), after=lambda e: os.remove(tmpfile.name))
        await ctx.reply("Enviando mensaje de voz...")

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            await ctx.reply("Debes estar en un canal de voz.")
            return
        voice = ctx.guild.voice_client
        if voice is None:
            await ctx.author.voice.channel.connect()
            voice = ctx.guild.voice_client

        queue = self.get_queue(ctx.guild.id)

        if not query.startswith("http"):
            query = f"ytsearch:{query}"

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        title = data.get('title', query)
        url = data['webpage_url']

        if voice.is_playing() or voice.is_paused():
            await queue.put((url, title))
            await ctx.reply(f"Agregado a la cola: **{title}**")
        else:
            await self._play_url(ctx, url)

    @commands.command()
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.pause()
            await ctx.reply("Musica Pausada.")
        else:
            await ctx.reply("No se esta reproduciendo nada para pausar.")

    @commands.command()
    async def resume(self, ctx):
        voice = ctx.guild.voice_client
        if voice and voice.is_paused():
            voice.resume()
            await ctx.reply("Reproduciendo nuevamente . . .")
        else:
            await ctx.reply("No hay nada pausado.")

    @commands.command()
    async def stop(self, ctx):
        voice = ctx.guild.voice_client
        if voice and voice.is_playing():
            self.queues.pop(ctx.guild.id, None)
            voice.stop()
            await ctx.reply("Cancion detenida y cola limpiada.")
        else:
            await ctx.reply("No hay nada que detener.")

    @commands.command()
    async def skip(self, ctx):
        voice = ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.stop()
            await ctx.reply("Canción saltada.")
        else:
            await ctx.reply("No hay nada reproduciéndose.")

    @commands.command()
    async def queue(self, ctx):
        q = self.get_queue(ctx.guild.id)
        items = list(q._queue)
        if not items:
            await ctx.reply("La cola está vacía.")
        else:
            lista = "\n".join(f"{i+1}. **{title}**" for i, (url, title) in enumerate(items))
            await ctx.reply(f"**Cola:**\n{lista}")

async def setup(client):
    await client.add_cog(Music(client))
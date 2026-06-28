import discord
from discord.ext import commands
from gtts import gTTS
import yt_dlp
import asyncio
import os
import tempfile

yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {'options': '-vn'}

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

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
    async def play(self, ctx, url: str):
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice = ctx.guild.voice_client
            voice.play(player)
            await ctx.reply("Reproduciendo . .")
        except Exception as e:
            print(e)

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
            voice.stop()
            await ctx.reply("Cancion detenida correctamente.")
        else:
            await ctx.reply("No hay nada que detener.")

async def setup(client):
    await client.add_cog(Music(client))
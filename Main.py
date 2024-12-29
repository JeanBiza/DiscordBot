import discord
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
import yt_dlp
import asyncio
import random
import yaml
import os
import tempfile
import webserver


#yt_dl
yt_dl_options = {"format" : "bestaudio/best",
                 "cookies": "cookies.txt"
                }
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {'options' : '-vn'}

#discord
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
token = config["discord_token"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
prefix = "$"
client = commands.Bot(command_prefix=prefix,intents=intents, help_command=None)
voice_client = None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command(pass_context = True)
async def help(ctx, categoria:str = None):
    categorias = ["voz", "configuracion", "interaccion", "entretencion"]
    prefix = client.command_prefix

    embed_principal = discord.Embed(
        title=" Comandos ",
        description="Estos son los comandos disponibles del bot"
    )
    embed_principal.add_field(name="", value="", inline=False)
    embed_principal.add_field(name="Prefijo del servidor", value=prefix, inline=False)
    embed_principal.add_field(name="", value="", inline=False)


    embed_voz = discord.Embed(
        title="Categoria : Voz",
        description="Comandos para el chat de voz"
    )
    embed_voz.add_field(name="", value="", inline=False)
    embed_voz.add_field(name="join", value="Entrar a un canal de voz", inline=True)
    embed_voz.add_field(name="leave", value="Salir de un canal de voz", inline=True)
    embed_voz.add_field(name="tts", value="Envia un mensaje por voz", inline=True)
    embed_voz.add_field(name="play", value="Reproduce una canción (URL de YouTube)", inline=True)
    embed_voz.add_field(name="pause", value="Pausa la canción actual", inline=True)
    embed_voz.add_field(name="resume", value="Reanuda la canción actual", inline=True)
    embed_voz.add_field(name="stop", value="Detiene la música actual", inline=True)
    embed_voz.add_field(name="", value="", inline=False)


    embed_configuracion = discord.Embed(
        title="Categoria : Configuracion",
        description="Comandos de configuracion del servidor"
    )
    embed_configuracion.add_field(name="", value="", inline=False)
    embed_configuracion.add_field(name="help", value="Muestra todos los comandos", inline=True)
    embed_configuracion.add_field(name="prefix", value="Cambia el prefijo de los comandos", inline=True)
    embed_configuracion.add_field(name="", value="", inline=False)
    

    embed_interaccion = discord.Embed(
        title="Categoria : Configuracion",
        description="Comandos de interaccion"
    )
    embed_interaccion.add_field(name="", value="", inline=False)
    embed_interaccion.add_field(name="hi", value="Quieres un saludo?", inline=True)
    embed_interaccion.add_field(name="avatar", value="Mira el avatar de algun usuario", inline=True)
    embed_interaccion.add_field(name="", value="", inline=False)


    embed_entretencion = discord.Embed(
        title="Categoria : Entretencion",
        description="Comandos de Entretenimiento"
    ) 
    embed_entretencion.add_field(name="", value="", inline=False)
    embed_entretencion.add_field(name="rps", value="Piedra, Papel o Tijera", inline=True)
    embed_entretencion.add_field(name="dice", value="Tira el dado", inline=True)
    embed_entretencion.add_field(name="", value="", inline=False)

    if categoria is None:
            await ctx.send(embed=embed_principal)
            await ctx.send(embed=embed_configuracion)
            await ctx.send(embed=embed_interaccion)
            await ctx.send(embed=embed_voz)
            await ctx.send(embed=embed_entretencion)
    else:
        if any(categoria.lower().startswith(c) for c in categorias):
            
            if categoria.lower().startswith("config"):
                await ctx.send(embed=embed_principal)
                await ctx.send(embed=embed_configuracion)

            if categoria.lower().startswith("inter"):
                await ctx.send(embed=embed_principal)
                await ctx.send(embed=embed_interaccion)

            if categoria.lower().startswith("vo"):
                await ctx.send(embed=embed_principal)
                await ctx.send(embed=embed_voz)

            if categoria.lower().startswith("entre"):
                await ctx.send(embed=embed_principal)
                await ctx.send(embed=embed_entretencion)

        else:
            await ctx.reply("Ingrese una categoría válida: voz, configuracion, interaccion, entretencion.")


#Comando para saludar
@client.command(pass_context = True)
async def hi(ctx, usuario: discord.User = None):
    if usuario is None:
        await ctx.reply("Hola!")
    else:
        await ctx.send(f'Hola {usuario.mention}!')

#Comando para cambiar el prefijo
@client.command(pass_context = True)
async def prefix(ctx, prefix:str):
    if len(prefix) == 1:
        client.command_prefix = prefix
        await ctx.reply(f'Prefijo cambiado exitosamente a {prefix}')
    else:
        await ctx.reply(f'Usa solo un caracter para el prefijo (Si es posible un simbolo, para no interrumpir con chat)')

#Comando para entrar a un canal de voz
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.reply(f'Conectado exitosamente al canal: {channel}')
    else:
        await ctx.reply(f'Debes estar en un canal para poder conectarme.')


#Cmando para salir de un canal de voz
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.reply("Me he desconectado del canal correctamente.")
    else:
        await ctx.reply("No estoy en ningun canal.")

#comando para tts
@client.command(pass_context = True)
async def tts(ctx, *, text: str):
    global voice_client

    if voice_client and voice_client.is_connected():
        if voice_client.channel != ctx.author.voice.channel:
            await ctx.send(f"El bot ya está en el canal de voz {voice_client.channel.name}. No puede cambiar de canal.")
            return

    if ctx.author.voice:
        channel = ctx.author.voice.channel
        
        if voice_client is None or not voice_client.is_connected():
            voice_client = await channel.connect()
        
        tts = gTTS(text=text, lang='es')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)

        voice_client.play(discord.FFmpegPCMAudio(tmpfile.name), after=lambda e: print('Reproducción finalizada'))

        while voice_client.is_playing():
            await asyncio.sleep(1)

        os.remove(tmpfile.name)
    else:
        await ctx.send("Debes estar en un canal de voz para usar el comando TTS.")


#Comando para reproducir una cancion
@client.command(pass_context = True)
async def play(ctx, url:str):
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda : ytdl.extract_info(url, download=False))
        song = data['url']
        player = discord.FFmpegPCMAudio(song, executable='C:/ffmpeg/ffmpeg.exe', **ffmpeg_options)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(player)
        await ctx.reply("Reproduciendo . .")
    except Exception as e:
        print(e)

#Comando para pausar musica
@client.command(pass_context = True)
async def pause(ctx):
    voz = get(client.voice_clients,guild=ctx.guild)
    if voz and voz.is_playing():
        print("Musica pausada")
        voz.pause()
        await ctx.reply("Musica Pausada.")
    else:
        await ctx.reply("No se esta reproduciendo nada para pausar.")

#comando para continuar musica
@client.command(pass_context = True)
async def resume(ctx):
    voz = get(client.voice_clients,guild=ctx.guild)
    if voz and voz.is_paused():
        print("Reproduciendo nuevamente")
        voz.resume()
        await ctx.reply("Reproduciendo nuevamente . . .")
    else:
        await ctx.reply("No hay nada pausado.")

#comando para detener musica
@client.command(pass_context = True)
async def stop(ctx):
    voz = get(client.voice_clients,guild=ctx.guild)
    if voz and voz.is_playing():
        print("Cancion detenida.")
        voz.stop()
        await ctx.reply("Cancion detenida correctamente.")
    else:
        await ctx.reply("No hay nada que detener.")

#Comando para tirar el dado
@client.command(pass_context = True)
async def dice(ctx):
    numero = random.randint(1,6)
    await ctx.reply("Girando el dado . . .")
    await ctx.send(f'Ha salido el numero: {numero}.')

#comando para piedra, papel o tijeras
@client.command(pass_context = True)
async def rps(ctx, eleccion:str):
    ppt = ["piedra","papel","tijeras"]
    if eleccion in ppt:
        eleccion_bot = random.choice(ppt)

        if eleccion == "piedra":
            if eleccion_bot == "piedra":
                await ctx.reply("He elegido Piedra, es un empate!")
            if eleccion_bot == "papel":
                await ctx.reply("He elegido Papel, Has perdido!")
            if eleccion_bot == "tijeras":
                await ctx.reply("He elegido Tijeras, Has ganado!")

        if eleccion == "papel":
            if eleccion_bot == "piedra":
                await ctx.reply("He elegido Piedra, Has ganado!")
            if eleccion_bot == "papel":
                await ctx.reply("He elegido Papel, Es un empate!")
            if eleccion_bot == "tijeras":
                await ctx.reply("He elegido Tijeras, Has perdido!")
    
        if eleccion == "tijeras":
            if eleccion_bot == "piedra":
                await ctx.reply("He elegido Piedra, Has perdido!")
            if eleccion_bot == "papel":
                await ctx.reply("He elegido Papel, Has ganado!")
            if eleccion_bot == "tijeras":
                await ctx.reply("He elegido Tijeras, Es un empate.")
    else:
        await ctx.reply(f'Usa el comando correctamente! (Ejemplo: rps papel)')


#comando para enviar avatar de usuario
@client.command(pass_context = True)
async def avatar(ctx, usuario: discord.User = None):
    if usuario is None:
        usuario = ctx.author

    await ctx.reply(f'Avatar del usuario {usuario.mention}:')
    await ctx.send(f'{usuario.avatar.url}')


#Evento de bienvenida al usuario
@client.event
async def on_member_join(member):
    id_canal = 1322320350155112448
    canal = await member.guild.fetch_channel(id_canal)
    await canal.send(f'Bienvenid@ al servidor, humano estupido! {member.mention}')




webserver.keep_alive()
client.run(token)

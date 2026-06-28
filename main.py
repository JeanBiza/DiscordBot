import discord
from discord.ext import commands
import os
import shutil
import webserver
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="$", intents=intents, help_command=None)

@client.event
async def on_ready():
    await client.load_extension("cogs.fun")
    await client.load_extension("cogs.config")
    await client.load_extension("cogs.music")
    if not shutil.which("ffmpeg"):
        print("WARNING: ffmpeg no encontrado. Los comandos de voz no funcionarán.")
    print(f'We have logged in as {client.user}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Comando no encontrado. Usa `{client.command_prefix}help` para ver los comandos disponibles.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Faltan argumentos. Usa `{client.command_prefix}help` para más información.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("No tienes permisos para usar este comando.")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Argumento inválido. Revisa el comando e intenta de nuevo.")
    else:
        print(f"Error no manejado: {error}")

webserver.keep_alive()
client.run(token)
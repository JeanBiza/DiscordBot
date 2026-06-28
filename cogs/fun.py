import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Comando para saludar
    @commands.command()
    async def hi(self, ctx, usuario: discord.User = None):
        if usuario is None:
            await ctx.reply("Hola!")
        else:
            await ctx.send(f'Hola {usuario.mention}!')

    #Comando para tirar el dado
    @commands.command()
    async def dice(self, ctx):
        numero = random.randint(1,6)
        await ctx.reply("Girando el dado . . .")
        await ctx.send(f'Ha salido el numero: {numero}.')

    #comando para piedra, papel o tijeras
    @commands.command()
    async def rps(self, ctx, eleccion:str):
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
    @commands.command()
    async def avatar(self, ctx, usuario: discord.User = None):
        if usuario is None:
            usuario = ctx.author

        await ctx.reply(f'Avatar del usuario {usuario.mention}:')
        await ctx.send(f'{usuario.avatar.url}')

async def setup(client):
    await client.add_cog(Fun(client))
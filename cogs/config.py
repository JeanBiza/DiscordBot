import discord
from discord.ext import commands
import database

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, categoria:str = None):
        categorias = ["voz", "configuracion", "interaccion", "entretencion"]
        prefix = self.client.command_prefix

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


    #Comando para cambiar el prefijo
    @commands.command()
    async def prefix(self, ctx, prefix:str):
        if len(prefix) == 1:
            self.client.command_prefix = prefix
            await ctx.reply(f'Prefijo cambiado exitosamente a {prefix}')
        else:
            await ctx.reply(f'Usa solo un caracter para el prefijo (Si es posible un simbolo, para no interrumpir con chat)')

    #Comando para definir canal de bienvenida
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, canal: discord.TextChannel):
        database.set_welcome_channel(ctx.guild.id, canal.id)
        await ctx.reply(f'Canal de bienvenida configurado en {canal.mention}')

    #Evento de bienvenida al usuario
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = database.get_welcome_channel(member.guild.id)
        if channel_id is None:
            return
        canal = member.guild.get_channel(channel_id)
        if canal:
            await canal.send(f'Bienvenid@ al servidor! {member.mention}')


async def setup(client):
    await client.add_cog(Config(client))
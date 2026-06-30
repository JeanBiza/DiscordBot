import discord
from discord.ext import commands
import database

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        prefix = self.client.command_prefix

        embed = discord.Embed(
            title="Comandos del bot",
            description=f"Prefijo actual: `{prefix}`",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Música/Voz",
            value=(
                f"`{prefix}join` `{prefix}leave` `{prefix}play <url/búsqueda>`\n"
                f"`{prefix}pause` `{prefix}resume` `{prefix}stop`\n"
                f"`{prefix}skip` `{prefix}queue` `{prefix}tts <texto>`"
            ),
            inline=False
        )

        embed.add_field(
            name="Entretenimiento",
            value=f"`{prefix}rps <piedra/papel/tijeras>` `{prefix}dice`",
            inline=False
        )

        embed.add_field(
            name="Interacción",
            value=f"`{prefix}hi` `{prefix}avatar [@usuario]`",
            inline=False
        )

        embed.add_field(
            name="Configuración",
            value=f"`{prefix}prefix <símbolo>` `{prefix}setwelcome #canal`",
            inline=False
        )

        embed.add_field(
            name="Moderación",
            value=(
                f"`{prefix}kick @usuario` `{prefix}ban @usuario` `{prefix}unban <id>` `{prefix}banlist`\n"
                f"`{prefix}mute @usuario [min]` `{prefix}unmute @usuario` `{prefix}purge <n>`\n"
                f"`{prefix}warn @usuario` `{prefix}warnings @usuario` `{prefix}clearwarns @usuario`"
            ),
            inline=False
        )

        embed.set_footer(text="Usa los comandos con el prefijo correspondiente")

        await ctx.send(embed=embed)

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
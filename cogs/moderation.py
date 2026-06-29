import discord
from discord.ext import commands
import datetime
import asyncio
import database

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, usuario: discord.Member, *, razon: str = "Sin razón especificada"):
        await usuario.kick(reason=razon)
        await ctx.reply(f"**{usuario}** ha sido expulsado. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, usuario: discord.Member, *, razon: str = "Sin razón especificada"):
        await usuario.ban(reason=razon)
        await ctx.reply(f"**{usuario}** ha sido baneado. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            user = await self.client.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.reply(f"**{user}** ha sido desbaneado.")
        except discord.NotFound:
            await ctx.reply("No se encontró ese usuario o no está baneado.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        bans = [entry async for entry in ctx.guild.bans()]
        if not bans:
            await ctx.reply("No hay usuarios baneados.")
            return
        lista = "\n".join(f"- **{entry.user}** (ID: `{entry.user.id}`)" for entry in bans)
        embed = discord.Embed(title="Lista de bans", description=lista, color=discord.Color.red())
        await ctx.reply(embed=embed, ephemeral=True)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, usuario: discord.Member, minutos: int = 10, *, razon: str = "Sin razón especificada"):
        duracion = datetime.timedelta(minutes=minutos)
        await usuario.timeout(duracion, reason=razon)
        await ctx.reply(f"**{usuario}** ha sido silenciado por {minutos} minutos. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, usuario: discord.Member):
        await usuario.timeout(None)
        await ctx.reply(f"**{usuario}** ha sido desilenciado.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, cantidad: int):
        if cantidad <= 0:
            await ctx.reply("Ingresa un número mayor a 0.")
            return
        await ctx.message.delete()
        borrados = await ctx.channel.purge(limit=cantidad)
        msg = await ctx.send(f"Se eliminaron **{len(borrados)}** mensajes.")
        await asyncio.sleep(3)
        await msg.delete()
    
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, usuario: discord.Member, *, razon: str = "Sin razón especificada"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        database.add_warning(ctx.guild.id, usuario.id, ctx.author.id, razon, timestamp)
        await ctx.reply(f"**{usuario}** ha recibido una advertencia. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx, usuario: discord.Member):
        rows = database.get_warnings(ctx.guild.id, usuario.id)
        if not rows:
            await ctx.reply(f"**{usuario}** no tiene advertencias.")
            return
        lista = "\n".join(
            f"- {ts} | Mod: <@{mod_id}> | Razón: {reason}"
            for mod_id, reason, ts in rows
        )
        embed = discord.Embed(
            title=f"Advertencias de {usuario}",
            description=lista,
            color=discord.Color.orange()
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def clearwarns(self, ctx, usuario: discord.Member):
        database.clear_warnings(ctx.guild.id, usuario.id)
        await ctx.reply(f"Se eliminaron todas las advertencias de **{usuario}**.")

async def setup(client):
    await client.add_cog(Moderation(client))
import discord

class MusicControls(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice = self.ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.pause()
            await interaction.response.send_message("Música pausada.", ephemeral=True)
        else:
            await interaction.response.send_message("No hay nada reproduciéndose.", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.success)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice = self.ctx.guild.voice_client
        if voice and voice.is_paused():
            voice.resume()
            await interaction.response.send_message("Reproduciendo nuevamente.", ephemeral=True)
        else:
            await interaction.response.send_message("No hay nada pausado.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice = self.ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.stop()
            await interaction.response.send_message("Canción saltada.", ephemeral=True)
        else:
            await interaction.response.send_message("No hay nada reproduciéndose.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice = self.ctx.guild.voice_client
        if voice:
            await voice.disconnect()
            await interaction.response.send_message("Detenido y desconectado.", ephemeral=True)
        else:
            await interaction.response.send_message("No estoy en ningún canal.", ephemeral=True)
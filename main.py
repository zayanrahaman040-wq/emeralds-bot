import discord
from discord.ext import commands
import os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
in_servizio = {}

class PannelloView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    def get_embed(self):
        embed = discord.Embed(title="EMERALS RP · Turni staff", description="Premi un pulsante qui sotto per entrare o uscire dal servizio.", color=0x2b2d31)
        if in_servizio:
            lista = ""
            for uid, (nome, inizio) in in_servizio.items():
                sec = int((datetime.now() - inizio).total_seconds())
                m, s = divmod(sec, 60)
                h, m = divmod(m, 60)
                lista += f"• <@{uid}> - in servizio da {h}h {m}m {s}s\n"
            embed.add_field(name=f"In servizio ora ({len(in_servizio)}):", value=lista, inline=False)
        else:
            embed.add_field(name="In servizio ora (0):", value="Nessuno in servizio.", inline=False)
        embed.set_image(url="https://i.imgur.com/exemplo.png")
        return embed
    @discord.ui.button(label="Entra in servizio", style=discord.ButtonStyle.green, custom_id="entra_servizio")
    async def entra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        uid = interaction.user.id
        if uid in in_servizio:
            await interaction.followup.send("Sei già in servizio!", ephemeral=True)
            return
        in_servizio[uid] = (str(interaction.user), datetime.now())
        await interaction.message.edit(embed=self.get_embed(), view=self)
        await interaction.followup.send(f"**Turno iniziato**\n<@{uid}> ha iniziato il turno alle {datetime.now().strftime('%H:%M')}.", ephemeral=True)
    @discord.ui.button(label="Fuori servizio", style=discord.ButtonStyle.red, custom_id="esci_servizio")
    async def esci(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        uid = interaction.user.id
        if uid not in in_servizio:
            await interaction.followup.send("Non sei in servizio!", ephemeral=True)
            return
        del in_servizio[uid]
        await interaction.message.edit(embed=self.get_embed(), view=self)
        await interaction.followup.send(f"**Turno finito**\n<@{uid}> ha finito il turno alle {datetime.now().strftime('%H:%M')}.", ephemeral=True)

@bot.command()
async def pannello(ctx):
    await ctx.send(embed=PannelloView().get_embed(), view=PannelloView())

@bot.event
async def on_ready():
    bot.add_view(PannelloView())
    print(f"Bot online come {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))

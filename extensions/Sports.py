import discord, os
from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv

load_dotenv()
OPENAPI_KEY = os.environ.get("OPENAPI_KEY")

class Sports(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="player-stats" , description="Command to show stats of a player")
    async def player_stats(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.send_message(content=f"You requested stats of {player_name}")

    @app_commands.command(name="player-performance" , description="Command to show performance of a player")
    async def player_performance(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.send_message(content=f"You requested performance of {player_name}")

    @app_commands.command(name="team-stats" , description="Command to show stats of a team")
    async def team_stats(self, interaction: discord.Interaction, team_name: str):
        await interaction.response.send_message(content=f"You requested stats of {team_name}")

    @app_commands.command(name="team-performance" , description="Command to show performance of a team")
    async def team_performance(self, interaction: discord.Interaction, team_name: str):
        await interaction.response.send_message(content=f"You requested performance of {team_name}")

    @app_commands.command(name="which-picks" , description="Command to choose a team that might win based on factual information and stats")
    async def which_picks(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(content=f"You requested which team might win based on {prompt}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Sports(bot))

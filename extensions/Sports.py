import discord, os
from discord.ext import commands
from discord import app_commands

from models.Sports import TeamStatListModel
from models.Sports import PlayerStatListModel

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAPI_KEY = os.environ.get("OPENAPI_KEY")

class Sports(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="player-stats" , description="Command to show stats of a player")
    async def player_stats(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.send_message(content=f"Please wait loading player stats...")

        client = OpenAI(api_key=OPENAPI_KEY)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful sports expert. Give me stats of this user."},
                {"role": "user", "content": player_name}
            ],
            response_format=PlayerStatListModel
        )

        all_stats = completion.choices[0].message.parsed.all_stats
        player_name = completion.choices[0].message.parsed.player_name
        sports_name = completion.choices[0].message.parsed.sports_name

        embed = discord.Embed(title="Player Statistics" , color=discord.Color.blurple())
        embed.set_footer(text=f"{interaction.user.id} | {interaction.user.name}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Player Name", value=player_name, inline=False)
        embed.add_field(name="Sports Name", value=sports_name, inline=False)
        for stat in all_stats:
            embed.add_field(name=stat.stat_name , value=stat.stat_value , inline=False)

        await interaction.edit_original_response(content="" , embed=embed)


    @app_commands.command(name="team-stats" , description="Command to show stats of a team")
    async def team_stats(self, interaction: discord.Interaction, team_name: str):
        await interaction.response.send_message(content=f"Please wait loading team stats...")

        client = OpenAI(api_key=OPENAPI_KEY)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful sports expert. Give me stats of this team."},
                {"role": "user", "content": team_name}
            ],
            response_format=TeamStatListModel
        )

        all_stats = completion.choices[0].message.parsed.all_stats
        team_name = completion.choices[0].message.parsed.team_name
        sports_name = completion.choices[0].message.parsed.sports_name

        embed = discord.Embed(title="Player Statistics" , color=discord.Color.blurple())
        embed.set_footer(text=f"{interaction.user.id} | {interaction.user.name}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Team Name", value=team_name, inline=False)
        embed.add_field(name="Sports Name", value=sports_name, inline=False)
        for stat in all_stats:
            embed.add_field(name=stat.stat_name , value=stat.stat_value , inline=False)

        await interaction.edit_original_response(content="" , embed=embed)


    @app_commands.command(name="player-performance" , description="Command to show performance of a player")
    async def player_performance(self, interaction: discord.Interaction, player_name: str):
        await interaction.response.send_message(content=f"You requested performance of {player_name}")


    @app_commands.command(name="team-performance" , description="Command to show performance of a team")
    async def team_performance(self, interaction: discord.Interaction, team_name: str):
        await interaction.response.send_message(content=f"You requested performance of {team_name}")

    @app_commands.command(name="which-picks" , description="Command to choose a team that might win based on factual information and stats")
    async def which_picks(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(content=f"You requested which team might win based on {prompt}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Sports(bot))

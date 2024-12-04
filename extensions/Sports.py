import discord, os
from discord.ext import commands
from discord import app_commands

from models.Sports import TeamStatListModel
from models.Sports import WhichPickListModel
from models.Sports import WillHappenListModel
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
                {"role": "system", "content": "You are a helpful sports expert. Give me stats of this user. Also give data from latest 2024."},
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
                {"role": "system", "content": "You are a helpful sports expert. Give me stats of this team. Also give data from latest 2024."},
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

    @app_commands.command(name="which-picks" , description="Command to choose a team that might win based on factual information and stats")
    async def which_picks(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(content=f"Please wait loading prediction...")

        client = OpenAI(api_key=OPENAPI_KEY)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful sports expert. Give me which team might win based on factual information and stats. Give the probability in percentage. With why shorter than 100 characters. You will have to predict no matter what. I own't hear an excuse. Also give data from latest 2024."},
                {"role": "user", "content": prompt}
            ],
            response_format=WhichPickListModel
        )

        who_will_win = completion.choices[0].message.parsed.who_will_win
        why = completion.choices[0].message.parsed.why
        probability = completion.choices[0].message.parsed.probability
        all_stats = completion.choices[0].message.parsed.all_stats

        embed = discord.Embed(title="Player Statistics" , color=discord.Color.blurple())
        embed.set_footer(text=f"{interaction.user.id} | {interaction.user.name}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Who will win?", value=who_will_win, inline=False)
        embed.add_field(name="Why would they win?", value=why, inline=False)
        embed.add_field(name="Probability of them winning:", value=f"{probability}%", inline=False)
        for stat in all_stats:
            embed.add_field(name=stat.stat_name , value=stat.stat_value , inline=False)

        await interaction.edit_original_response(content="" , embed=embed)

    @app_commands.command(name="will-happen" , description="Command to check if something will happen based on factual information and stats.")
    async def will_happen(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(content=f"Please wait loading prediction...")

        client = OpenAI(api_key=OPENAPI_KEY)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful sports expert. Give me information that if something will happen or not. Give the probability in percentage. With why shorter than 100 characters. You will have to predict no matter what. I own't hear an excuse. Also give data from latest 2024."},
                {"role": "user", "content": prompt}
            ],
            response_format=WillHappenListModel
        )

        will_happen_or_not = completion.choices[0].message.parsed.will_happen_or_not
        why = completion.choices[0].message.parsed.why
        probability = completion.choices[0].message.parsed.probability
        all_stats = completion.choices[0].message.parsed.all_stats

        embed = discord.Embed(title="Player Statistics" , color=discord.Color.blurple())
        embed.set_footer(text=f"{interaction.user.id} | {interaction.user.name}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Will happen or not?", value=will_happen_or_not, inline=False)
        embed.add_field(name="Why would that happen?", value=why, inline=False)
        embed.add_field(name="Probability of that happening:", value=f"{probability}%", inline=False)
        for stat in all_stats:
            embed.add_field(name=stat.stat_name , value=stat.stat_value , inline=False)

        await interaction.edit_original_response(content="" , embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sports(bot))

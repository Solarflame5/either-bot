import requests
from bs4 import BeautifulSoup
from pathlib import Path
import discord
from discord import app_commands

def scrape_either():
    either_html = requests.get("https://either.io/").text
    either_soup = BeautifulSoup(either_html, "html.parser")
    either = {}
    either["preface"] = either_soup.find("h3", {"class": "preface"}).string
    either["option_a"] = either_soup.find_all("span", {"class": "option-text"})[0].string
    either["option_b"] = either_soup.find_all("span", {"class": "option-text"})[1].string
    either["title"] = either_soup.find("h2", {"id": "question-title"}).string
    either["desc"] = either_soup.find("p", {"class": "more-info"}).string
    return either

# Read bot token from "token.txt" in the same folder as "main.py"
token_path = Path(__file__).with_name("token.txt")
with token_path.open("r") as token_file:
    bot_token = token_file.read()

intents = discord.Intents.none() # bot only uses slash commands, no intents needed
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    await tree.sync() # ONLY UNCOMMENT ONCE WHEN YOU RUN THE BOT FOR THE FIRST TIME

@tree.command(name="wyr", description="Get a question from either.io")
async def send_wyr(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)
    either = scrape_either()
    wyr_embed = discord.Embed(
        title=either["title"],
        description=either["preface"]
    )
    wyr_embed.add_field(name="Option A", value=either["option_a"])
    wyr_embed.add_field(name="OR", value="")
    wyr_embed.add_field(name="Option B", value=either["option_b"])
    wyr_embed.set_footer(text=either["desc"])
    await interaction.followup.send(embed=wyr_embed, ephemeral=False)
    
client.run(bot_token)
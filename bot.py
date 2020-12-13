import discord
from discord.ext import commands
import random
from glob import glob
import logging
import os
from dotenv import load_dotenv

# Logging module setup (Maybe move to another .py file if this project gets big enough)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot setup
bot = commands.Bot(command_prefix="-pb ")
class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        friendlyHelp = discord.Embed(title=dialogueGenerator("help"), description='' , color=discord.Color.green())
        for page in self.paginator.pages:
            friendlyHelp.description += page
            await destination.send(embed=friendlyHelp)
bot.help_command = MyNewHelp()

def mediaGenerator(request):
    """
    Randomly picks an content file from the requested database.
    (request: selects prefered database)
    """
    folder = "content/" + request
    mediaPaths = glob(folder + "/*")
    return random.choice(mediaPaths)

def dialogueGenerator(request):
    return(random.choice(list(open("content/dialogue/" + request + ".txt"))))

@bot.event
async def on_ready():
    status = (dialogueGenerator("game") + " | -pb help")
    print("Internal Report Check: Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(name=status))
    channel = bot.get_channel(312583704524619786)
    await channel.send("External Report Check: Ready to go!")



### COMMANDS

## Random Content Commands
# Images
@bot.command()
async def photo(ctx):
    await ctx.send(file=discord.File(mediaGenerator("photo"), filename=None))
@bot.command()
async def picasso(ctx):
    await ctx.send(file=discord.File(mediaGenerator("picasso"), filename=None))
# Videos
@bot.command()
async def motion(ctx):
    await ctx.send(file=discord.File(mediaGenerator("motion"), filename=None))
# Text
#@bot.command() #TODO: Make an actual help embed
#async def help(ctx):
#    await ctx.send(dialogueGenerator("help"))

@bot.command()
async def quote(ctx):
    await ctx.send(dialogueGenerator("quote"))



### TOKEN
load_dotenv('.env')
bot.run(os.getenv('PERSONBOT_TOKEN'))
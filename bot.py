import discord
from discord.ext import commands
import random
import logging
import glob

# Logging module setup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# Bot setup
bot = commands.Bot(command_prefix="-pb ")
bot.remove_command('help')

def mediaGenerator(request):
    """
    Randomly picks an content file from the requested database.
    (request: selects prefered database)
    """
    folder = "content/" + request
    mediaPaths = glob.glob(folder + "/*")
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



# Random Content Commands
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
@bot.command()
async def help(ctx):
    await ctx.send(dialogueGenerator("help"))
@bot.command()
async def quote(ctx):
    await ctx.send(dialogueGenerator("quote"))



# Token for the bot
#bot.run("token")


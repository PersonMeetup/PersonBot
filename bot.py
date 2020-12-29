import discord
from discord.ext import commands
from discord.utils import get
import random
from glob import glob
import logging
import os

# Logging module setup (Maybe move to another .py file if this project gets big enough)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot setup
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="-pb ", intents=intents)
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

def dialogueGenerator(request): return(random.choice(list(open("content/dialogue/" + request + ".txt"))))

@bot.event
async def on_ready():
    status = (dialogueGenerator("game") + " | -pb help")
    print("Internal Report Check: Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(name=status))
    channel = bot.get_channel(312583704524619786)
    await channel.send("External Report Check: Ready to go!")
## Event below currently breaks all code.
## It's overriding all other commands being sent out.
#@bot.event
#async def on_message(message):
#    mention = f'<@!{bot.user.id}>'
#    if mention in message.content:
#        await message.channel.send(dialogueGenerator("mentioned"))
#    else:
#        ???
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(dialogueGenerator("error"))


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
@bot.command()
async def quote(ctx):
    await ctx.send(dialogueGenerator("quote"))
@bot.command()
async def harass(ctx):
    person = ctx.guild.get_member(149608924394422272)
    try:
        await ctx.send(f"{person.mention} " + dialogueGenerator("harass"))
    except:
        await ctx.send(dialogueGenerator("harass-error"))
# Audio
@bot.command()
async def summon(ctx):
    channel = ctx.message.author.voice.channel #This is kinda interesting, worth exploring more
    voice = get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        if ctx.voice_client is not None and not channel:
            await ctx.voice_client.move_to(channel)
            print(f"Connected to voice channel {channel}")
            await ctx.send("I'm here, can you just repeat that?")
    else:
        voice = await channel.connect()
        print(f"Connected to voice channel {channel}")
    
    try:
        source = discord.FFmpegPCMAudio(mediaGenerator("audio"))
        voice.play(discord.PCMVolumeTransformer(source))
        voice.source.volume = 0.5
    except:
        await ctx.send("Slow down!")
# KNOWN ISSUES: Moving the bot does not allow for playback (https://github.com/Rapptz/discord.py/issues/6219)

@bot.command()
async def leave(ctx): #There is no practical way to remove the bot from the VC automatically as far as I know (TODO: PROVE THIS WRONG)
    voice = get(ctx.bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()



### TOKEN
bot.run(os.getenv('PERSONBOT_TOKEN'))
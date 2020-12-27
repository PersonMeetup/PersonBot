import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
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
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)
slash = SlashCommand(client=bot,auto_register=True)
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
    status = (dialogueGenerator("game") + " | /pb help")
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

## (12/27/2020) The auto_register parameter in the discord_slash.client module
##              does not yet apply to subcommands. As such, @slash.slash is the
##              best method of adding commands as of right now. 

# Copied from eunwoo1104's README for reference
@slash.slash(name="test", description="Pain without end", guild_ids=[312583704524619786])
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])

## Random Content Commands
# Images
@slash.slash(name="photo",description="Sends a randomised photo to the chat", guild_ids=[312583704524619786])
async def _photo(ctx: SlashContext):
    await ctx.send(file=discord.File(mediaGenerator("photo"), filename=None))
@bot.command()
async def picasso(ctx):
    await ctx.send(file=discord.File(mediaGenerator("picasso"), filename=None))
# Videos
@bot.command()
async def motion(ctx):
    await ctx.send(file=discord.File(mediaGenerator("motion"), filename=None))
# Text
@slash.slash(name="quote",description="Sends a randomised quote", guild_ids=[312583704524619786])
async def _quote(ctx: SlashContext):
    await ctx.send(content=dialogueGenerator("quote"))
@bot.command()
async def harass(ctx):
    person = ctx.guild.get_member(149608924394422272)
    try:
        await ctx.send(content=(f"{person.mention} " + dialogueGenerator("harass")))
    except:
        await ctx.send(content=(dialogueGenerator("harass-error")))



### TOKEN
load_dotenv('.env')
bot.run(os.getenv('PERSONBOT_TOKEN'))
import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import manage_commands
from discord_slash import SlashCommand, SlashContext
import random
from glob import glob
import logging
import asyncio
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
guild_ids = [312583704524619786]

def mediaGenerator(request):
    """Randomly picks an content file from the requested database.

    `request`: selects prefered database
    """
    folder = "content/" + request
    mediaPaths = glob(folder + "/*")
    return random.choice(mediaPaths)

def dialogueGenerator(request): return(random.choice(list(open("content/dialogue/" + request + ".txt"))))

@bot.event
async def on_ready():
    status = (dialogueGenerator("game") + " | /pb help")
    print("Internal Report Check: Logged in as {0.user}".format(bot))
    await bot.change_presence(activity=discord.Game(name=status))
    channel = bot.get_channel(312583704524619786)
    await channel.send("External Report Check: Ready to go!")
    resp = await manage_commands.get_all_commands(787713500813197342,"Nzg3NzEzNTAwODEzMTk3MzQy.X9Y9XQ.MSdclRS0niMVZ5BHhx1TmApbosE",312583704524619786)
    print(resp) #TODO: Once updated to 3.9.X, change to pprint
    #sbdel = await manage_commands.remove_slash_command(787713500813197342,"Nzg3NzEzNTAwODEzMTk3MzQy.X9Y9XQ.MSdclRS0niMVZ5BHhx1TmApbosE",312583704524619786,792867979992891412)
    #print(sbdel)

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

## Reference For JSON: https://discord.com/channels/789032594456576001/789032934648447016/791911916422561822

## (12/27/2020) The auto_register parameter in the discord_slash.client module
##              does not yet apply to subcommands. As such, @slash.slash is the
##              best method of adding commands as of right now. 

# Copied from eunwoo1104's README for reference
@slash.slash(name="test", description="Pain without end", guild_ids=guild_ids)
async def _test(ctx: SlashContext):
    embed = discord.Embed(title="embed test")
    await ctx.send(content="test", embeds=[embed])

## Random Content Commands
# Images
@slash.slash(name="photo",description="Sends a random photo of Person", guild_ids=guild_ids)
async def _photo(ctx: SlashContext):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator("photo"), filename=None))
@slash.slash(name="picasso",description="Sends a random piece of art", guild_ids=guild_ids)
async def _picasso(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator("picasso"), filename=None))
# Videos
@slash.slash(name="motion",description="Sends a random video", guild_ids=guild_ids)
async def _motion(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator("motion"), filename=None))
# Text
@slash.slash(name="quote",description="Sends a randomised quote", guild_ids=guild_ids)
async def _quote(ctx: SlashContext):
    await ctx.send(content=dialogueGenerator("quote"))
@slash.slash(name="harass",description="Pings Person with a message", guild_ids=guild_ids)
async def _harass(ctx):
    person = ctx.guild.get_member(149608924394422272)
    try:
        await ctx.send(content=(f"{person.mention} " + dialogueGenerator("harass")))
    except:
        await ctx.send(content=(dialogueGenerator("harass-error")))
# Audio
@slash.slash(name="summon",description="Brings PersonBot into the VC momentarily", guild_ids=guild_ids)
async def _summon(ctx: SlashContext):
    channel = ctx.author.voice.channel #This is kinda interesting, worth exploring more
    voice = get(bot.voice_clients, guild=ctx.guild)
    def toaster(error):
        coro = voice.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            fut.result()
        except:
            pass #There was an error while sending message

    if voice and voice.is_connected():
        await ctx.send(content="Slow down!", complete_hidden=True)
    else:
        await ctx.send(5)
        voice = await channel.connect()
        print(f"Connected to voice channel {channel}")
        source = discord.FFmpegPCMAudio(mediaGenerator("audio"))
        voice.play(discord.PCMVolumeTransformer(source), after=toaster)
        voice.source.volume = 0.5



### TOKEN
bot.run(os.getenv('PERSONBOT_TOKEN'))
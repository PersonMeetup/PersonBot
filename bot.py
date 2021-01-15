import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, SlashContext, manage_commands
import random
from glob import glob
import asyncio
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents,help_command=None)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)

def mediaGenerator(request):
    """Randomly picks an content file from the requested database.

    `request`: selects prefered database
    """
    folder = 'content/' + request
    mediaPaths = glob(folder + '/*')
    return random.choice(mediaPaths)

def dialogueGenerator(request): return(random.choice(list(open('content/dialogue/' + request + '.txt'))))

@bot.event
async def on_ready():
    status = (dialogueGenerator('game') + ' | / enabled')
    print('Internal Report Check: Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name=status))
    resp = await manage_commands.get_all_commands(bot.user.id,os.getenv('PERSONBOT_TOKEN'),None)
    print(resp) #TODO: Once updated to 3.9.X, change to pprint



# "mediaGenerator" can be used to select random files.
# PNG, GIF, MP4, pretty much anything under 8GB works.
@slash.slash(name='photo', description='Sends a random photo')
async def _photo(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator('photo'), filename=None))
@slash.slash(name='motion',description='Sends a random video')
async def _motion(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator('motion'), filename=None))

# "dialougeGenerator" picks random lines in TXT files.
@slash.slash(name='quote',description='Sends a randomised quote')
async def _quote(ctx):
    await ctx.send(content=dialogueGenerator('quote'))

# Another showcase of "mediaGenerator", this time with voice capabilities!
@slash.slash(name='summon',description='Brings PersonBot into the VC momentarily')
async def _summon(ctx):
    channel = ctx.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    def toaster(error):
        coro = voice.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            fut.result()
        except:
            pass #There was an error while sending message

    if voice and voice.is_connected():
        await ctx.send(content=("`Unable to summon PersonBot, they may be in a voice channel already.`"), complete_hidden=True)
    else:
        await ctx.send(5)
        voice = await channel.connect()
        print(f'Connected to voice channel {channel}')
        source = discord.FFmpegPCMAudio(mediaGenerator('audio'))
        voice.play(discord.PCMVolumeTransformer(source), after=toaster)
        voice.source.volume = 0.5



bot.run(os.getenv('PERSONBOT_TOKEN'))
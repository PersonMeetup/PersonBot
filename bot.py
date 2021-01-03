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
bot = commands.Bot(command_prefix='/', intents=intents,help_command=None)
slash = SlashCommand(client=bot,auto_register=True,auto_delete=True)
guild_ids = [312583704524619786]

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
    resp = await manage_commands.get_all_commands(787713500813197342,os.getenv('PERSONBOT_TOKEN'),None)
    print(resp) #TODO: Once updated to 3.9.X, change to pprint

@bot.event
async def on_message(message):
    mention = f'<@!{bot.user.id}>'
    if mention in message.content:
        await message.channel.send(dialogueGenerator('mentioned'))



### COMMANDS

## Reference For JSON: https://discord.com/channels/789032594456576001/789032934648447016/791911916422561822
## Future Note: subcommands require a base string of <= 3 (do not include spaces)

## Random Content Commands
# Images
@slash.slash(name='photo', description='Sends a random photo of Person')
async def _photo(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator('photo'), filename=None))
@slash.slash(name='picasso',description='Sends a random piece of art')
async def _picasso(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator('picasso'), filename=None))
# Videos
@slash.slash(name='motion',description='Sends a random video')
async def _motion(ctx):
    await ctx.send(5)
    await ctx.channel.send(file=discord.File(mediaGenerator('motion'), filename=None))
# Text
@slash.slash(name='quote',description='Sends a randomised quote')
async def _quote(ctx):
    await ctx.send(content=dialogueGenerator('quote'))
@slash.slash(name='harass',description='Pings Person with a message')
async def _harass(ctx):
    person = ctx.guild.get_member(149608924394422272)
    try:
        await ctx.send(content=(f'{person.mention} ' + dialogueGenerator('harass')))
    except:
        await ctx.send(content=(dialogueGenerator('error/error_harass') + "\n`Person Meetup wasn't detected in the server!`"), complete_hidden=True)
# Audio
@slash.slash(name='summon',description='Brings PersonBot into the VC momentarily')
async def _summon(ctx):
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
        await ctx.send(content=(dialogueGenerator('error/error_summon') + "\n`Unable to summon PersonBot, they may be in a voice channel already.`"), complete_hidden=True)
    else:
        await ctx.send(5)
        voice = await channel.connect()
        print(f'Connected to voice channel {channel}')
        source = discord.FFmpegPCMAudio(mediaGenerator('audio'))
        voice.play(discord.PCMVolumeTransformer(source), after=toaster)
        voice.source.volume = 0.5



### TOKEN
bot.run(os.getenv('PERSONBOT_TOKEN'))
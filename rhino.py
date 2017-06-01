#!/usr/bin/env python3

import asyncio
import json
import os
import random
import sys

import aiohttp
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

URL_GOOGLE_RHINO = "https://www.google.com/search?q=rhino+animal&tbm=isch"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
HEADERS = {"User-Agent": USER_AGENT}

FILE_SETTINGS = "config.json"
FACTS_RHINOS = [('The name "rhinoceros" comes from Greek "rhino," meaning nose, and "ceros," '
                 'meaning horn. I\'m talking about your face, by the way.'),
                ('In many cultures, rhino horns are believed to have healing properties, and '
                 'this has led to their use in medicines. '
                 'They\'re also made of the same substance as your fingernails. Ew.'),
                ('The smallest species of rhino is the Sumatran rhinoceros, standing between 112 '
                 'and 145 cm at the shoulder and having a head-body length of 2.36 to 3.18 m. So '
                 'it is still fairly large - approximately the size of your significant other.'),
                ('There are five species of rhino - the black rhino, the white rhino, the Indian '
                 'rhino, the Javan rhino, and the Sumatran rhino. There is also a RhinoBot.'),
                ('The white rhino is the largest species of rhino, and the largest land '
                 'animal after the elephants. It is very large.'),
                ('Rhino horns are pointy.'),
                ('A rhino crashing into you would hurt. By the way, a group of rhinos is called '
                 'a "crash".'),
                ("Rhinos are gray. They share this property with elephants and the color gray, "
                 "among other things."),
                ('Rhinos have toes.'),
                ('Rhinos can run up to 40 miles per hour, which is very fast.'),
                ('Rhinos have a bad sense of sight, but strong senses of smell and hearing.')]

settings = {}
systemrandom = random.SystemRandom()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("*", "\U0001F98F ", "\U0001F98F"))
bot.session = aiohttp.ClientSession(loop=bot.loop)

# Ignore this meme.
del bot.all_commands["help"]

@bot.check
def is_human(ctx):
    if ctx.author.bot:
        return False
    return True

@bot.event
async def on_command_error(ctx, exc):
    if not isinstance(exc, (commands.CommandNotFound, commands.CheckFailure)):
        message = await ctx.send(f"{exc}")

## HELP COMMAND ##
@bot.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def help(ctx, *, command:str=None):
    """Display help about the bot."""
    if not command:
        help = ", ".join(f"{ctx.prefix}{command.name}" for command in bot.commands if not command.hidden)
        help = (f"{ctx.author.mention}, **Commands**\n```{help}```"
                "https://github.com/Just-Some-Bots/MusicBot/wiki/Commands")
        await ctx.send(help)
    elif command in bot.all_commands:
        help_pages = await bot.formatter.format_help_for(ctx, bot.all_commands[command])
        for page in help_pages:
            await ctx.send(page)

## MUSIC COMMANDS ##
@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def play(ctx):
    """You just got played!"""
    await ctx.send("You just got played!")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def queue(ctx):
    """Prints a queue."""
    await ctx.send("http://i.telegraph.co.uk/multimedia/archive/02854/queue_1446267c_2854335b.jpg")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def np(ctx):
    """No problem!"""
    await ctx.send("No problem!")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def skip(ctx):
    """Skip someone's face."""
    await ctx.send("http://www.cardboardrepublic.com/wp-content/uploads/2014/05/uno-skip.png")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def search(ctx):
    """Search someone's face."""
    await ctx.send("I'll search your face!")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def shuffle(ctx):
    """Shuffles a deck of cards."""
    await ctx.send("Shuffling a deck of cards...")
    await asyncio.sleep(15)
    await ctx.send("Done.")

@commands.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(ctx, limit:int):
    """Clears the queue."""
    await ctx.send("There is no queue. Only Rhino.")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def pause(ctx):
    """Pauses for a few seconds."""
    await ctx.send("...")
    await asyncio.sleep(5)
    await ctx.send("Okay.")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def resume(ctx):
    """Shows a resume."""
    await ctx.send("http://www.nafme.org/wp-content/files/2016/01/Sample-Resume-3-1.jpg")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def volume(ctx):
    """Volumetric analysis."""
    await ctx.send("http://users.iconz.co.nz/trout/vaSoln.gif")

@commands.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def summon(ctx):
    """Blue-Eyes White Dragon!"""
    await ctx.send(("I summon Blue-Eyes White Dragon!\n"
                    "https://vignette2.wikia.nocookie.net/yugioh/images/d/d4/"
                    "BlueEyesWhiteDragon-DUSA-EN-UR-1E.png"))

## BOT RELATED AND OWNER COMMANDS ##
@bot.command()
@commands.is_owner()
async def clean(ctx, times:int=1):
    """Clean up the bot's messages."""
    if times < 1:
        return commands.UserInputError("Can't delete less than 1 message.")
    times_executed = 0
    async for message in ctx.channel.history():
        if times_executed == times:
            break
        if message.author.id == bot.user.id:
            await message.delete()
            times_executed += 1

@bot.command(aliases=["halt", "kys"])
@commands.is_owner()
async def shutdown(ctx):
    """Shut the bot down."""
    await bot.logout()

@bot.command()
@commands.is_owner()
async def restart(ctx):
    """Restarts the bot."""
    await bot.logout()
    os.execv(sys.executable, [sys.executable] + sys.argv + ["&"])

@bot.command(aliases=["about"])
@commands.is_owner()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def fact(ctx):
    """Display a random fact about a rhino."""
    fact = systemrandom.choice(FACTS_RHINOS)
    message = f"**Did you know?**\n{fact}"
    await ctx.send(message)

@bot.command(aliases=["rhino", "picture", "google", "gimage"])
@commands.cooldown(5, 10, commands.BucketType.channel)
async def image(ctx):
    """Fetch a random image of a rhino."""
    async with bot.session.request("GET", URL_GOOGLE_RHINO, headers=HEADERS) as response:
        if response.status == 200:
            data = await response.text()
            soup = BeautifulSoup(data)
            links = soup.find_all("div", class_="rg_meta")
            for index in range(len(links)):
                links[index] = json.loads(links[index].contents[0]).get("ou")
            await ctx.send(systemrandom.choice(links))
        else:
            await ctx.send("Whoops, couldn't find a picture of a rhino.")

if __name__ == "__main__":
    try:
        with open(FILE_SETTINGS) as f:
            new_settings = json.load(f)
            for key, value in new_settings.items():
                settings[key] = value
    except Exception as error:
        print(error)
        token = input("Enter your bot token here: ")
        settings["OAUTH_TOKEN_DISCORD"] = token
        with open(FILE_SETTINGS, "w") as f:
            json.dump(settings, f)
    bot.run(settings["OAUTH_TOKEN_DISCORD"])

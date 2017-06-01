#!/usr/bin/env python3

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
                 'meaning horn.'),
                ('In many cultures, rhino horns are thought to have healing properties, which '
                 'has led to them being hunted to near extinction.'),
                ('The smallest species of rhino is the Sumatran rhinoceros, standing between 112 and '
                 '145 cm at the shoulder and having a head-body length of 2.36 to 3.18 m.'),
                ('There are five species of rhino - the black rhino, the white rhino, the Indian '
                 'rhino, the Javan rhino, and the Sumatran rhino.'),
                ('The white rhino is the largest species of rhino, and the largest land '
                 'animal after the elephants.'),
                ('Rhino horns are made of keratin, the same substance as your fingernails and '
                 'hair.'),
                ('A group of rhinos is called a "herd" or a "crash".'),
                ("The white and black rhinos are actually both gray. The white rhino's name comes "
                 'from Afrikaans "weit" meaning "wide", referring to the animal\'s large mouth. '
                 'The black rhino\'s name may come from the dark mud that they often wallow in.'),
                ('The closest living relatives of the rhinos are tapirs, horses, and zebras.'),
                ('Rhinos can run up to 40 miles per hour.'),
                ('Rhinos have a bad sense of smell, but strong senses of smell and hearing.'),
                ("Of all mammal fights within the same species, black rhinos have the highest "
                 "death rates - 50% of males and 30% of females.")]

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

@bot.command()
@commands.cooldown(5, 10, commands.BucketType.channel)
async def help(ctx, *, command:str=None):
    """Display help about the bot."""
    if not command:
        help = ", ".join(f"{ctx.prefix}{command.name}" for command in bot.commands if not command.hidden)
        help = f"{ctx.author.mention}, **Commands**\n```{help}```https://github.com/Just-Some-Bots/MusicBot"
        await ctx.send(help)
    elif command in bot.all_commands:
        help_pages = await bot.formatter.format_help_for(ctx, bot.all_commands[command])
        for page in help_pages:
            await ctx.send(page)

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

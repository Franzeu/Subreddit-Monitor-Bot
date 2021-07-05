import discord
import random
import asyncpraw
import os
from discord.embeds import Embed 
from dotenv import load_dotenv
from discord.ext import commands
from discord import message
 
load_dotenv()

client = commands.Bot(command_prefix = '!')

reddit = asyncpraw.Reddit(client_id = os.getenv("REDDIT_CLIENT_ID"), 
                     client_secret = os.getenv("REDDIT_CLIENT_SECRET"), 
                     username = os.getenv("REDDIT_USERNAME"), 
                     password = os.getenv("REDDIT_PASSWORD"), 
                     user_agent = os.getenv("REDDIT_USER_AGENT"))

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")

@client.command()
async def meme(ctx):
    subreddit = await reddit.subreddit("mechmarket")

    all_subs = []

    async for submission in subreddit.top(limit = 10):
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title = name)
    em.set_image(url = url)

    await ctx.send(embed = em)

@client.command
async def displayembed():
    embed = discord.Embed(
        title = 'Title',
        description = 'This is a description.',
        color = discord.Color.blue(),
        
    )

    embed.set_footer(text="This is a footer.")

    embed.set_image(url='https://cdn.discordapp.com/attachments/766444741239504941/859595814891552778/71ouOX4BmIL.png')
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/766444741239504941/859595814891552778/71ouOX4BmIL.png')
    embed.set_author(name='Author name', icon_url='https://cdn.discordapp.com/attachments/766444741239504941/859595814891552778/71ouOX4BmIL.png')
    embed.add_field(name ='Field name', value='Field Value', inline=False)
    embed.add_field(name ='Field name', value='Field Value', inline=True)
    embed.add_field(name ='Field name', value='Field Value', inline=True)

    await client.say(embed = embed)
    


client.run(os.getenv("DISCORD_TOKEN"))
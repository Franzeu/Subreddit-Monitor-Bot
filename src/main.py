import discord
import random
import asyncpraw
import praw
import os
import asyncio
from discord.embeds import Embed 
from dotenv import load_dotenv
from discord.ext import commands
from discord import message
from discord.ext import tasks

load_dotenv()

client = commands.Bot(command_prefix = '!')

reddit = asyncpraw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    check_for_updates=False,
    comment_kind="t1",
    message_kind="t4",
    redditor_kind="t2",
    submission_kind="t3",
    subreddit_kind="t5",
    trophy_kind="t6",
    oauth_url="https://oauth.reddit.com",
    reddit_url="https://www.reddit.com",
    short_url="https://redd.it",
    ratelimit_seconds=5,
    timeout=16,
)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument")


@client.command()
async def showtop(ctx, input_subreddit, filter):

    filter_list = ["day", "month", "year", "all", "hour"]

    if filter not in filter_list:
        await ctx.send("Incorrect filter")
        return None

    if filter == "all":
        await ctx.send("Posting top 50 posts of all time from " + input_subreddit)
    else:        
        await ctx.send("Posting top 50 posts of the " + filter + " from " + input_subreddit)

    subreddit = await reddit.subreddit(input_subreddit)

    async for submission in subreddit.top(filter, limit = 50):
        display_embed = discord.Embed(title = submission.title[0:256])
        display_embed.set_author(name = "RedditPost Bot 🐢")
        display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
        display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
        display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
        display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
        await ctx.send(embed = display_embed)

    if filter == "all":
        await ctx.send("Finished posting top 50 posts of all time from " + input_subreddit)
    else:
        await ctx.send("Finished posting top 50 posts of the " + filter + " from " + input_subreddit)

@client.command()
async def showhot(ctx, input_subreddit):

    await ctx.send("Posting hot 50 posts from " + input_subreddit)

    subreddit = await reddit.subreddit(input_subreddit)

    async for submission in subreddit.hot(limit = 50):
        display_embed = discord.Embed(title = submission.title[0:256])
        display_embed.set_author(name = "RedditPost Bot 🐢")
        display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
        display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
        display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
        display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
        await ctx.send(embed = display_embed)

    await ctx.send("Finished hot posts from " + input_subreddit)

@client.command()
async def showrecent(ctx, input_subreddit):

    global postloop

    @tasks.loop(seconds=1)
    async def postloop(inputsub):
        subreddit = await reddit.subreddit(input_subreddit)

        async for submission in subreddit.stream.submissions():
            display_embed = discord.Embed(title = submission.title[0:256])
            display_embed.set_author(name = "RedditPost Bot 🐢")
            display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
            display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
            display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
            display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
            await ctx.send(embed = display_embed)
        
    postloop.start(input_subreddit)
    await ctx.send("Posting recent posts from " + input_subreddit)
        

@client.command()
async def stopshowing (ctx):
    postloop.cancel()
    await ctx.send("Successfully deactivated showsub")

    
client.run(os.getenv("DISCORD_TOKEN"))
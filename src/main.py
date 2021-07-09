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

@client.command(aliases=['showsub'])
async def showsubreddit(ctx, input_subreddit):
    subreddit = await reddit.subreddit(input_subreddit)

    # all_subs = []

    async for submission in subreddit.stream.submissions():
        display_embed = discord.Embed(title = submission.title)
        display_embed.set_author(name = "RedditPost Bot 🐢")
        display_embed.add_field(name =  "Link:", value = submission.url, inline=True)
        display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
        await ctx.send(embed = display_embed)
    
    # for subs in all_subs:
        # display_embed = discord.Embed(title = subs.title)
        # display_embed.set_author(name = "RedditPost Bot 🐢")
        # display_embed.add_field(name =  "Link:", value = subs.url, inline=True)
        # display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
        # await ctx.send(embed = display_embed)
    
client.run(os.getenv("DISCORD_TOKEN"))
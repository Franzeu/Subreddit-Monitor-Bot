import discord
import asyncpraw
import os
from discord.embeds import Embed 
from dotenv import load_dotenv
from discord.ext import commands
from discord import message
from discord.ext import tasks

#Loads the .env file.
load_dotenv()

is_running = False

#Command prefix used for commands on Discord
client = commands.Bot(command_prefix = '!')

#Creates a read-only Reddit instances. Read-only instances are able to retrieve information from subreddits
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

#Keywords for the command !streamkeywords
userKeywords = []

#When the bot is running, it sends a message in the terminal saying that they have logged in.
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

#Error handling
@client.event
async def on_command_error(ctx, error):
    #If a user inputs a command that bot does not recognize, it sends a message that the command was not found.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    
    #If a user inputs a command but leaves the argument empty, it sends a message that the user is missing a required argument.
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument")

#Displays all the commands that are available to use 
@client.command()
async def allcommands(ctx):
    display_embed=discord.Embed(title="RedditPost Bot 🐢", description="All the commands that are available to use!", color=0x007514)
    display_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png')
    display_embed.add_field(name="Commands: ", value="!add, !show, !clear, !showtop [subreddit] [filter], !showhot [subreddit], !shownew [subreddit], !stream [subreddit], !streamkey [subreddit], !stop, !stopkey", inline=False)
    display_embed.add_field(name="Filters: ", value="hour, day, month, year, all, hour", inline=True)
    await ctx.send(embed = display_embed)

#Adds a word into userKeyword list
@client.command()
async def add(ctx, keyword):
    userKeywords.append(keyword)
    await ctx.send("Added " + keyword + " as a keyword")

#Displays the userKeyword list
@client.command()
async def show(ctx):
    for keyword in range(len(userKeywords)):
        await ctx.send(userKeywords[keyword])

#Deletes all the keywords in the userKeyword list
@client.command()
async def clear(ctx):
    userKeywords.clear()
    await ctx.send("Cleared keyword list")

#Displays the top 50 posts of the user's requested subreddit during a specific time.
@client.command()
async def showtop(ctx, input_subreddit, filter):

    filter_list = ["day", "week", "month", "year", "all", "hour"]

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

#Displays the hot 50 posts of the user's requested subreddit.
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

#Displays the newest 50 posts of the user's requested subreddit
@client.command()
async def shownew(ctx, input_subreddit):

    await ctx.send("Posting new 50 posts from " + input_subreddit)

    subreddit = await reddit.subreddit(input_subreddit)

    async for submission in subreddit.new(limit = 50):
        display_embed = discord.Embed(title = submission.title[0:256])
        display_embed.set_author(name = "RedditPost Bot 🐢")
        display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
        display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
        display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
        display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
        await ctx.send(embed = display_embed)

    await ctx.send("Finished new posts from " + input_subreddit)

#Displays the newest posts of a subreddit and updates in real time whenever a new post is created. This command only sends posts to the chat
#that have keywords in the title. Runs until the user tells it to stop by using !stopkeywords
@client.command()
async def streamkey(ctx, input_subreddit):
    
    global keywordloop
    global is_running

    if is_running == False:
        is_running = True
        @tasks.loop(seconds=1)
        async def keywordloop(inputsub):
                subreddit = await reddit.subreddit(input_subreddit)

                async for submission in subreddit.stream.submissions():
                    subtitle = submission.title
                    if any(keyword in subtitle for keyword in userKeywords):
                        display_embed = discord.Embed(title = submission.title[0:256])
                        display_embed.set_author(name = "RedditPost Bot 🐢")
                        display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
                        display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
                        display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
                        display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
                        await ctx.send(embed = display_embed)
    else:
        await ctx.send("Another command is running!")

        
    keywordloop.start(input_subreddit)
    await ctx.send("Posting streaming posts from " + input_subreddit)

#Displays the newest posts of a subreddit and updates in real time whenever a new post is created. Runs until the user tells it to stop by using !stop
@client.command()
async def stream(ctx, input_subreddit):

    global streamloop
    global is_running

    if is_running == False:
        is_running = True
        @tasks.loop(seconds=1)
        async def streamloop(inputsub):
            subreddit = await reddit.subreddit(input_subreddit)

            async for submission in subreddit.stream.submissions():
                display_embed = discord.Embed(title = submission.title[0:256])
                display_embed.set_author(name = "RedditPost Bot 🐢")
                display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
                display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
                display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
                display_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/435613438560043008/862045274037813258/375ce83551aafaec5f2d5ffef338b2fa.png")
                await ctx.send(embed = display_embed)
    else:
        await ctx.send("Another command is running!")
        
    streamloop.start(input_subreddit)
    await ctx.send("Posting streaming posts from " + input_subreddit)

#Stops the !stream command.
@client.command()
async def stop(ctx):
    global is_running
    streamloop.cancel()
    is_running = False
    await ctx.send("Successfully deactivated !stream")

# Stops the !streamkey command.
@client.command()
async def stopkey(ctx):
    global is_running
    keywordloop.cancel()
    is_running = False
    await ctx.send("Successfully deactivated !streamkeywords")

#Runs the bot
client.run(os.getenv("DISCORD_TOKEN"))

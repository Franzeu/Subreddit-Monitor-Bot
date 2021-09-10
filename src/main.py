import discord
import asyncpraw
import asyncprawcore
import os
import re
from discord.embeds import Embed
from discord.errors import NotFound 
from dotenv import load_dotenv
from discord.ext import commands
from discord import message
from discord.utils import get
from discord.ext import tasks
from prawcore import NotFound

# Loads the .env file.
load_dotenv()

# Command prefix used for commands on Discord
client = commands.Bot(command_prefix = '!')

# Creates a read-only Reddit instances. Read-only instances are able to retrieve information from subreddits
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

# Keywords for the command !streamkeywords
userKeywords = []

# Checks if the server has the role "Notify". 
active_role = False

#Limits the amount of posts that the bot sends in the discord chat
post_limit = 10

running = False

# When the bot is running, it sends a message in the terminal saying that they have logged in.
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

# Error handling
@client.event
async def on_command_error(ctx, error):
    # If a user inputs a command that bot does not recognize, it sends a message that the command was not found.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("**Command not found. ❌** Please look at !allcommands if you need help!")
    
    # If a user inputs a command but leaves the argument empty, it sends a message that the user is missing a required argument.
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send("**Missing required argument. ❌** Please look at !allcommands if you need help!")

# Displays all the commands that are available to use 
@client.command()
async def allcommands(ctx):
    display_embed=discord.Embed(title="RedditPost Bot 🤖", description="All the commands that are available to use!")
    display_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/435613438560043008/879198155374211122/question-mark-1750942_960_720.png')
    display_embed.add_field(name="Commands: ", value="!add [keyword], !show, !clear, !limit [# of posts], !top [subreddit] [filter], !hot [subreddit], !new [subreddit], !stream [subreddit], !stop", inline=False)
    display_embed.add_field(name="Filters: ", value="hour, day, month, year, all, hour", inline=True)
    await ctx.send(embed = display_embed)

# Adds a word into userKeyword list
@client.command()
async def add(ctx, keyword):
    userKeywords.append(keyword)
    await ctx.send("Added " + keyword + " as a keyword ✅")

# Displays the userKeyword list
@client.command()
async def show(ctx):
    for keyword in range(len(userKeywords)):
        await ctx.send(userKeywords[keyword])

# Deletes all the keywords in the userKeyword list
@client.command()
async def clear(ctx):
    userKeywords.clear()
    await ctx.send("Cleared keyword list 📃")

@client.command()
async def limit(ctx, number_of_posts):
    global post_limit
    post_limit = number_of_posts
    string_post_limit = str(post_limit)
    await ctx.send("Limited the amount of posts to " + string_post_limit + " ✅")

# Displays the top posts of the user's requested subreddit during a specific time.
@client.command()
async def top(ctx, input_subreddit, filter):

    filter_list = ["day", "week", "month", "year", "all", "hour"]

    global running
    global post_limit

    string_post_limit = str(post_limit)
    int_post_limit = int(post_limit)

    if len(input_subreddit) > 21 or len(input_subreddit) < 3:
        await ctx.send("Subreddit name is too long! Must be between 3-21 characters long. 😓")
        return None
    elif not re.match("^[a-zA-Z_]*$", input_subreddit):
        await ctx.send("Subreddit name cannot have spaces or special characters. Underscores are allowed. 😓")
        return None
   
    try:
        subreddit = await reddit.subreddit(input_subreddit, fetch=True) # by default Async PRAW doesn't make network requests when subreddit is called
    except asyncprawcore.Redirect as e: 
        # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
        await ctx.send("Subreddit "+ input_subreddit +" does not exist. 😥")
        return None


    if running == False:
        running = True
       
        if filter not in filter_list:
            await ctx.send("Incorrect filter 🚫")
            return None
        
        if filter == "all":
            await ctx.send("Posting **TOP** " + string_post_limit + " posts of all time from " + input_subreddit + " 🔝")
        else:        
            await ctx.send("Posting **TOP** " + string_post_limit + " posts of the " + filter + " from " + input_subreddit + " 🔝")
      
        subreddit = await reddit.subreddit(input_subreddit)
        
        async for submission in subreddit.top(filter, limit = int_post_limit):
            display_embed = discord.Embed(title = submission.title[0:256])
            display_embed.set_author(name = "RedditPost Bot 🤖")
            display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
            display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
            display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
            display_embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_960_720.png")
            await ctx.send(embed = display_embed)

        running = False
        if filter == "all":
            await ctx.send("Finished posting **TOP** " + string_post_limit + " posts of all time from " + input_subreddit + " ✅")
        else:
            await ctx.send("Finished posting **TOP** " + string_post_limit + " posts of the " + filter + " from " + input_subreddit + " ✅")
    else:
        await ctx.send("**Another command is running!** 🚫")

# Displays hot posts of the user's requested subreddit.
@client.command()
async def hot(ctx, input_subreddit):

    global running
    global post_limit
    string_post_limit = str(post_limit)
    int_post_limit = int(post_limit)

    if len(input_subreddit) > 21 or len(input_subreddit) < 3:
        await ctx.send("Subreddit name is too long! Must be between 3-21 characters long. 😓")
        return None
    elif not re.match("^[a-zA-Z_]*$", input_subreddit):
        await ctx.send("Subreddit name cannot have spaces or special characters. Underscores are allowed. 😓")
        return None

    try:
        subreddit = await reddit.subreddit(input_subreddit, fetch=True) # by default Async PRAW doesn't make network requests when subreddit is called
    except asyncprawcore.Redirect as e: 
        # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
        await ctx.send("Subreddit "+ input_subreddit +" does not exist. 😥")
        return None

    if running == False:
        running = True
        
        await ctx.send("Posting **HOT** " + string_post_limit + " posts from " + input_subreddit + " 🔥")

        subreddit = await reddit.subreddit(input_subreddit)

        async for submission in subreddit.hot(limit = int_post_limit):
            display_embed = discord.Embed(title = submission.title[0:256])
            display_embed.set_author(name = "RedditPost Bot 🤖")
            display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
            display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
            display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
            display_embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_960_720.png")
            await ctx.send(embed = display_embed)

        running = False
        await ctx.send("Finished posting **HOT** " + string_post_limit + " posts from " + input_subreddit + " ✅")
    else:
        await ctx.send("**Another command is running!** 🚫")

# Displays the newest 50 posts of the user's requested subreddit
@client.command()
async def new(ctx, input_subreddit):

    global running
    global post_limit
    string_post_limit = str(post_limit)
    int_post_limit = int(post_limit)

    if len(input_subreddit) > 21 or len(input_subreddit) < 3:
        await ctx.send("Subreddit name is too long! Must be between 3-21 characters long. 😓")
        return None
    elif not re.match("^[a-zA-Z_]*$", input_subreddit):
        await ctx.send("Subreddit name cannot have spaces or special characters. Underscores are allowed. 😓")
        return None

    try:
        subreddit = await reddit.subreddit(input_subreddit, fetch=True) # by default Async PRAW doesn't make network requests when subreddit is called
    except asyncprawcore.Redirect as e: 
        # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
        await ctx.send("Subreddit "+ input_subreddit +" does not exist. 😥")
        return None

    if running == False:
        running = True

        await ctx.send("Posting **NEW** " + string_post_limit + " posts from " + input_subreddit + " 🆕")

        subreddit = await reddit.subreddit(input_subreddit)

        async for submission in subreddit.new(limit = int_post_limit):
            display_embed = discord.Embed(title = submission.title[0:256])
            display_embed.set_author(name = "RedditPost Bot 🤖")
            display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
            display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
            display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
            display_embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_960_720.png")
            await ctx.send(embed = display_embed)

        running = False
        await ctx.send("Finished posting **NEW** " + string_post_limit + " posts from " + input_subreddit + " 🆕")
    else:
        await ctx.send("**Another command is running!** 🚫")

# Displays the newest posts of a subreddit and updates in real time whenever a new post is created. Once a new post is created, the bot will @
# the users in the 'Notify' role. Additionally, if keywords are added, the bot will only send posts to the chat that have keywords in the reddit post title. 
# Runs until the user tells it to stop by using the command !stop
@client.command()
async def stream(ctx, input_subreddit):

    global streamloop
    global running
    global active_role

    for role in ctx.guild.roles:
        if role.name == 'Notify':
            active_role = True

    if len(input_subreddit) > 21 or len(input_subreddit) < 3:
        await ctx.send("Subreddit name is too long! Must be between 3-21 characters long. 😓")
        return None
    elif not re.match("^[a-zA-Z_]*$", input_subreddit):
        await ctx.send("Subreddit name cannot have spaces or special characters. Underscores are allowed. 😓")
        return None

    try:
        subreddit = await reddit.subreddit(input_subreddit, fetch=True) # by default Async PRAW doesn't make network requests when subreddit is called
    except asyncprawcore.Redirect as e: 
        # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
        await ctx.send("Subreddit "+ input_subreddit +" does not exist. 😥")
        return None

    if active_role == True:
        if len(userKeywords) == 0:
            if running == False:
                running = True
                @tasks.loop(seconds=1)
                async def streamloop(inputsub):
                    subreddit = await reddit.subreddit(input_subreddit)

                    notify = get(ctx.guild.roles, name = "Notify")
                    
                    async for submission in subreddit.stream.submissions():
                        
                        await ctx.send(f"{notify.mention}")
                        display_embed = discord.Embed(title = submission.title[0:256])
                        display_embed.set_author(name = "RedditPost Bot 🤖")
                        display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
                        display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
                        display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
                        display_embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_960_720.png")
                        await ctx.send(embed = display_embed)
            else:
                await ctx.send("**Another command is running!** 🚫")
        else:
            if running == False:
                running = True
                @tasks.loop(seconds=1)
                async def streamloop(inputsub):
                        subreddit = await reddit.subreddit(input_subreddit)

                        notify = get(ctx.guild.roles, name = "Notify")

                        async for submission in subreddit.stream.submissions():
                            subtitle = submission.title
                            if any(keyword in subtitle for keyword in userKeywords):
                                await ctx.send(f"{notify.mention}")
                                display_embed = discord.Embed(title = submission.title[0:256])
                                display_embed.set_author(name = "RedditPost Bot 🤖")
                                display_embed.add_field(name =  "Subreddit:", value = input_subreddit, inline=False)
                                display_embed.add_field(name =  "Link:", value = submission.shortlink, inline=True)
                                display_embed.add_field(name =  "Posted by:", value = submission.author, inline=True)
                                display_embed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2015/12/16/17/41/bell-1096280_960_720.png")
                                await ctx.send(embed = display_embed)
            else:
                await ctx.send("**Another command is running!** 🚫")
    else: 
        await ctx.send("Need to create the role **Notify** in order to get pinged whenever a new post is created. 🛠")
        return None
   
    streamloop.start(input_subreddit)
    active_role = False
    await ctx.send("**Streaming** posts from " + input_subreddit + " 💻")

# Stops the !stream command.
@client.command()
async def stop(ctx):
    global running
    global active_role
    streamloop.cancel()
    running = False
    active_role = False
    await ctx.send("Successfully deactivated the **stream** ✅")

#Runs the bot
client.run(os.getenv("DISCORD_TOKEN"))

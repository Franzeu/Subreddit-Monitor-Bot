# RedditPosts-Bot
RedditPosts-Bot is a Discord bot that retreives reddit submissions and streams it in real time.

![Alt text](assets/Title.gif?raw=true "Title")

## Installation

Before using this bot, make sure you have created an app in https://www.reddit.com/prefs/apps and bot in your discord development portal. 

In order to use this bot, two APIs must be installed. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these two APIs.

```bash
pip install discord.py
```
```bash
pip install asyncpraw
```

After installing both APIs. Go ahead and clone this repository. 

```bash
https://github.com/Franzeu/RedditPosts-Bot.git
```

Once cloned, go ahead and go into the src folder and create a .env. In the .env, go ahead and fill in the blanks

```bash
DISCORD_TOKEN = 
REDDIT_CLIENT_ID = 
REDDIT_CLIENT_SECRET = 
REDDIT_USER_AGENT = 
REDDIT_USERNAME = 
REDDIT_PASSWORD = 
```

After filling in all the necessary information in your .env, you can go ahead and run the bot! Have fun!

## Running the application

There are several commands that you can use when using this bot. Here are all the commands that are available!

```
!allcommands
!add [keyword]
!show
!clear
!stop
!limit[# of posts]
!top [subreddit] [filter]
!hot [subreddit]
!new [subreddit]
!stream [subreddit]
```

!allcommands: 
Shows all available commands that you can use

!add: 
You can add a keyword so that !stream will only send posts that have the keywords in the title

!show:  
Shows all the keywords

!clear: 
Clears all the keywords

!stop: 
Stops !stream

!limit:  
You can limit the number of posts that !top, !hot, and !new send

!top: 
Displays all the top posts of a specific subreddit during a specific time

!hot: 
Displays hot posts of a specific subreddit

!new:
Displays the newest posts of a specific subreddit

!stream: 
Displays the newest posts of a subreddit and updates in real time whenever a new post is created. Once a new post is created, the bot will @ the users in the 'Notify' role. Additionally, if keywords are added, the bot will only send posts to the chat that have keywords in the reddit post title. This command will run forever until the user tells it to stop by using the command !stop

## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See LICENSE for more information.
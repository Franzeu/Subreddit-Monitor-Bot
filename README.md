# RedditPosts-Bot
RedditPosts Bot is a Discord bot that retreives reddit submissions and streams it in real time.

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

## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See LICENSE for more information.

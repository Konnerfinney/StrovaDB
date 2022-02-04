import os
from keep_alive import keep_alive
from discord.ext import commands
import cogs
import os
# from dotenv import load_dotenv

# load_dotenv(dotenv_path = "env/.env")
DISCORD_BOT_SECRET = os.environ.get('DISCORD_BOT_SECRET')

bot = commands.Bot(
	command_prefix="!",  
	case_insensitive=True  
)

bot.author_id = 277964604771008515  
@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	'cogs.dev_commands', 
	'cogs.scheduling',
	'cogs.admin'
]

if __name__ == '__main__':  # Ensures this is the file being ran
	print("loading cogs")
	for extension in extensions:
		bot.load_extension(extension)  # Loads every extension.

bot.run(DISCORD_BOT_SECRET)  # Starts the bot
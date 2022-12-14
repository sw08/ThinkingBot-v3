import config
import discord
from discord.ext import commands
from os import listdir

if config.BOT.debug_mode:
    prefix = config.BOT.test_prefix
    token = config.BOT.test_token
else:
    prefix = config.BOT.prefix
    token = config.BOT.token

bot = commands.Bot(
    command_prefix=prefix,
    intents=discord.Intents.all(),
    help_command=None,
    owner_ids=config.BOT.owner_ids,
)

bot.load_extension("jishaku")
print("Succeeded to load extension\t: Jishaku")

for i in [i for i in sorted(listdir("./Cogs/")) if i[-3:] == ".py"]:
    print(i)
    try:
        bot.load_extension(f"Cogs.{i[:-3]}")
        print(f"Succeeded to load extension\t: Cogs.{i[:-3]}")
    except Exception as error:
        print(f"Failed to load extension\t: Cogs.{i[:-3]}")
        print(error)

bot.run(token)

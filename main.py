
from interactions.api.http import HTTPClient
from interactions.client import Client

from resources import ids, components
import botconfig

import interactions
print("Interactions Imported...")

secret = botconfig.load_secret("C:/Dworv Stuff/Coding/Downfall-4.0/botconfig.toml", "key")
bot = Client(token=secret)
print("Bot Initiated...")

http: HTTPClient = bot.http



print("Commands Defined...")
bot.start()
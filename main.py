
from interactions.api.http import HTTPClient
from interactions.client import Client

from resources import ids, components

import interactions
print("Interactions Imported...")

bot: Client = interactions.Client(token="OTA5NTE5NDAyNTE5NjU0NDcx.YZFd8w.XDfxvl9WKuJAi2yPMltXIcok5C8")
print("Bot Initiated...")

http: HTTPClient = bot.http



print("Commands Defined...")
bot.start()
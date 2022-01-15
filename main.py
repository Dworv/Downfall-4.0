
from datetime import datetime
from interactions.api.http import HTTPClient
from interactions.api.models.message import Embed, EmbedFooter
from interactions.api.models.user import User
from interactions.client import Client
from interactions.context import CommandContext
from model import application
from resources import ids, components, verifyer
import botconfig
import interactions
from resources.misc import ErrorEmbed, RichEmbed
print("Interactions Imported...")

secret = botconfig.load_secret("C:/Dworv Stuff/Coding/Downfall-4.0/botconfig.toml", "key")
bot: Client = Client(token=secret)
print("Bot Initiated...")

http: HTTPClient = bot.http

@bot.command(name = 'apply',
    description = 'The command used to apply for Downfall Editing',
    scope = ids.server,
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="link",
            description="The link to your application to the team",
            required=True,
            ),
        interactions.Option(
            type=interactions.OptionType.BOOLEAN,
            name="prerecs",
            description="Did you use pre-prepared clips?",
            required=True
            )
        ]
    )
async def apply(
    ctx: CommandContext, 
    link: str, 
    prerecs: bool
    ):
    await ctx.defer(ephemeral = True)

    url_error = verifyer.url(link)
    if url_error:
        embed = ErrorEmbed('URL', verifyer.VerificationStatus.ver_msg[url_error]).embed
        await ctx.send(ephemeral = True, embeds = embed)
        return

    ap: application = application.new(
        user_id = int(ctx.author.user.id),
        url = link,
        prerecs = prerecs
    )
    embed = RichEmbed(
        title = 'Application Success!',
        description = f'You applied to the Downfall Editing team!\n\n```Ticket: {ap.ticket}\nUrl: {link}```',
        expression = RichEmbed.Expression.celebration,
        footer = None
        ).embed
    await ctx.send(embeds = embed, ephemeral = True)



print("Commands Defined...")
bot.start()
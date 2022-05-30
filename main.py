
from unicodedata import name
from interactions.api.models.message import Message
from interactions.client import Client
from interactions.context import CommandContext
from resources.sql import Application, Editor, InfoChannel
import interactions

print("Interactions Imported...")

from resources import ids, components, verifyer
from resources.misc import ErrorEmbed, InfoEmbeds, RichEmbed
import botconfig

secret = botconfig.load_secret("C:/Dworv Stuff/Coding/Downfall-4.0/botconfig.toml", "key")
bot: Client = Client(token=secret)
print("Bot Initiated...")

# listeners
@bot.event
async def on_message_create(msg: Message):
    if 'hi' in msg.content or 'Hi' in msg.content or 'HI' in msg.content: # lmfaooo for the memes
        await bot.http.create_message({'content': 'hello'}, msg.channel_id)

# apply command
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

    if url_error := verifyer.url(link):
        embed = ErrorEmbed('URL', verifyer.VerificationStatus.ver_msg[url_error]).embed
        await ctx.send(ephemeral = True, embeds = embed)
        return

    ap: Application = Application.new(
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

# info-channel commands
@bot.command(name = "info-channel",
    description = "Your Friendly Neighboorhood Info Channel Command!",
    scope = ids.s,
    options=[
        interactions.Option(
            type=interactions.OptionType.SUB_COMMAND,
            name="new",
            description="For Creating New Info Channels",
            options=[
                interactions.Option(
                type=interactions.OptionType.CHANNEL,
                name="channel",
                description="Only use on Announcement Channels",
                required=True
                    )
                ]
            ),
        interactions.Option(
            type=interactions.OptionType.SUB_COMMAND,
            name="delete",
            description="For Deleting Old Info Channels",
            options=[
                interactions.Option(
                type=interactions.OptionType.CHANNEL,
                name="channel",
                description="Only use on Announcement Channels",
                required=True
                    )
                ]
            ),
        interactions.Option(
            type=interactions.OptionType.SUB_COMMAND,
            name="edit",
            description="InfoChannel editor",
            options=[
                interactions.Option(
                    type=interactions.OptionType.CHANNEL,
                    name="channel",
                    description="Only use on Announcement Channels",
                    required=True
                    ),
                interactions.Option(
                    type=interactions.OptionType.INTEGER,
                    name="section",
                    description="The section to edit (0 for title)",
                    required=True
                    ),
                interactions.Option(
                    type=interactions.OptionType.STRING,
                    name="title",
                    description="Pick the title of the section (or the whole thing if section is 0)"
                    ),
                interactions.Option(
                    type=interactions.OptionType.STRING,
                    name="content",
                    description="The content of the entry (does nothing if editing 0)"
                    )
                ]
            ),
        ]
    )
async def infochannel(
    ctx: CommandContext, 
    sub_command: str, 
    channel, 
    section = None, 
    title = None, 
    content = None
    ):

    channel_id = channel
    channel = await bot.http.get_channel(channel)
    match sub_command:
        case('new'):
            embed = RichEmbed(
                title = "Info Channel Created!",
                description = f"You have created a new Info Channel in <#{channel_id}>",
                expression = RichEmbed.Expression.success
                ).embed
            await ctx.send(embeds=embed)
            embeds = InfoEmbeds().embeds
            await bot.http.send_message(embeds = embeds, channel_id = channel_id, content = "Bruh")
        case('delete'):
            pass
        case('edit'):
            pass

print("Commands Defined...")
bot.start()
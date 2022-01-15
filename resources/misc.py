
from ast import Expression
from datetime import datetime
import interactions
from typing import Optional
from interactions.api.models.message import EmbedFooter
from interactions.api.models.user import User
from async_class import AsyncClass, AsyncObject, task, link

class RichEmbed():
    def __init__(
        self,
        title: str,
        description: str,
        expression: Optional[dict] = None,
        url: Optional[str] = None,
        footer: Optional[str] = None
        ):

        self.title = title if not expression or not title else expression['emoji'] + ' ' + title
        self.description = description
        self.expression = expression if expression else Expression.confusion
        footer_append = f' · {footer}' if footer else ''
        self.footer = EmbedFooter(
            text = 'Downfall Editing' + footer_append,
            icon_url = 'https://i.imgur.com/nEatfh9.png'
            )
        self.embed = interactions.Embed(
            title = self.title,
            description = self.description,
            color = self.expression['color'],
            timestamp = str(datetime.now()),
            footer = self.footer
            )

    class Expression:
        success = {
            'name': 'success',
            'emoji': '✅',
            'color': int('00FF00', 16)
            }
        failure = {
            'name': 'failure',
            'emoji': '❌',
            'color': int('FF0000', 16)
            }
        celebration = {
            'name': 'celebration',
            'emoji': '🎊',
            'color': int('FFC0CB', 16)
            }
        confusion = {
            'name': 'confusion',
            'emoji': '❔',
            'color': int('FFFF00', 16)
            }
        happy = {
            'name': 'happy',
            'emoji': '🙂',
            'color': int('FFA500', 16)
            }
        sad = {
            'name': 'sad',
            'emoji': '😢',
            'color': int('FFFF00', 16)
            }

class ErrorEmbed:
    def __init__(self,
        type: str = 'Interaction', 
        description: str = 'An unknown error occured.',
        ):
        self.type = type
        self.title = type + ' Error'
        self.desciption = description
        self.footer = EmbedFooter(
            text = f'Downfall Editing · {self.title}',
            icon_url = 'https://i.imgur.com/nEatfh9.png'
        )
        self.embed = interactions.Embed(
            title = self.title,
            description = self.desciption,
            timestamp = str(datetime.now()),
            color = int('FF0000', 16),
            footer = self.footer
        )
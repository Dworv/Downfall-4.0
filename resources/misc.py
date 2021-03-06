
from datetime import datetime
import interactions
from typing import Optional
from interactions.api.models.message import EmbedFooter, Embed
from interactions.api.models.user import User

class RichEmbed():
    def __init__(
        self,
        title: str,
        description: str,
        expression: Optional[dict] = None,
        url: Optional[str] = None,
        footer: Optional[str] = None
        ):

        self.title = title if not expression or not title else expression['emoji'] + '  ' + title
        self.description = description
        self.expression = expression or __class__.Expression.confusion
        footer_append = f' ยท {footer}' if footer else ''
        self.footer = EmbedFooter(
            text = 'Downfall Editing' + footer_append,
            icon_url = 'https://i.imgur.com/nEatfh9.png'
            )
        self.embed = Embed(
            title = self.title,
            description = self.description,
            color = self.expression['color'],
            timestamp = str(datetime.now()),
            footer = self.footer
            )

    class Expression:
        success = {
            'name': 'success',
            'emoji': 'โ',
            'color': int('00FF00', 16)
            }
        failure = {
            'name': 'failure',
            'emoji': 'โ',
            'color': int('FF0000', 16)
            }
        celebration = {
            'name': 'celebration',
            'emoji': '๐',
            'color': int('FFC0CB', 16)
            }
        confusion = {
            'name': 'confusion',
            'emoji': 'โ',
            'color': int('FFFF00', 16)
            }
        happy = {
            'name': 'happy',
            'emoji': '๐',
            'color': int('FFA500', 16)
            }
        sad = {
            'name': 'sad',
            'emoji': '๐ข',
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
            text = f'Downfall Editing ยท {self.title}',
            icon_url = 'https://i.imgur.com/nEatfh9.png'
            )
        self.embed = Embed(
            title = self.title,
            description = self.desciption,
            timestamp = str(datetime.now()),
            color = int('FF0000', 16),
            footer = self.footer
            )

class InfoEmbeds:
    def __init__(self, title: str = None, entries: list = None):
        self.title: str = title or 'No Title'
        self.entries: list = entries
        self.color: int = int('3e047b', 16) # make gradient later lmao
        self.footer = EmbedFooter(
            text = f'Downfall Editing ยท {self.title}',
            icon_url = 'https://i.imgur.com/nEatfh9.png'
            )
        self.embeds = [Embed(title = self.title, color = self.color)]
        if entries:
            for name, content in entries[:-1]:
                self.embeds.append(
                    Embed(
                        title = name,
                        description = content,
                        color = self.color
                        )       
                    )
            self.embeds.append(
                Embed(
                    title = entries[-1][0],
                    description = entries[-1][1],
                    color = self.color,
                    footer = self.footer
                    )
                )
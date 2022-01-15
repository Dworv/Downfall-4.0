
import requests, validators

def url(url: str) -> int:

    rickrolls = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'https://www.youtube.com/watch?v=sXwaRjU7Tj0',
        'https://www.youtube.com/watch?v=iik25wqIuFo',
        'https://www.youtube.com/watch?v=QtBDL8EiNZo',
        'https://www.youtube.com/watch?v=xvFZjo5PgG0',
        'https://www.youtube.com/watch?v=a3Z7zEc7AXQ'
        ]

    if [x for x in rickrolls if x in url]:
        return VerificationStatus.RICKROLL
        
    if validators.url('https://' + url):
        return VerificationStatus.MISSING_HTTPS

    if not validators.url(url):
        return VerificationStatus.UNKNOWN_LINK

    try:
        requests.get("http://www.google.com/")
    except requests.ConnectionError:
        return VerificationStatus.UNKNOWN_LINK

    accepted_streamers = ['youtube', 'streamable', 'discordapp']
    if not [x for x in accepted_streamers if x in url]:
        return VerificationStatus.WRONG_SERVICE
        
    return VerificationStatus.REAL
    

class VerificationStatus:
    REAL = 0
    RICKROLL = 1
    MISSING_HTTPS = 2
    WRONG_SERVICE = 3
    UNKNOWN_LINK = 4

    ver_msg = {
        1: "You dare rickroll a discord bot? FOOL!",
        2: "You didn't copy the https from the link...",
        3: "That doesn't look like a YouTube or Streamable link...",
        4: "That link is not valid..."
        }

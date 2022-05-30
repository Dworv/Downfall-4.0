
import sqlite3
from datetime import datetime
from typing import Union
from json import dumps, loads

d = sqlite3.connect("downfall.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
c = d.cursor()

class OfYear:
    month_days = [
        0, 
        31, 28, 31, 
        30, 31, 30, 
        31, 31, 30, 
        31, 30, 31
        ]
    month_names = [
        0, 
        "January","Febuary","March",
        "April","May","June",
        "July","August","September",
        "October","November","December"
        ]

    def __init__(self, month: int, day: int):
        self.month = month
        self.day = day
        self.month_name = __class__.month_names[month]

        self.days_into_year = sum(__class__.month_days[i] for i in range(1,month))
        self.days_into_year += day

    def __repr__(self):
        return (f"{self.month};{self.day}")

    def next_unix(self):
        now = datetime.now()
        today = __class__.convert(now.strftime("%m;%d"))
        if self.days_into_year > today.days_into_year:
            then = datetime(now.year, self.month, self.day, 4)
        else:
            then = datetime(now.year+1, self.month, self.day, 4)
        return int(then.timestamp())

    def convert(self):
        if self != None:
            arg_list = self.split(";")
            return OfYear(int(arg_list[0]), int(arg_list[1]))
    
    def discord_ts(self, type):
        return f"<t:{self}:{type}>"

    class TimestampType:
        
        SHORT_TIME = "t"
        LONG_TIME = "T"
        SHORT_DATE = "d"
        LONG_DATE = "D"
        SHORT_DT = "f"
        LONG_DT = "F"
        RELATIVE = "R"

class Editor:
    def __init__(self, id: int):
        c.execute("SELECT * FROM roster WHERE user_id = (?)", [id])
        _db_info = c.fetchone()
        self.id = int(_db_info[0])
        self.rank = int(_db_info[1])
        self.subtext = _db_info[2]
        self.youtube = _db_info[3]
        self.custom_name = _db_info[4]
        self.birthday = OfYear.convert(_db_info[5])

        self.has_subtext = self.subtext is not None
        self.has_youtube = self.youtube is not None
        self.has_custom_name = self.custom_name is not None
        self.has_birthday = self.birthday is not None
    
    def set_rank(self, rank: int):  # sourcery skip: class-extract-method
        if rank != self.rank:
            c.execute("UPDATE roster SET rank = (?) WHERE user_id = (?)", [rank, self.id])
            d.commit()
            self.rank = rank
    
    def set_subtext(self, subtext: str):
        if subtext != self.subtext:
            c.execute("UPDATE roster SET subtext = (?) WHERE user_id = (?)", [subtext, self.id])
            d.commit()
            self.subtext = subtext
            self.has_subtext = True

    def set_youtube(self, youtube: str):
        if youtube != self.youtube:
            c.execute("UPDATE roster SET youtube = (?) WHERE user_id = (?)", [youtube, self.id])
            d.commit()
            self.youtube = youtube
            self.has_youtube = True

    def set_custom_name(self, custom_name: str):
        if custom_name != self.custom_name:
            c.execute("UPDATE roster SET custom_name = (?) WHERE user_id = (?)", [custom_name, self.id])
            d.commit()
            self.custom_name = custom_name
            self.has_custom_name = True

    def set_birthday(self, birthday):
        if birthday != self.birthday:
            c.execute("UPDATE roster SET birthday = (?) WHERE user_id = (?)", [birthday, self.id])
            d.commit()
            self.birthday = birthday
            self.has_birthday = True

    def remove(self):
        c.execute("DELETE FROM roster WHERE user_id = (?)", [self.id])
        d.commit()

    def new(self, rank: int, subtext: str = None, youtube: str = None, custom_name: str = None, birthday: OfYear = None):
        c.execute(
            "INSERT INTO roster VALUES (?,?,?,?,?,?)",
            [self, rank, subtext, youtube, custom_name, birthday],
        )

        d.commit()
        return Editor(self)

    def get(self):
        c.execute("SELECT * FROM roster WHERE user_id = (?)", [self])
        return Editor(self) if c.fetchone() else None

    class ServerRank:
        TRIAL = 1
        MEMBER = 2
        MEMPERPLUS = 3
        REVIEWER = 4
        OWNER = 5

class Application:
    def __init__(self, ticket: int):
        c.execute("SELECT * FROM applications WHERE ticket = (?)", [ticket])
        _db_info: list = c.fetchone()
        self.ticket: int = int(_db_info[1])
        self.status: int = int(_db_info[2])
        self.url: str = _db_info[3]
        self.prerecs: bool = bool(_db_info[4])
        self.appdate: datetime = _db_info[5]
        self.revdate: Union[datetime, None] = _db_info[6]

    def new(self, url: str, prerecs: bool):
        c.execute(
            "INSERT INTO applications (user_id, status, url, prerec, appdate) VALUES (?, ?, ?, ?, ?)",
            [self, -1, url, int(prerecs), datetime.now()],
        )

        d.commit()
        return Application(c.lastrowid)

    def get(self):
        c.execute("SELECT * FROM applications WHERE ticket = (?)", [self])
        return Application(self) if c.fetchone() else None

    class AcceptStatus:
        PENDING = -1
        REAPP = 0
        TRIAL = 1
        MEMBER = 2
        MEMPERPLUS = 3

class InfoChannel:
    def __init__(self, channel_id: int):
        c.execute("SELECT * FROM infochannels WHERE id = (?)", [channel_id])
        _db_info = c.fetchone()

        self.channel_id: int = channel_id
        self.title: str = _db_info[1]
        self.entries: list = loads(_db_info[2])

    def add_entry(self, location: int, title: str, content: str):
        self.entries.insert(location, [title, content])
        c.execute("UPDATE infochannels SET entries = ? WHERE id = ?", [dumps(self.entries), self.channel_id])
        d.commit()

    def edit_entry(self, location: int, title: str = None, content: str = None):
        old = self.entries[location]
        new = [
            title or old[0],
            content or old[1]
        ]
        self.entries[location] = new
        c.execute("UPDATE infochannels SET entries = ? WHERE id = ?", [dumps(self.entries), self.channel_id])
        d.commit()

    def remove_entry(self, location: int):
        self.entries.pop(location)
        c.execute("UPDATE infochannels SET entries = ? WHERE id = ?", [dumps(self.entries), self.channel_id])
        d.commit()

    def edit_title(self, title: str):
        self.title = title
        c.execute("UPDATE infochannels SET title = ? WHERE id = ?", [self.title, self.channel_id])
        d.commit()

    def switch_channel(self, channel_id: int):
        self.channel_id = channel_id
        c.execute("UPDATE infochannels SET id = ? WHERE id = ?", [self.channel_id, self.channel_id])
        d.commit()

    def new(self, title: str):
        c.execute("INSERT INTO infochannels VALUES (?, ?, NULL)", [self, title])
        d.commit()
        return InfoChannel(self)

    def get(self):
        c.execute("SELECT * FROM infochannels WHERE id = (?)", [self])
        if c.fetchall():
            return InfoChannel(self)

    def delete(self):
        c.execute("DELETE * FROM infochannels WHERE id = (?)", [self])

    class EntryType:
        PARAGRAPH = 1
        BULLETS = 2


import sqlite3
from datetime import datetime

from interactions.api.models.message import Embed


d = sqlite3.connect("downfall.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
c = d.cursor()

class of_year:
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

        self.days_into_year = 0
        for i in range(1,month):
            self.days_into_year += __class__.month_days[i]
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

    def convert(arg):
        if arg != None:
            arg_list = arg.split(";")
            return of_year(int(arg_list[0]), int(arg_list[1]))
    
    def discord_ts(unix: int, type):
        return f"<t:{unix}:{type}>"

    class dc_ts_types:
        
        short_time = "t"
        long_time = "T"
        short_date = "d"
        long_date = "D"
        short_dt = "f"
        long_dt = "F"
        relative = "R"

class editor:
    def __init__(self, id: int):
        c.execute("SELECT * FROM roster WHERE user_id = (?)", [id])
        db_info = c.fetchone()
        self.id = int(db_info[0])
        self.rank = int(db_info[1])
        self.subtext = db_info[2]
        self.youtube = db_info[3]
        self.custom_name = db_info[4]
        self.birthday = of_year.convert(db_info[5])

        if self.subtext == None: self.has_subtext = False
        else: self.has_subtext = True
        if self.youtube == None: self.has_youtube = False
        else: self.has_youtube = True
        if self.custom_name == None: self.has_custom_name = False
        else: self.has_custom_name = True
        if self.birthday == None: self.has_birthday = False
        else: self.has_birthday = True
    
    #basic
    def set_rank(self, rank: int):
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

    #other
    def new(id: int, 
            rank: int, 
            subtext: str = None, 
            youtube: str = None, 
            custom_name: str = None, 
            birthday: of_year = None
            ):
        c.execute(
            "INSERT INTO roster VALUES (?,?,?,?,?,?)", 
            [id, rank, subtext, youtube, custom_name, birthday]
            )
        d.commit()
        return editor(id)

    def get(id: int):
        c.execute("SELECT * FROM roster WHERE user_id = (?)", [id])
        if c.fetchone():
            return editor(id)
        else: 
            return None

    class server_rank:
        trial = 1
        member = 2
        memberplus = 3
        reviewer = 4
        owner = 5

class application:
    def __init__(self, ticket: int):
        c.execute("SELECT * FROM applications WHERE ticket = (?)", [ticket])
        db_info = c.fetchone()
        self.ticket = int(db_info[0])
        self.user_id = int(db_info[1])
        self.status = int(db_info[2])
        self.url = db_info[3]
        self.prerec = bool(db_info[4])
        self.appdate = db_info[5]
        self.revdate = db_info[6]

    def new(user_id: int, url: str, prerec: bool):
        insert = c.execute(
            "INSERT INTO applications (user_id, status, url, prerec, appdate) VALUES (?, ?, ?, ?, ?)",
            [user_id, -1, url, int(prerec), datetime.now()]
        )
        d.commit()
        print(insert)
    
    def get(ticket: int):
        c.execute("SELECT * FROM applications WHERE ticket = (?)", [ticket])
        if c.fetchone():
            return application(ticket)
        else: 
            return None

    class accept_status:
        pending = -1
        reapp = 0
        trial = 1
        member = 2
        memberplus = 3

def build_embed(title: str, content: str, express: int = None):
    embed = Embed(
        title = title,
        description = content,
        color = 0x800080,
    )
    return embed
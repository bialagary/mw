from modules import client
import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.nbafullgames', sys.argv)

class atdhe():
    def __init__(self):
        self.base = 'http://goatd.net/'
        self.html = client.request(self.base)

    def get_basketball_events(self):
        reg = re.compile('<td width="26px" height="13px"><img src=".+?basketball.gif" width="13" height="13" /></td>\s*<td width="400px"  align="left"><b><a href="(.+?)" title=".+?" target="_blank">(.+?)</a></b><font style="font-size: 8px;"> </font></td>\s*<td align="right"><b>(.+?)</b></td><td align="left"><b>(.+?)</b></td>')
        events = re.findall(reg,self.html)
        events = self.__prepare_events(events)
        return events

    @staticmethod
    def convert_time(time):
        li = time.split(':')
        hour,minute=li[0],li[1]
        import datetime
        from modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,events):
        new = []
        for event in events:
            url = self.base + event[0]
            title = event[1]
            time = self.convert_time(event[2])
            title = '[COLOR orange](%s)[/COLOR] %s'%(time,title)
            new.append((url,title))

        return new
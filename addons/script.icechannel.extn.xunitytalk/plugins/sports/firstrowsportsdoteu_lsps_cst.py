'''
    Ice Channel
    firstrowsports.eu
'''

# GMT + 5
# print (datetime.datetime.strptime('03:55', '%H:%M') + datetime.timedelta(hours=5)).time()

from entertainment.plugnplay.interfaces import SportsSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class firstrowsportsdoteu(SportsSource, CustomSettings):
    implements = [SportsSource, CustomSettings]
    
    name = "firstrowsports.eu"
    display_name = "FirstRow Sports"
    source_enabled_by_default = 'true'
    
    source_time_zone = 1
    
    base_url = 'http://firstrowus1.eu'
    
    source_sports_list = ['americanfootball', 'basketball', 'football', 'golf', 'icehockey', 'rugby', 'tennis']
    
    source_sports_urls = {
        'americanfootball' : '/sport/american-football.html',
        'basketball' : '/sport/basketball.html',
        'football' : '/sport/football.html',
        'golf' : '/sport/golf.html',
        'icehockey' :  '/sport/ice-hockey.html',
        'rugby' :  '/sport/rugby.html',
        'tennis' :  '/sport/tennis.html'
        }
        
    #timezone_cookie = 'vipstand_timezone=00%3A00'
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_url" type="labelenum" label="URL" default="http://firstrowus1.eu" values="Custom|http://firstrowus1.eu|http://firstrowsports.unblocked.co" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
    def get_url(self):
        custom_url = self.Settings().get_setting('custom_url')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            custom_url = ('http://' + custom_url)
        if custom_url.endswith('/'):
            custom_url = custom_url[:-1]
        return custom_url
        
    def GetSportsContent(self, indexer, type, list, lock, message_queue): 
    
        sport_url = self.get_url() + self.source_sports_urls[type]
        
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(sport_url ).content
        
        import re
        
        for item in re.finditer("(?s)<h3>.+?alt=['\"](.+?)['\"].+?<span>(.+?)</span>.+?href=['\"](/watch/.+?)['\"]", content):
            
            title = item.group(1)
            
            start_time = re.search( '"matchtime">(.*)', item.group(2) )
            if not start_time:
                continue
            import datetime
            start_time = datetime.date.today().strftime('%Y %m %d ') + start_time.group(1)
            
            url = self.get_url() + item.group(3)
            
            self.AddSportsContent(list, indexer, type, common.mode_File_Hosts, title, start_time=start_time, url=url )
            
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        from entertainment.net import Net
        net = Net()        
        
        content = common.unescape(common.str_conv(net.http_GET(url).content))

        import re
        for link in re.finditer(r"href='(/watch/.+?)'>(.+?)</a>", content):
            if link.group(2).startswith('</a>'):
                continue
            self.AddLiveLink(list, link.group(2), self.get_url() + link.group(1))
            
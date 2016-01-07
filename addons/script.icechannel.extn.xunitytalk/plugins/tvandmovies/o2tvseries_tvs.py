'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch

class o2tvseries(TVShowSource):
    implements = [TVShowSource]
    
    name = "o2tvseries"
    display_name = "o2 Tv Series"
    base_url = 'http://www.o2tvseries.com'
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
    
        import re        
        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
                
        media_url = re.compile('<a href="(.+?)">(.+?)</a> <span class="count">.+?Downloads\)</span>',re.DOTALL).findall(content)
        for show,codec in media_url:
            if codec.endswith('mp4'):
                self.AddFileHost(list, 'HD', show)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        if len(episode)< 2:
            episode = '0'+episode.replace(' ','-')
        if len(season)< 2:
            season = '0'+season.replace(' ','-')    
        season='Season-'+season
        episode='Episode-'+episode
        tv_url='http://o2tvseries.com/%s/%s/%s/index.html'%(name.replace(' ','-'),season,episode)
        
        self.GetFileHosts(tv_url, list, lock, message_queue)
                
            
    def Resolve(self, url):

        return url
            
                

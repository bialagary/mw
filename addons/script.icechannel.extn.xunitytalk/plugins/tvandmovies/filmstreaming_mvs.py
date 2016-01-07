'''
    Ice Channel
    Film-Streaming
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class filmstreaming(MovieSource):
    implements = [MovieSource]
    
    name = "Film-Streaming"
    display_name = "Film-Streaming"
    base_url = 'http://film-streaming.in'
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net()        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','+')+'+'+year
        
        import re
        url=self.base_url+'/?s='+search_term
        link=net.http_GET(url).content
        if not 'I am sorry, what are you looking for' in link:        
            match = re.compile('<h2><a href="(.+?)" title="(.+?)"').findall(link)

            for movie_url, TITLE in match:
                if year in TITLE:
                    self.GetFileHosts(movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re
        import urllib
        from entertainment.net import Net
        net = Net()
 
        link = net.http_GET(url).content
        if 'https://www.cloudy.ec/embed.php?' in link:
            match = re.compile('https://www.cloudy.ec/embed.php\?id=(.+?)"').findall(link)[0]

            html = net.http_GET('https://www.cloudy.ec/embed.php?id=' +match).content

            key=re.compile('flashvars.filekey="(.+?)"').findall(html)[0]

            api='http://www.cloudy.ec/api/player.api.php?&file=%s&key=%s'%(match,key.replace('.', '%2E'))
     
            content =net.http_GET(api).content
            
            resolved_media=re.compile('url=(.+?)&title').findall(content)[0]
            
            return urllib.unquote(resolved_media)
        
        elif 'http://letwatch.us/embed-' in link:

            match = re.compile('http://letwatch.us/embed-(.+?)"').findall(link)[0]
      
            html = net.http_GET('http://letwatch.us/embed-' +match).content
            
            FILE=re.compile('file:"(.+?)",label:"(.+?)"').findall(html)
  
            resolved_media=FILE[len(FILE)-1][len(FILE)-2]
   
            
            return resolved_media            
        else:return ''               
                

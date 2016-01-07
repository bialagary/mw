'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class onlinemovies(MovieSource):
    implements = [MovieSource]
    
    name = "Online Movies"
    display_name = "Online Movies"

    base_url='http://onlinemoviespro.me'
    
    source_enabled_by_default = 'true'
    
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

            
        self.AddFileHost(list, res, url)

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
                

        movie_url = self.base_url+'/'+name.lower().replace(' ','-')+'-'+year

        
        try:            
            content = net.http_GET(movie_url).content
        except:
            from entertainment import cloudflare            
            content = cloudflare.solve(movie_url)
                  
        
        match=re.compile("iframe.php\?ref=(.+?)&").findall(content)
        
       
        for ID in match:
            

            self.GetFileHosts('http://videomega.tv/iframe.php?ref='+ID, list, lock, message_queue,'HD')



 
        

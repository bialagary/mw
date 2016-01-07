'''
    http://afdah.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch



class moviefarsi(MovieSource):
    implements = [MovieSource]
    
    name = "Moviefarsi"
    display_name = "Moviefarsi"
    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):
        if '720' in url:
            quality ='720P'
            if '3d' in url.lower():
                quality = '3D'
        elif '1080' in url:
            quality ='1080P'
            if '3d' in url.lower():
                quality = '3D'            
        else:
            if '3d' in url.lower():
                quality = '3D'            
            quality='HD'
        self.AddFileHost(list, quality, url)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='/Apple iPhone')
        name = self.CleanTextForSearch(name)
         
        search_term = name.lower().replace(':','')
        helper_term = ''
        ttl_extrctr = ''

        search = 'https://google.co.uk/search?q=%s'  % search_term.replace(' ','+')+'+site%3Ahttp%3A%2F%2Fdl4.moviefarsi.com'
        contents= net.http_GET(search).content
        match1=re.compile('<a href="\/url\?q=(.+?)&.+?">(.+?)</a>').findall(contents)
        for movie_url , name in match1:
            if 'Index of' in name:             
                content= net.http_GET(movie_url).content

                match=re.compile('<a href="(.+?)">').findall(content)
                for URL in match:
                    if search_term.replace(' ','.') in URL.lower():
                        MOVIE =movie_url+URL
                        if year in MOVIE.lower():
                            self.GetFileHosts(MOVIE, list, lock, message_queue)



    def Resolve(self, url):

        return url

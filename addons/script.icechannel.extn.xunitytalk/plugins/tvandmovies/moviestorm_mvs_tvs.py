'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
from BeautifulSoup import BeautifulSoup as soup

class moviestorm(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
    
    name = "MovieStorm"
    display_name = "Movie Storm"

    base_url='http://moviestorm.eu'
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue,res,host):
        if 'CAM' in res:
            res='LOW'
        elif 'HD' in res:
            res='HD'
        elif 'DVD' in res:
            res='DVD'
        elif 'BRRip' in res:
            res='HD'
        elif 'R5' in res:
            res='DVD'
        elif '3D' in res:
            res='3D'
        else:
            res='SD'            
        self.AddFileHost(list, res, url,host=host.upper())
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 

        
        if type == 'tv_episodes':
            search_term = '%s</h1>'%(re.sub('\A(a|A|the|THE|The)\s','',name))
            episode_get = '?season=%s&episode=%s#searialinks'%(season,episode)

            movie_url = 'http://moviestorm.eu/search'
            data={'q':name,'go':'Search'}         
            content = net.http_POST(movie_url,data).content
            
            html=content.split('<div class="movie_box">')
            
            for p in html:
                if search_term in p:
                    
                    match=re.compile('<a href="(.+?)"').findall(p)
                    for url in match:
                        if 'http://moviestorm.eu/view' in url:
                            
                            new_tv_url= url+episode_get
                            
                            link = net.http_GET(new_tv_url).content

                            quality=link.split('<td class="quality_td">')
                            for p in quality:
                                res= p.split('</td>')[0]
                                ep=re.compile('<a target="_blank" href="(.+?)">WATCH</a>').findall(p)
                                host=re.compile('data-host="(.+?)"').findall(p)[0]
                                for episode_link in ep:
                            
                                    self.GetFileHosts(episode_link,list, lock, message_queue,res,host)
                            
                
            

                

            
        elif type == 'movies':
            name = name.rstrip()
            search_term = '%s</h1>'%(re.sub('\A(a|A|the|THE|The)\s','',name))
            movie_url = 'http://moviestorm.eu/search'
            data={'q':name,'go':'Search'}         
            content = net.http_POST(movie_url,data).content
        
            html=content.split('<div class="movie_box">')
            
            for p in html:
                if search_term in p:
                    
                    new_url=re.compile('<a href="(.+?)"').findall(p)[0]
                        
                    if 'http://moviestorm.eu/view' in new_url:
                        
                        link = net.http_GET(new_url).content
                        quality=link.split('<td class="quality_td">')
                        for p in quality:
                            res= p.split('</td>')[0]
                            try:
                                movie_link=re.compile('href="(.+?)">WATCH</a>').findall(p)[0]
                                host=re.compile('data-host="(.+?)"').findall(p)[0]
                                self.GetFileHosts(movie_link, list, lock, message_queue,res,host)
                            except:pass                                        
                                
                    
                
    def Resolve(self, url):
        import re
        from entertainment.net import Net
        
        net = Net(cached=False)

                                
        if 'http://moviestorm.eu/exit/' in url:
            link2 = net.http_GET(url).content
            url=re.compile('<a class="real_link" href="(.+?)"').findall(link2)[0]
      

        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url        

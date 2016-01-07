'''
    Ice Channel
    simplymovies.net
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class watch_tvseries(TVShowSource):
    implements = [TVShowSource]
    
    name = "Watch Tv Series"
    display_name = "Watch Tv Series"
    base_url = 'http://www.watch-tvseries.net'
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        quality_dict = {'1080':'HD', '720':'HD', '540':'SD', '480':'SD', '360':'LOW', '240':'LOW'}
        
        content = net.http_GET(url).content
        r = '\+updv\+"(.+?)"'
        match  = re.compile(r).findall(content)[0]
        
        
        
        content = net.http_GET('http://www.watch-tvseries.net/play/plvids'+match).content      
        r ='src="(.+?)"'
        FINAL_URL  = re.compile(r).findall(content)[0]
        
        if 'mail.ru' in FINAL_URL:
            matchme=re.compile('"metadataUrl":"(.+?)"').findall(net.http_GET(FINAL_URL).content)[0]
            self.GrabMailRu(matchme,list)
                
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name
        if len(episode)< 2:
            episode = '0'+episode
        if len(season)< 2:
            season = '0'+season
        helper_term = 's%se%s' % (season,episode)

    
        import re
        from entertainment.net import Net
        net = Net()
        tv_url = self.base_url+ '/play/menulist'
        
        content = net.http_GET(tv_url).content
        match = re.compile("<li><a href='(.+?)'>(.+?)<").findall(content)
        
        for url, title in match:
            if search_term.lower() in title.lower():
                if not 'http' in url:
                    url=self.base_url+url
                content = net.http_GET(url).content
                link =content.split('href')
                
                for p in link:
                    if helper_term in p:
                        get_url=re.compile('="(.+?)">').findall (p) [0]
                        
                        self.GetFileHosts(self.base_url+get_url, list, lock, message_queue)
            
            
    def GrabMailRu(self,url,list):
        print 'RESOLVING VIDEO.MAIL.RU VIDEO API LINK'
        
        from entertainment.net import Net
        net = Net(cached=False)

        
        import json,re
        items = []

        data = net.http_GET(url).content
        cookie = net.get_cookies()
        for x in cookie:

             for y in cookie[x]:

                  for z in cookie[x][y]:
                       
                       l= (cookie[x][y][z])
                       
        r = '"key":"(.+?)","url":"(.+?)"'
        match = re.compile(r,re.DOTALL).findall(data)
        for quality,stream in match:
            test = str(l)
            test = test.replace('<Cookie ','')
            test = test.replace(' for .my.mail.ru/>','')
            url=stream +'|Cookie='+test
            QUALITY=quality.upper()
            if '480' in QUALITY:
                QUALITY = '720P'
            self.AddFileHost(list, QUALITY, url,host='WATCH-TVSERIES.NET') 
                        
                
            
    def Resolve(self, url):
        '''
        from entertainment import odict
        resolved_media_url = odict.odict()
        
        import re
        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        r = '<iframe class="videoPlayerIframe" src="(.+?)"></iframe>'
        match  = re.compile(r).findall(content)
        
        content = net.http_GET(match[0]).content
        r ='url(.+?)=(.+?)&amp'
        match  = re.compile(r).findall(content)
        
        urlselect  = []

        for res, url in match:            
            if url not in urlselect:
                urlselect.append(url)
                resolved_media_url[res] = url
        '''        
        return url
            
                

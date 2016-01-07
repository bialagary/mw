'''
    watchmoviespro
    Copyright (C) 2014 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class watchmoviespro(MovieSource):
    implements = [MovieSource]
    
    name = "watchmoviespro"
    display_name = "watchmoviespro"
    cookie_file = os.path.join(common.cookies_path, 'watchmoviespro')
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(url).content
        r = "onclick=\"window.open\('(.+?)', '_blank'\);\">(.+?)\s(.+?)</a>" 
        match  = re.compile(r).findall(content)
        for url,host,res in match:      
            if not 'now' in res.lower():
                if not '"' in res.lower():
                    res=res.replace('LQ','CAM').replace('MQ','SD').replace('HQ','HD')
                    self.AddFileHost(list, res, url,host=host.upper())
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers={'Host':'www.watchmoviesall.com','Origin':'http://www.watchmoviesall.com','Referer':'http://www.watchmoviesall.com/search_movies','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded'}

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        form_data={ "q":"%s" % (name) }
        content = net.http_GET('http://www.watchmoviesall.com/search_movies'+name.replace(' ','%20'), headers).content
        
        match=re.compile('<a href="(.+?)">(.+?) \((.+?)\)</a>').findall(content)
        for url , _name , _year  in match:
            url='http://www.watchmoviesall.com'+url
            if name in _name:
                if year in _year:
                    self.GetFileHosts(url, list, lock, message_queue)
                    

    
    def Resolve(self, url):
        
        import requests
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        r=requests.get(url, headers=headers,allow_redirects=False)


        URL = r.headers['location'].replace('/redirect.php?url=','')
        from entertainment import istream
        play_url = istream.ResolveUrl(URL)
        return play_url

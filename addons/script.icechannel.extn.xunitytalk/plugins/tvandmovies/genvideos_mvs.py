'''
    http://genvideos.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch



class genvideos(MovieSource):
    implements = [MovieSource]
    
    name = "genvideos"
    display_name = "genvideos"
    base_url = 'http://genvideos.org/'
    #img=''
    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):

        import re,urllib
        from entertainment.net import Net
        
        net = Net(user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
                  

        loginurl = 'https://m.genvideos.org/video_info/html5'
        
        v=url.split('v=')[1]
        data={'v': v}
        headers = {'host': 'm.genvideos.org','origin':'https://m.genvideos.org', 'referer': url,
                   'user-agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5','x-requested-with':'XMLHttpRequest'}

        first= net.http_POST(loginurl,data,headers).content

        import json

        link= json.loads(first)

        for j in link:
            quality = j.upper()
            if '360P' in quality:
                quality='SD'
                
            THEURL = urllib.unquote(link[j][3])+'**'+url
            self.AddFileHost(list, quality, THEURL,host='GOOGLEVIDEO.COM')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        name = self.CleanTextForSearch(name)

        search_term = name.lower()
        helper_term = ''
        ttl_extrctr = ''
        new_url='https://genvideos.org/results?q='+name.replace(' ','+')
        content= net.http_GET(new_url).content
        match=re.compile('title="(.+?)" href="(.+?)#').findall(content)
        for title , url in match:
            if name in title:
                if year in title:
                    movie_url = 'http://m.genvideos.org'+url

                    self.GetFileHosts(movie_url, list, lock, message_queue)



    def Resolve(self, url):

        v=url.split('**')[1]
        url=url.split('**')[0]

                   
        return url

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
    
    name = "izlemeyedeger"
    display_name = "izlemeyedeger"
    base_url = 'http://www.izlemeyedeger.com'
    #img=''
    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        
        net = Net(user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
                  

        first= net.http_GET(url).content
        
        new_url='http://www.izlemeyedeger.com/iframe/'+re.compile('/iframe/(.+?)"').findall(first)[0]
        headers = {'referer':url}
        second= net.http_GET(new_url,headers=headers).content
   
        match=re.compile('file: "(.+?)".+?label: "(.+?)"',re.DOTALL).findall(second)
        #print match
        for THEURL , res  in match:
            quality=res.upper()
            self.AddFileHost(list, quality, THEURL,host='GOOGLEVIDEO.COM')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        name = self.CleanTextForSearch(name)

        search_term = name.lower()
        helper_term = ''
        ttl_extrctr = ''
        new_url=self.base_url +'/arama?q='+name.replace(' ','+')
        content= net.http_GET(new_url).content
        link = content.split('<li>')

        for p in link:
          try:
              movie_url=re.compile('href="(.+?)"',re.DOTALL).findall(p)[0]
              title=re.compile('"video-title">(.+?)<',re.DOTALL).findall(p)[0]
              YEAR=re.compile('"year">(.+?)<',re.DOTALL).findall(p)[0]
              
          
       
              title=title.strip()
              YEAR=YEAR.strip()
  
              if name.lower() in title.lower():
                  if year in YEAR:
                    

                      self.GetFileHosts(movie_url, list, lock, message_queue)
          except:pass
          

    def Resolve(self, url):

        import urllib
        return urllib.urlopen(url).geturl()

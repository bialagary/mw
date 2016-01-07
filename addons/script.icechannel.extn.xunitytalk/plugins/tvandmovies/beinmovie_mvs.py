'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class beinmovie(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "BeinMovie"
    display_name = "BeinMovie"
    base_url = 'https://beinmovie.com/'
   
    source_enabled_by_default = 'true'

            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net(cached=False)
     
        print url
        content = net.http_GET(url).content
        #print content
      
        match=re.compile('movie-player/(.+?)"').findall(content)



        for URL  in match:
            getcontent = net.http_GET('https://beinmovie.com/movie-player.php?'+URL).content
            #print getcontent
            try:
                 FINAL_URL=re.compile('src="(.+?)"').findall(getcontent)[0]
            except:
                 FINAL_URL=re.compile("src='(.+?)'").findall(getcontent)[0]
       
            if len(FINAL_URL)< 8:
                grabsecond =  re.compile('movie-player/(.+?)"').findall(getcontent)[1]
                getcontent = net.http_GET('https://beinmovie.com/movie-player.php?'+grabsecond).content
                try: 
                    FINAL_URL=re.compile(' src="(.+?)"').findall(getcontent)[0]
                except: 
                    FINAL_URL=re.compile(" src='(.+?)'").findall(getcontent)[0]                
            if 'movie_lang=fr' in URL:
                language= 'French'
            elif 'movie_lang=en' in URL:
                language= 'English'
            else:language=''    
            self.AddFileHost(list, '1080P', FINAL_URL,host='GOOGLEVIDEO - '+language)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        name = self.CleanTextForSearch(name)

        

        main_url='https://beinmovie.com/movies-list.php?b=search&v=' + name.replace(' ','+')
        
  
        content=net.http_GET(main_url).content
        
        match=re.compile('#!movie-detail/id=(.+?)/').findall (content)
        for id in match: 
            item_url='https://beinmovie.com/movie-detail.php?id='+id
            self.GetFileHosts(item_url, list, lock, message_queue)
              

    def GrabMailRu(self,url,list):
        print 'RESOLVING VIDEO.MAIL.RU VIDEO API LINK'
        
        
        from entertainment.net import Net
        net = Net(cached=False)

        
        import json,re
        items = []

        data = net.http_GET(url).content
        cookie = net.get_cookies()
        
        for x in cookie:
             if '.my.mail.ru' in x: 
                 for y in cookie[x]:
                      for z in cookie[x][y]:
                           l= (cookie[x][y][z])
                       
        r = '"key":"(.+?)","url":"(.+?)"'
        match = re.compile(r,re.DOTALL).findall(data)
        for quality,stream in match:
            test = str(l)
            test = test.replace('<Cookie ','')
            matcher =re.compile('for (.+?)>').findall(test)[0]
            test = test.replace(' for '+matcher+'>','')
            url=stream +'|Cookie='+test
            Q=quality.upper()
            if Q == '1080P':
                Q ='1080P'
            elif Q == '720P':
                Q ='720P'                
            elif Q == '480P':
                Q ='HD'
            else:
                Q ='SD'     
            self.AddFileHost(list, Q, url,host='MAIL.RU')  

             

    def Resolve(self, url):                 
        print '############################' +url
        if 'mail.ru' in url:
            resolved = url
        if 'googleusercontent.com' in url:
            import urllib
            page = urllib.urlopen(url)
            resolved=page.geturl()
            
        elif 'googlevideo.com' in url:
            resolved =url
        else:
        
            from entertainment import istream
            resolved =istream.ResolveUrl(url)
        return resolved    









            

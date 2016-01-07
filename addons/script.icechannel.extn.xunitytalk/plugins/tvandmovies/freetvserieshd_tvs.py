'''
    Istream
    Oneclickwatch
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.xgoogle.search import GoogleSearch


class freetvserieshd(TVShowSource):
    implements = [TVShowSource]
	
    #unique name of the source
    name = "freetvserieshd"
    source_enabled_by_default = 'true'
    #display name of the source
    display_name = "FreeTvSeriesHD"
    
    #base url of the source website
    base_url = 'http://freetvserieshd.com/'
    
    def GetFileHosts(self, url, list, lock, message_queue,referer):
        import re

        from entertainment.net import Net
        net = Net()

        headers={'Host': 'freetvserieshd.com',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
                'Referer': referer,
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language':'en-US,en;q=0.8'}
        
        
        content = net.http_GET(url,headers=headers).content
        match=re.compile('"file":"(.+?)".+?"label":"(.+?)"',re.DOTALL).findall(content)
        for url , res in match:            
               
                res =res.upper()
                if '480' in res:
                    res='HD'
                    
                url=url+'|'+res
                            
                self.AddFileHost(list, res, url)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net()
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)


        search_term ='%s Season %s Episode %s' %(name,season,episode)
        referer = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, '', title_extrctr=['(.+?) Watch Online'])
     
        content = net.http_GET(referer,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}).content 
        print '#################################'
        print referer
        URL=re.compile('<iframe src="(.+?)"').findall(content)[0]        

       

        
        self.GetFileHosts(URL, list, lock, message_queue,referer)


    def Resolve(self, url):
        url=url.split('|')[0]
        return url

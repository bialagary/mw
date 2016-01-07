'''
    Istream
    http://www.oneclickmoviez.ag/
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common

#from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class oneclickmoviez(MovieSource):
    implements = [MovieSource]
	
    #unique name of the source
    name = "oneclickmoviez"
    source_enabled_by_default = 'false'
    #display name of the source
    display_name = "Oneclickmoviez"
    
    #base url of the source website
    base_url = 'http://www.oneclickmoviez.ag/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()

        content = net.http_GET(url).content
        r = '<li class="current right" style="float:right"><a href="(.+?)" target="_blank">Open video</a>' 
        match  = re.compile(r).findall(content)


        for url in match:
            
            first=url.split('http://')[1]
            host=first.split('/')[0].upper()
            host=host.strip('WWW.')
            
            self.AddFileHost(list,'DVD', url, host=host)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net()

        search_term = name
        category = ''
        if type == 'tv_episodes':
            category = 'category=4'
        elif type == 'movies':
            category = 'category=5'
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        name = name.rstrip()
        name = name.replace("'","")
        name = name.replace(":","")
        name = name.replace("&","and")
        name = name.replace("."," ")
        
        movie_url='http://www.oneclickmoviez.ag/movie/%s' %(name.replace(' ','-')).lower()
        print movie_url
        print '################################################################################################################################'
        
        if type == 'movies':
            headers = ({'User-Agent': 'Magic Browser'})
            link = re.split('Start: Post', net.http_GET(movie_url).content)[0]
            url = re.findall(r'<a href="http://www.oneclickmoviez.ag/movie/(.+?)"><img src=".+?" class="video-page-thumbnail" /></a>', str(link), re.DOTALL)
            for url in url:
                url = 'http://www.oneclickmoviez.ag/movie/'+ url
                print url
                print '#######################################################################################################################'
                self.GetFileHosts(url, list, lock, message_queue)
            
            
        #elif type == 'tv_episodes':
            #headers = ({'User-Agent': 'Magic Browser'})
            #link = re.split('Start: Post', net.http_GET(tv_url).content)[0]
            #r = re.findall('s\d+e', link, re.I)
            #if r:
                #url = re.findall(r'<h2 class="title"><a href="(.+?)" title=".+?">.+?</a></h2>', str(link), re.I)
                #for url in url:
                    #self.GetFileHosts(url, list, lock, message_queue)

'''
    Istream
    Oneclickwatch
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class oneclickwatch(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    #unique name of the source
    name = "oneclickwatch"
    source_enabled_by_default = 'false'
    #display name of the source
    display_name = "Oneclickwatch"
    
    #base url of the source website
    base_url = 'http://oneclickwatch.org/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()

        content = net.http_GET(url).content
        r = '<a href="(.+?)" rel="nofollow">.+?</a><br />' 
        match  = re.compile(r).findall(content)

        r2 = '<strong>Release Title</strong>\: (.+?)<br />'
        quality  = re.compile(r2).findall(content)
        
        
        urlselect  = []

        for url in match:            
            if url not in urlselect:
                urlselect.append(url)
                res = 'SD'
                if re.findall('720', str(quality), re.I):
                    res = 'HD'
                elif re.findall('1080', str(quality), re.I):
                    res = 'HD'
                elif re.findall('CAM', str(quality), re.I):
                    res = 'CAM'
                elif re.findall('BRRIP', str(quality), re.I):
                    res = 'DVD'
                
                #if '720p' in quality or '1080p' in quality or 'BRRip' in quality:
                    #res = 'HD'
                #elif 'CAM' in quality:
                    #res = 'CAM'
                #elif 'Cam' in quality:
                    #res = 'CAM'
                
                            
                self.AddFileHost(list, res, url)



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

        #Movies = http://oneclickwatch.org/?s=Escape+Plan+2013
        #TV Shows = http://oneclickwatch.org/?s=warped+roadies+s02E07

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode

        tv_url='http://oneclickwatch.org/?s=%s+S%s+E%s' %(name.replace(' ','+'),season_pull,episode_pull)
        movie_url='http://oneclickwatch.org/?s=%s+%s' %(name.replace(' ','+'),year)
        if type == 'movies':#<h2 class="title"><a href="(.+?)" title=".+?">.+?</a></h2>
            headers = ({'User-Agent': 'Magic Browser'})
            link = re.split('Start: Post', net.http_GET(movie_url).content)[0]
            url = re.findall(r'<h2 class="title"><a href="(.+?)" title=".+?">.+?</a></h2>', str(link), re.DOTALL)
            for url in url:
                self.GetFileHosts(url, list, lock, message_queue)
            
        elif type == 'tv_episodes':
            headers = ({'User-Agent': 'Magic Browser'})
            link = re.split('Start: Post', net.http_GET(tv_url).content)[0]
            r = re.findall('s\d+e', link, re.I)
            if r:
                url = re.findall(r'<h2 class="title"><a href="(.+?)" title=".+?">.+?</a></h2>', str(link), re.I)
                for url in url:
                    self.GetFileHosts(url, list, lock, message_queue)

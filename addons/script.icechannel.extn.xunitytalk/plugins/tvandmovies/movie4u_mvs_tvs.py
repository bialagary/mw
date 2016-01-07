'''
    Istream
    movie4u
    Copyright (C) 2013 Coolwave

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class movie4u(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    name = "movie4u"
    source_enabled_by_default = 'false'
    display_name = "Movie4u"
    base_url = 'http://movie4u.org/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        r = 'href="(.+?)"\s*><img class="favicon" alt="(.+?)" src=".+?".+?<div class="cell" data-field="source">(.+?)</div>'
        match  = re.compile(r,re.DOTALL).findall(content)
        
        urlselect  = []

        for url,host,res in match:            
            if url not in urlselect:
                urlselect.append(url)
                
                quality = 'SD'
                res_lower = '.' + res.lower() + '.'
                for quality_key, quality_value in common.quality_dict.items():
                    if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                        quality = quality_value
                        break
                
                self.AddFileHost(list, quality, url, host=host.upper())


    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net()

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
        
        tv_url='http://movie4u.org/rss/search/%s s%se%s' %(name.replace(' ','%20'),season_pull,episode_pull)
        tv_url= tv_url.replace(' ','%20')
        movie_url='http://movie4u.org/rss/search/%s %s' %(name.replace(' ','%20'),year)
        movie_url=movie_url.replace(' ','%20')

        if type == 'movies':
            
            html = net.http_GET(movie_url).content
            name_lower = common.CreateIdFromString(name)
            for item in re.finditer(r"<title>(.+?) \((.+?)\)</title>\s*<link>(.+?)</link>\s*<category>Movies</category>", html):
                item_url = item.group(3)
                item_name = common.CreateIdFromString(item.group(1))
                item_year = item.group(2)
                item_name = item_name.replace('-',' ')
                            
                if item_name == name_lower and item_year == year:
                    self.GetFileHosts(item_url, list, lock, message_queue)

        elif type == 'tv_episodes':
            html = net.http_GET(tv_url).content
            name_lower = common.CreateIdFromString(name)        
            for item in re.finditer(r"<title>(.+?) S(.+?) E(.+?)</title>\s*<link>(.+?)</link>\s*<category>TV Episodes</category>", html):
                item_url = item.group(4)
                item_name = common.CreateIdFromString(item.group(1))
                item_season = item.group(2)
                item_eps = item.group(3)
                season_pull = "0%s"%season if len(season)<2 else season
                episode_pull = "0%s"%episode if len(episode)<2 else episode

                if item_name == name_lower and item_season == season_pull and item_eps == episode_pull:

                        self.GetFileHosts(item_url, list, lock, message_queue)


                        
                

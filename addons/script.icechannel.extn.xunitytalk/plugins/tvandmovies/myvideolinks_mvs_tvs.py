'''
    Istream
    myvideolinks
    Copyright (C) 2013 Coolwave

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class myvideolinks(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    name = "myvideolinks"
    source_enabled_by_default = 'false'
    display_name = "Myvideolinks"
    base_url = 'http://www.myvideolinks.eu/'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()

        content = net.http_GET(url).content
        
        r = '<li><a href="(http://.+?)">(.+?)</a></li>'
        match  = re.compile(r).findall(content)
        match1 = re.compile('rel="bookmark" title=".+?">(.+?)</a></h1>').findall(content)
        
        urlselect  = []

        for url, host in match:
            for res in match1:
                if url not in urlselect:
                    urlselect.append(url)
                    
                    quality = 'SD'
                    res_lower = '.' + res.lower() + '.'
                    for quality_key, quality_value in common.quality_dict.items():
                        if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                            quality = quality_value
                            break
                    if 'myvideolinks' in url:
                        url= False
                        continue
                    if 'http://i.imgur.com/' in url:
                        url=False
                        continue
                    
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
        
        tv_url='http://www.myvideolinks.eu/index.php?s=%s+S%sE%s' %(name.replace(' ','+'),season_pull,episode_pull)
        movie_url='http://www.myvideolinks.eu/index.php?s=%s+%s' %(name.replace(' ','+'),year)

        if type == 'movies':
            html = net.http_GET(movie_url).content
            for item in re.finditer(r'<h4><a href="(.+?)" rel="bookmark"',html,re.I):
                url = item.group(1)                
                self.GetFileHosts(url, list, lock, message_queue)

        elif type == 'tv_episodes':
            html = net.http_GET(tv_url).content
            for item in re.finditer(r'<h4><a href="(.+?)" rel="bookmark"',html,re.I):
                url = item.group(1)                
                self.GetFileHosts(url, list, lock, message_queue)

    '''
    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        print "test#############################################################"
        content = net.http_GET(url).content
                       
        if 'http://adf.ly/' in url:
            
            try:
                import time
                content = net.http_GET(url).content
                time.sleep(9)
                encoded_url = re.compile("var ysmm = '(.+?)';").findall(content)[0]
                encoded_url_length = len(encoded_url)
                encdd_url_part_1 = ''
                encdd_url_part_2 = ''
                for x in range(0, encoded_url_length):
                    enc_char = encoded_url[x]
                    if not re.match("[a-zA-Z0-9\+/=]", enc_char):
                        break;
                    if x % 2 == 0:
                        encdd_url_part_1 = encdd_url_part_1 + enc_char
                    else:
                        encdd_url_part_2 = enc_char + encdd_url_part_2
                encoded_url = encdd_url_part_1 + encdd_url_part_2
                import base64
                url = (base64.b64decode(encoded_url))[2:]
            
            except:
                continue
        self.GetFileHosts(url)
    '''

        

                
                

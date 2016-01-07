
'''
    Istream
    tv-release.net
    Copyright (C) 2013 the-one, voinage, Jas0npc, Coolwave

    version 0.2

    0/01/2014 improved regex for GetFileHostsForContent results.
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin

class Tvrelease(TVShowSource):
    implements = [TVShowSource]
    name = "Tvrelease"
    display_name = "TV-Release"
    base_url = 'http://tv-release.net'
    source_enabled_by_default = 'false'

    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import re

        net = Net()
        sources = []
        
        content = net.http_GET(url).content
        qual = re.compile(r'td_col\"\>TV-(.+?)\<\/td\>').findall(content)[0]

        try:
            links = re.compile(r'\'_blank\'\shref=\'(.+?)\'\>', re.I|re.M|re.DOTALL).findall(content)
            for url in links:
                sources.append(url)
        except:
            pass

        try:
            links = re.compile(r'\d\d\:\d\d\<\/div\>(http\:.+?)\<\/div\>\<\/li\>', re.I|re.M|re.DOTALL).findall(content)
            for url in links:
                sources.append(url)
        except:
            pass

            
        for url in sources:
            res = 'SD'
            quality = qual.lower()

            if '720p' in quality or '1080p' in quality or 'hd' in quality:
                res = 'HD'
            

            #if re.search(r'go4up.com', url, re.I):
            #    import requests2
            #    import time

                
            #    Referer = url
            #    html = requests2.get(url)

            #    r = re.findall(r'Cookie\s(.*?)\=(.*?)\>', str(html.cookies), re.I)
            #    cookies = {}
            #    for name, value in r:
            #        cookies.update({str(name): str(value)})

            #    r = re.findall(r'href=\"(.*?)\"\s+class=\"dl\"\s+\"\s+title=\".*?\s+:\s+succeed\"',
            #                   html.text, re.I)

            #    for go4url in r:

            #        headers = {}
            #        headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #                        'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
            #                        'Connection': 'keep-alive', 'Referer': '',
            #                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'})
                    
            #        try:
            #            url = requests2.get(go4url).url
            #        except:
            #            return
            #        self.AddFileHost(list,res,url)
            if not '.rar' in url:
               
                self.AddFileHost(list,res,url)


    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        from entertainment.net import Net
        import re

        net = Net()
        
        seasonshit = "0%s"%season if len(season)<2 else season
        episodeshit = "0%s"%episode if len(episode)<2 else episode
        valid_constructor='S%sE%s'%(seasonshit,episodeshit)
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        search_url_title = "%s/?s=%s"%(self.base_url,name.replace(' ','+').lower())
        search_url_digit = "%s/?s=%s%sS%sE%s&cat=" % (self.base_url, name.replace(' ','+').lower(),
                                                      '%20', seasonshit, episodeshit)
        print search_url_title
        print search_url_digit
        content = net.http_GET(search_url_digit).content
        match=re.compile("<a href='http://tv-release.net/(\d*\/.+?)'").findall(content)
        
        for url in match:
            self.GetFileHosts(self.base_url+'/'+url, list, lock, message_queue)

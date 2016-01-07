'''
    http://ororo.tv/en    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui
import urllib,urllib2,urlparse,re,datetime,base64,xbmcaddon


class ororo(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "ororo"
    display_name = "Ororo.tv"
    base_url = 'http://ororo.tv/nl'
    login_url = 'http://ororo.tv/users/sign_in'
    img=''
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'
    cookie_file = os.path.join(common.cookies_path, 'ORlogin.cookie')
    icon = common.notify_icon
    
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="hhhhhhhh@hhhhhhhh.com" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="hhhhhhhh" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
          
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')
        net.set_cookies(self.cookie_file)
        content = net.http_GET(url).content
        
        r = "<source src='(.+?)' type='(.+?)'>"
        match  = re.compile(r).findall(content)

        for url,res in match:
            url = '%s|User-Agent=%s&Cookie=%s' % (url,urllib.quote_plus('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'), urllib.quote_plus('video=true'))
            quality = 'HD'
            if 'video/mp4' in res:
                quality = 'HD'
            else:
                quality = 'SD'
                             
            self.AddFileHost(list, quality, url,'ORORO.TV')
        


    def login(self):
        
        headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
                 'Host':'ororo.tv',
                 'Pragma':'no-cache',
                 'Referer':'http://ororo.tv/en',
                 'Upgrade-Insecure-Requests':'1',
                 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Accept-Encoding':'gzip, deflate, sdch',
                 'Accept-Language':'en-US,en;q=0.8',
                 'Cache-Control':'no-cache',
                 'Connection':'keep-alive'}
        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')        
        from entertainment.net import Net
        
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')
        
        tries = 0
        while True:
            html = html = net.http_GET('http://ororo.tv/nl/',headers=headers).content
            if html.startswith('http://') and tries < MAX_REDIRECT:
                tries += 1
                url = html
            else:
                break
        
        data = {'user[email]': tv_user, 'user[password]': tv_pwd, 'user[remember_me]': 1}
        html = net.http_POST('http://ororo.tv/en/users/sign_in',data,headers=headers).content
        net.save_cookies(self.cookie_file)
      
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        if os.path.exists(common.cookies_path) == False:
                os.makedirs(common.cookies_path)
                
        import re
        from entertainment.net import Net
        
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        main_url=self.base_url

        helper = '%s (%s)' %(name,year)

        
        if type == 'movies':
            self.login()
            url='http://ororo.tv/nl/movies'
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            name_lower = common.CreateIdFromString(name)
            r = '<span class=\'value\'>(\d{4}).*?href="([^"]+)[^>]+>([^<]+)'
            match  = re.compile(r,re.DOTALL).findall(html)
            for item_year,item_url,item_title in match:
                item_title=item_title.lower()
                if item_title in name_lower:
                    self.GetFileHosts(item_url, list, lock, message_queue)


        elif type == 'tv_episodes':
            self.login()
            name_lower = common.CreateIdFromString(name)
            name_lower = name_lower.replace('_','-')
            title_url='http://ororo.tv/en/shows/'+name_lower
            net.set_cookies(self.cookie_file)
            html2 = net.http_GET(title_url).content
            net.save_cookies(self.cookie_file)
            r = '%s-%s' % (season, episode)
            match  = re.compile('data-href="(.+?)".+?class="episode" href="#(.+?)">').findall(html2)
            for item_url , passer in match:
                item_url='http://ororo.tv/'+item_url
                if r in passer:

                    self.GetFileHosts(item_url, list, lock, message_queue)

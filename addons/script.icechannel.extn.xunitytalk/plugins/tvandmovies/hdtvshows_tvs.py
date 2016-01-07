'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
import xbmc,os
datapath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data','script.icechannel'))
cookie_path = os.path.join(datapath, 'cookies')


class hdtvshows(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "HDTVSHOWS"
    display_name = "HDTVSHOWS"
    base_url = 'http://hdtvshows.net'
    source_enabled_by_default = 'true'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Username" default="yotoyoto@yotoyoto.com" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="yotoyoto" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
    
    
    def GetFileHosts(self, url, list, lock, message_queue,scrape): 
        
        import re
        
        from entertainment.net import Net
        
        net = Net(cached=False)
        content = net.http_GET(url).content
        link=content.split('href=')
        
        for p in link:
            if scrape in p:
                r='"(.+?)"'
                
                match=re.compile(r).findall(p)[0]
                
                self.AddFileHost(list, 'HD', self.base_url+match)
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment.net import Net
        import re
        net = Net(cached=False)        
        
        name = self.CleanTextForSearch(name) 
        season = self.CleanTextForSearch(season) 
        episode = self.CleanTextForSearch(episode)
            
        scrape ='S' + season+ ', Ep' + episode
        search_term = name
        helper_term = 'tvshow'
        data     = {'q': name}
        headers  = {'Host':'hdtvshows.net',
                                            'Origin':'http://hdtvshows.net',
                                            'Referer':'http://hdtvshows.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        html = net.http_POST('http://hdtvshows.net/find.php', data, headers).content
           
        r='%s Free " href="(.+?)">' % name
        match=re.compile(r).findall(html)[0]
        self.GetFileHosts(self.base_url+match, list, lock, message_queue,scrape)
        
        

    def Resolve(self, url):
        print url
        import re        
        from entertainment.net import Net
        net = Net(cached=False,user_agent='Apple-iPhone/')
        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')
        loginurl = 'http://hdtvshows.net/reg.php'
        html = net.http_GET(loginurl).content
        match=re.compile('name="Token(.+?)" value="(.+?)"').findall(html)
        _Token=re.compile('name="data\[\_Token\]\[fields\]" value="(.+?)"').findall(html)[0]
        data     = {'_method':'POST','subscriptionsPass': tv_pwd,
                                            'UserUsername': tv_user,
                                            'Token'+match[0][0]:'login','data[_Token][fields]':_Token}
        headers  = {'Host':'hdtvshows.net',
                                            'Origin':'http://hdtvshows.net',
                                            'Referer':'http://hdtvshows.net/login.php',
                                                    'X-Requested-With':'XMLHttpRequest'}
        html = net.http_POST(loginurl, data, headers)
        cookie_jar = os.path.join(cookie_path, "hdtvshows.lwp")
        if os.path.exists(cookie_path) == False:
                os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)
        net.set_cookies(cookie_jar)        
        html = net.http_GET(url).content
        

        match=re.compile('<video id="ipadvideo" src="(.+?)"').findall(html)
        
        
        
        return  match[0].replace('|','%7C')

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class putlockeris(MovieSource):
    implements = [MovieSource]
    
    name = "putlocker.is"
    display_name = "Putlocker.is"
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        import decrypter
        from entertainment.net import Net
        net = Net()
        movielink = net.http_GET(url).content
        try:       
            match=re.compile('plugins=http://static1.movsharing.com/plugin.+?/proxy.swf&proxy.link=movs*(.+?)&').findall(movielink)
            match = match[0].replace('*','') 
            s= decrypter.decrypter(192,128)
            uncode = s.decrypt(match,'u3332bcCRs2DvUf17rqq','ECB').split('\0')[0]
            link = net.http_GET(uncode).content
            match=re.compile('"file":"(.+?)",').findall(link)
            newurl = match[0].replace ('\/','/')
            res = 'SD'
            host='*GOOGLE.COM'
            self.AddFileHost(list, res, newurl, host)
        except: pass
        links=re.compile('rel=".+?" href="(.+?)" target="_blank" title=".+?">Version .+?</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.+?').findall(movielink)        
        for url in links:
            hostname=re.compile('http://(.+?)/').findall(url)
            host = str(hostname).replace('www.','')
            res='SD'
            self.AddFileHost(list, res, url)
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re, urllib
        from entertainment.net import Net
        net = Net()
        name = self.CleanTextForSearch(name)
        helper ='%s (%s)' %(name, year)
        name = urllib.quote(name)
        search_url = 'http://putlocker.is/search/search.php?q=' + name
        print search_url
        content = net.http_GET(search_url).content
        search_res = re.split('Search Results For: "<font color=red>', content)[1]
        match = re.compile('href="(.+?)" title="(.+?)"').findall(search_res)
        for url, title in match:
            if title == helper or title == helper.replace(':',' 2:'):
                self.GetFileHosts(url, list, lock, message_queue)

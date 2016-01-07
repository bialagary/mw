'''
    Ice Channel
    http://clickplay.to/
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class clickplay(TVShowSource):
    implements = [TVShowSource]
    
    name = "clickplay"
    display_name = "clickplay"
    
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        #from entertainment.net import Net
        
        #net = Net(user_agent='Apple-iPhone/')
        #import re
        #html=net.http_GET(url).content
        #link_url = re.compile('<div id="videoplayer" style=".+?">\s*<iframe src="(.+?)"').findall(html)[0]
        #link_url = re.compile('FlashVars="plugins=/plugins/proxy.swf&proxy.link=clickplay*(.+?)"').findall(html)[0]
        
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net()        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','%20')
        search_term = search_term.lower()
        
        search_term = search_term.replace('the','')
        
        import re
        url='http://clickplay.to/search/'+search_term+'?'
        
        link=net.http_GET(url).content
        if 'Unfortunately there are no results right now' in link:
            return None
        match = re.compile('<div id="video_list">\s*<a href="(.+?)" class="article" data="(.+?)">.+?<span class="article-title">(.+?) \((.+?)\)</span>',re.DOTALL).findall(link)
        
        for tv_url , data, tvshowname, tvshowyear  in match:
            
            if year in tvshowyear:
                season_pull = "0%s"%season if len(season)<2 else season
                episode_pull = "0%s"%episode if len(episode)<2 else episode
                url=tv_url+'season-'+season+'/'
                html=net.http_GET(url).content
                link_url = re.compile('<a href="(.+?)" title=".+?Episode '+episode+' / .+?" class=".+?">').findall(html)[0]
                
                self.GetFileHosts(link_url, list, lock, message_queue)

    def Resolve(self, url):
        import base64
        import decrypter
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        html = net.http_GET(url).content

        url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(html)[-1]
        url = decrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]
        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url
                
            

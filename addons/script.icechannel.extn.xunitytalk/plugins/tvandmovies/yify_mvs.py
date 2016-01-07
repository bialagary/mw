'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class yify(MovieSource):
    implements = [MovieSource]
    
    name = "Yify"
    display_name = "Yify"
    base_url = 'http://yify.tv/'
    source_enabled_by_default = 'false'

    icon = common.notify_icon
    
    
    def GetFileHosts(self, url, list, lock, message_queue,name): 
        
        import re,json
        
        from entertainment.net import Net

        net = Net(cached=False)
        content = net.http_GET(url).content
        links=re.compile('pic=([^&]+)').findall (content)
        links = [x for y,x in enumerate(links) if x not in links[:y]]

        for i in links:

            data = {'url': i, 'fv': '16'}
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
            html=   net.http_POST('http://yify.tv/player/pk/pk/plugins/player_p2.php',data,headers=headers).content
            result = json.loads(html)     
            for field in result:

                     if field['width']== 1920:
                         url = field['url']
                         res= '1080P'
                         host=url.split('://')[1]
                         host=host.split('/')[0].replace('www','')
                         self.AddFileHost(list, res, url,host=host.upper())
                     if field['width']== 1280:
                         url = field['url']
                         res= '720P'
                         host=url.split('://')[1]
                         host=host.split('/')[0].replace('www','')                       
                         self.AddFileHost(list, res, url,host=host.upper())
       
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment.net import Net
        import re
        net = Net(cached=False)        
        
        name = self.CleanTextForSearch(name) 


        data={'action': 'ajaxy_sf', 'sf_value': name}
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        html=   net.http_POST('http://yify.tv/wp-admin/admin-ajax.php',data,headers=headers).content
        
        import json
        result=json.loads(html)
        data=result['post']['all']
        for field in data:
           url =field['post_link']
           title =field['post_title']
           if name == title:
               self.GetFileHosts(url, list, lock, message_queue,name)
        
        

    def Resolve(self, url):

        return url

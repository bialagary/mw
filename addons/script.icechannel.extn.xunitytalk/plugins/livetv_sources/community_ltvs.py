'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class community(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "Playlist Community"
    
    name = 'Playlist Community'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://pastebin.com/raw.php?i=%s'
    
    BLOG=['XaAWPhpG','dWd9TbSR']

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        

        
        from entertainment.net import Net
        net = Net()

        clean_id= id.replace('_',' ').lower()
        
        for blogs in self.BLOG:

            import re
            
            r = self.base_url % blogs
            
            content = net.http_GET(r).content
            

            POSTER=re.compile('<poster>(.+?)</poster>').findall(content)[0]

            match=re.compile('<title>(.+?)</title>.+?link>(.+?)</',re.DOTALL).findall(content)
 
            
            for name, RTMP in match:
                if clean_id.replace(' ','') in name.replace(' ','').lower():

                        self.AddLiveLink( list, name, RTMP, host=POSTER)

        

    def Resolve(self, url):

        
        return url
        
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)
        

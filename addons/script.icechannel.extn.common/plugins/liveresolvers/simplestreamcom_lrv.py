'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class simplestreamcom(LiveResolver):

    implements = [LiveResolver]
    
    name = 'simplestream.com'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"](http://players.simplestream.com/.+?\.js)[\'"]', content)

        if new_content:
        
            page_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net()
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            play_media = re.search('(http.+?\.m3u8)', content)
            
            if play_media:
            
                content = play_media.group(1)
                                
                return (True, True, content, url)
            
        return (False, False, content, url)

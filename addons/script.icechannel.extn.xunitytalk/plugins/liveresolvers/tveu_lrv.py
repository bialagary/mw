'''
    Ice Channel
    tv.eu
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class tveu(LiveResolver):
    implements = [LiveResolver]
    
    name = 'tv.eu'
    
    def ResolveLive(self, content, url):
    
        import re
        print '--------------------------------0'
        new_content = re.search("<iframe.+?src=[\"'](http://www\.embed\-tv\.eu/live.+?)[\"']", content)
        
        if new_content:
        
            page_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net(http_debug=True)            
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            print '---------------------------1'
            print content
                        
            return (False, True, content, page_url)
            
        return (False, False, content, url)

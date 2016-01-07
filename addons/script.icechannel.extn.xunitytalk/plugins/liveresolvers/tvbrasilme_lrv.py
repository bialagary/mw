'''
    Ice Channel
    tvbrasil.me
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class tvbrasilme(LiveResolver):
    implements = [LiveResolver]
    
    name = 'tvbrasil.me'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search("<iframe.+?src=[\"'](http://tvbrasil.me/.+?\.html)[\"']", content)
        
        if new_content:
        
            page_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net()            
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            new_content = re.search("<iframe.+?src=[\"'](.+?)[\"']", content)
            
            url = page_url
            page_url = 'http://tvbrasil.me/' + new_content.group(1)
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            return (False, True, content, page_url)
            
        return (False, False, content, url)

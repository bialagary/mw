'''
    Ice Channel
    lag10.com
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class lag10com(LiveResolver):
    implements = [LiveResolver]
    
    name = 'lag10.com'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search("<iframe.+?src=[\"'](http://lag10.com/.+?)[\"']", content)
        
        if new_content:
            from entertainment.net import Net
            net = Net()            
            
            content = net.http_GET(new_content.group(1), headers={'Referer':url}).content
            return (False, True, content, 'lag10.com')
            
        return (False, False, content, url)

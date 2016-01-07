'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class livehdstreamsinfo(LiveResolver):

    implements = [LiveResolver]
    
    name = 'livehdstreams.info'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"]{1}http://livehdstreams\.info/(.+?)\.php[\'"]{1}', content)

        if new_content:
            from entertainment.net import Net
            net = Net()
            
            new_url = 'http://livehdstreams.info/%s.php' % new_content.group(1)
            
            new_content = net.http_GET(new_url, headers={'Referer':url}).content

            return (False, True, new_content, new_url)
                            
        return (False, False, content, url)

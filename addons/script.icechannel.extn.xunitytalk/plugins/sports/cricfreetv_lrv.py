'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class cricfreetv(LiveResolver):

    implements = [LiveResolver]
    
    name = 'cricfree.tv'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"]{1}http://cricfree\.tv/(.+?)\.php[\'"]{1}', content)

        if new_content:
            from entertainment.net import Net
            net = Net()
            
            new_url = 'http://cricfree.tv/%s.php' % new_content.group(1)
            
            new_content = net.http_GET(new_url, headers={'Referer':url}).content

            return (False, True, new_content, new_url)
                            
        return (False, False, content, url)

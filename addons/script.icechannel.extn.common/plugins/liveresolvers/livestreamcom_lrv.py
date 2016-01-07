'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class livestreamcom(LiveResolver):
    implements = [LiveResolver]
    
    name = 'livestream.com'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search("<iframe.+?src=[\"']http://.+?livestream\.com/embed/(.+?)\?", content)        
        if new_content:
            channel_id = new_content.group(1)
            playable_url = 'http://x%sx.api.channel.livestream.com/3.0/playlist.m3u8' % channel_id
            return (True, True, playable_url, url)
            
        new_content = re.search("<iframe.+?src=[\"'](http://.+?livestream\.com/accounts/[0-9]+?/events/[0-9]+?/player\?.+?)", content)        
        if new_content:
            new_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net()
            new_content = net.http_GET(new_url, headers={'Referer':url}).content

            m3u8_url = re.search('[\'"]{1}(http://[^\'"]+?\.m3u8[^\'"]+?)[\'"]{1}', new_content)
            if m3u8_url:
                resolved_media_url = m3u8_url.group(1)
                return (True, True, resolved_media_url, url)
            
        return (False, False, content, url)

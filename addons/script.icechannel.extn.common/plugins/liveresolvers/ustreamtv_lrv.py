'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class ustreamtv(LiveResolver):
    implements = [LiveResolver]
    
    name = 'ustream.tv'
    
    def ResolveLive(self, content, url):
    
        import re
        new_content = re.search("<iframe.+?src=[\"']http://www\.ustream\.tv/embed/(.+?)\?", content)
        
        if new_content:
            
            channel_id = new_content.group(1)
            
            playable_url = 'http://iphone-streaming.ustream.tv/ustreamVideo/%s/streams/live/playlist.m3u8' % channel_id
                        
            return (True, True, playable_url, url)
            
        return (False, False, content, url)

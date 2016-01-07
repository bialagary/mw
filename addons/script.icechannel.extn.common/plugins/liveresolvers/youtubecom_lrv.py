'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class youtubecom(LiveResolver):
    implements = [LiveResolver]
    
    name = 'youtube.com'
    
    def ResolveLive(self, content, url):
    
        import re
        new_content = re.search("<object.+?data=[\"']{1}[^\"']+?youtube\.com/v/(.+?)\?", content)
        if not new_content:
            new_content = re.search("<iframe.+?src=[\"']{1}[^\"']+?youtube\.com/embed/(.+?)\?", content)
        
        if new_content:
            
            channel_id = new_content.group(1)
            
            from entertainment import youtube
            video, links = youtube.GetVideoInformation(channel_id)
            if 'best' in video:
                return (True, True, video['best'], url)
            
        return (False, False, content, url)

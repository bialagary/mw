'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class tulixcom(LiveResolver):

    implements = [LiveResolver]
    
    name = 'tulix.com'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"]http://tulix.com/player/(.+?).php[\'"]', content)

        if new_content:
        
            page_url = 'http://tulix.com/player/%s.php' % new_content.group(1)
            
            from entertainment.net import Net
            net = Net()
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            play_media = re.search('<embed type=[\'"]application/x\-shockwave\-flash[\'"] src=[\'"](.+?)[\'"].+?flashvars.+?file=(.+?)&.+?streamer=(.+?)&', content)
            
            if play_media:
            
                swf_url = play_media.group(1)
                
                playpath = play_media.group(2)
                
                streamer = play_media.group(3)
            
                content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=20 live=true'
                
                return (True, True, content, url)
                
            else:
            
                play_media = re.search('(http.+?\.m3u8)', content)
                
                if play_media:
                    
                    content = play_media.group(1)
                    
                    return (True, True, content, url)
            
        return (False, False, content, url)

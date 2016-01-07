'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class livealltv(LiveResolver):

    implements = [LiveResolver]
    
    name = 'liveall.tv'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"]{1}http://liveall\.tv/player\.php\?streampage=(.+?)[&\'"]{1}', content)

        if new_content:
        
            page_url = 'http://liveall.tv/player.php?streampage=%s' % new_content.group(1)
            
            from entertainment.net import Net
            net = Net()
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            var_a = int(re.search('var a = ([0-9]*);', content).group(1))
            var_b = int(re.search('var b = ([0-9]*);', content).group(1))
            var_c = int(re.search('var c = ([0-9]*);', content).group(1))
            var_d = int(re.search('var d = ([0-9]*);', content).group(1))
            var_f = int(re.search('var f = ([0-9]*);', content).group(1))
            var_v_part = re.search('var v_part = [\'"]{1}(.+?)[\'"]{1};', content).group(1)
            
            swf_url = 'http://wds.liveall.tv/jwplayer.flash.swf'
            
            #playpath = play_media.group(2)
            
            streamer = 'rtmp://%s.%s.%s.%s%s' % ( str(var_a/var_f), str(var_b/var_f), str(var_c/var_f), str(var_d/var_f), var_v_part  )
            ''' playpath=' + playpath + '''
            content = streamer + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=15 live=1'
            
            return (True, True, content, url)
                            
        return (False, False, content, url)

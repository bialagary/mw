'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class hqstreamtv(LiveResolver):
    implements = [LiveResolver]
    
    name = 'hqstream.tv'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search('src=[\'"]{1}http://hqstream\.tv/player\.php\?streampage=(.+?)[&\'"]{1}', content)
        
        if new_content:
        
            page_url = page_url = 'http://hqstream.tv/player.php?streampage=%s' % new_content.group(1)
            
            swf_url = 'http://filo.hqstream.tv/jwp6/jwplayer.flash.swf'
        
            from entertainment.net import Net
            net = Net()            
            
            content = net.http_GET(page_url, headers={'Referer':url}).content
            
            var_a = int ( re.search("var a = ([0-9]+);", content).group(1) )
            var_b = int ( re.search("var b = ([0-9]+);", content).group(1) )
            var_c = int ( re.search("var c = ([0-9]+);", content).group(1) )
            var_d = int ( re.search("var d = ([0-9]+);", content).group(1) )
            var_f = int ( re.search("var f = ([0-9]+);", content).group(1) )
            
            var_v_part = re.search("var v_part = [\"'](.+?)[\"'];", content).group(1) 
            
            streamer = 'rtmp://' + str(var_a/var_f) + '.' + str(var_b/var_f) + '.' + str(var_c/var_f) + '.' + str(var_d/var_f) + var_v_part
            
            content = streamer + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=20 live=true'
            
            return (True, True, content, url)
            
        return (False, False, content, url)

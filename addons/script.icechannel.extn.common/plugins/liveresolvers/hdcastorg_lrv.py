'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class hdcastorg(LiveResolver):

    implements = [LiveResolver]
    
    name = 'hdcast.org'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('<script type=[\'"]{1}text/javascript[\'"]{1}> fid=[\'"]{1}(.+?)[\'"]{1}; v_width=([0-9]*); v_height=([0-9]*);</script>.+?src=[\'"]{1}http://hdcast.org/player.js[\'"]{1}', content)

        if new_content:
        
            page_url = 'http://www.hdcast.org/player.php?u=%s&vw=%s&vh=%s&domain=%s' % (new_content.group(1), new_content.group(2), new_content.group(3), common.GetDomainFromUrl(url))
            
            from entertainment.net import Net
            net = Net()
            new_content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            streamer = re.search('[,\: \'"=]{1,5}((?:rtmp\://|rtmpe\://).+?[^\'"&=]+?)[\'"&]{1}', new_content).group(1)

            swf_url = re.search('[,\: \'"=]{1,5}(http\://.+?\.swf)[\'"&]{1}', new_content).group(1)
            
            playpath = re.search('file[,\: \'"=]{1,5}(.+?)[\'"&]{1}', new_content).group(1)
            
            content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=15 live=1'
            
            return (True, True, content, url)
                            
        return (False, False, content, url)

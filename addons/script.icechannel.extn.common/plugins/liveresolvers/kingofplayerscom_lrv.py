'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class kingofplayercom(LiveResolver):

    implements = [LiveResolver]
    
    name = 'kingofplayer.com'
    
    def ResolveLive(self, content, url):
    
        import re

        new_content = re.search('src=[\'"]{1}(http://cdn\.kingofplayers\.com/.+?\.(?:js|html))[\'"]{1}', content)

        if new_content:
        
            page_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net()
            new_content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            streamer = re.search('[,\: \'"=]{1,5}((?:rtmp\://|rtmpe\://).+?[^\'"&=]+?)[\'"&]{1}', new_content)
            if not streamer:
                new_content = re.search('src=[\'"]{1}(http://cdn\.kingofplayers\.com/.+?\.html)[\'"]{1}', new_content)
                new_url = new_content.group(1)
                new_content = net.http_GET( new_url, headers={'Referer':page_url} ).content
                page_url = new_url
                streamer = re.search('[,\: \'"=]{1,5}((?:rtmp\://|rtmpe\://).+?[^\'"&=]+?)[\'"&]{1}', new_content)
            
            streamer = streamer.group(1)
            swf_url = re.search('[,\: \'"=]{1,5}(http\://.+?\.swf)[\'"&]{1}', new_content).group(1)
            playpath = re.search('file[,\: \'"=]*([^\'"]+?)[\'"&]{1}', new_content).group(1)
            content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=15 live=1'
        
            return (True, True, content, url)
                            
        return (False, False, content, url)

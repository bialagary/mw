'''
    Ice Channel
    serverhd.eu
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class serverhdeu(LiveResolver):
    implements = [LiveResolver]
    
    name = 'serverhd.eu'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search("<script.+?src=[\"'](http://www\.serverhd\.eu/channel\.php.+?)[\"']", content)
        
        if new_content:
            page_url = new_content.group(1)
            
            from entertainment.net import Net
            net = Net()            
            content = net.http_GET( page_url, headers={'Referer':url} ).content

            new_content = re.search("<iframe.+?src=[\"'](http://www\.serverhd\.eu/embed\.php.+?)[\"']", content)
            page_url = new_content.group(1)
            content = net.http_GET( page_url, headers={'Referer':url} ).content

            import base64            
            swf_url = re.search( "SWFObject\([\"'](.+?)[\"']" ,content).group(1)
            playpath = base64.b64decode( re.search( "<input type=[\"']hidden[\"'] id=[\"']ssx1[\"'] value=[\"'](.+?)[\"']" ,content).group(1) )
            streamer = base64.b64decode( re.search( "<input type=[\"']hidden[\"'] id=[\"']ssx4[\"'] value=[\"'](.+?)[\"']" ,content).group(1) )
            
            content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=20 live=true'
            
            return (True, True, content, url)
            
        return (False, False, content, url)

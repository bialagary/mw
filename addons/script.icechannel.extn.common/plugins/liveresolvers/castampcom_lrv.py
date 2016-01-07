'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class castampcom(LiveResolver):
    implements = [LiveResolver]
    
    name = 'castamp.com'
    
    def ResolveLive(self, content, url):
    
        import re
        
        new_content = re.search("<script.+?channel=[\"'](.+?)[\"'].+?src=[\"']http://www\.castamp\.com/embed\.js[\"']", content)
        
        if new_content:
        
            chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
            chars_length = len(chars)
            string_length = 8;
            randomstring = '';
            import random
            for i in range(0,string_length):
                rnum = int(random.random() * chars_length);
                randomstring += chars[rnum:rnum+1];
        
            page_url = 'http://www.castamp.com/embed.php?c=' + new_content.group(1) + '&tk=' + randomstring
            
            from entertainment.net import Net
            net = Net()            
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            swf_url = re.search( "[\"']flashplayer[\"']: [\"'](.+?)[\"']" ,content).group(1)
            playpath = re.search( "[\"']file[\"']: [\"'](.+?)[\"']" ,content).group(1)
            streamer = re.search( "[\"']streamer[\"']: [\"'](.+?)[\"']" ,content).group(1)
            
            content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' timeout=20 live=true'
            
            return (True, True, content, url)
            
        return (False, False, content, url)

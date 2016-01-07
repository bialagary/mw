'''
    Ice Channel
    coolsport.tv
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class coolsporttv(LiveResolver):
    implements = [LiveResolver]
    
    name = 'coolsport.tv'
    
    def ResolveLive(self, content, url):

        import re
        
        new_content = re.search("<script.+?id=[\"'](.+?)[\"'].+?src=[\"']http://embeds\.coolsport\.tv/(.+?)\.js[\"']", content)
        if new_content:
            
            headers = {'Referer':url}
            page_url = 'http://embeds.coolsport.tv/' + new_content.group(2) + '.php?id=' + new_content.group(1)
            
            from entertainment.net import Net
            net = Net()            
            content = net.http_GET( page_url, headers=headers ).content
            
            return (False, True, content, page_url)
        
        new_content = re.search("<iframe.+?src=[\"'](http://www.coolsport.tv/.+?)[\"']", content)                
        if new_content:
        
            page_url = new_content.group(1)

            from entertainment.net import Net
            net = Net()            
            content = net.http_GET( page_url, headers={'Referer':url} ).content
            
            new_content = re.search("<script.+?id=[\"'](.+?)[\"'].+?src=[\"']http://embeds\.coolsport\.tv/(.+?)\.js[\"']", content)
            
            headers = {'Referer':page_url}
            page_url = 'http://embeds.coolsport.tv/' + new_content.group(2) + '.php?id=' + new_content.group(1)
            content = net.http_GET( page_url, headers=headers ).content
            
            return (False, True, content, page_url)
            
        return (False, False, content, url)

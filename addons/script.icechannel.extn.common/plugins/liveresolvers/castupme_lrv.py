'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class castupme(LiveResolver):
    implements = [LiveResolver]
    
    name = 'castup.me'
    
    def ResolveLive(self, content, url):
    
        import re
        from entertainment.net import Net
        net = Net()
        
        new_content = re.search("<script.+?fid=[\"'](.+?)[\"'].+?src=[\"']http://www\.castup\.me/js/embed\.js[\"']", content)
        
        if not new_content:
            new_content = re.search('src=[\'"]{1}(http://www\.castup\.me/channel\.php\?id=.+?)[\'"]{1}', content)
            if new_content:
                new_url = new_content.group(1)
                new_content = net.http_GET( new_content.group(1), headers={'Referer':url} ).content
                url = new_url
                new_content = re.search("<script.+?fid=[\"'](.+?)[\"'].+?src=[\"']http://www\.castup\.me/js/embed\.js[\"']", new_content)

        if new_content:
        
            page_url = 'http://www.castup.me/embed.php?channel=' + new_content.group(1)
            content = net.http_GET( page_url, headers={'Referer':url} ).content

            swf_url = re.search( "SWFObject\([\"'](.+?)[\"']" ,content).group(1)
            if 'castup.me' not in swf_url:
                swf_url = 'http://www.castup.me%s' % swf_url
            
            playpath = re.search( "so.addVariable\([\"']file[\"'].+?[\"'](.+?)[\"']" ,content).group(1)
            streamer = re.search( "so.addVariable\([\"']streamer[\"'].+?[\"'](.+?)[\"']" ,content).group(1)
            token = re.search( "so.addVariable\([\"']token[\"'].+?[\"'](.+?)[\"']" ,content).group(1)
            
            content = streamer + ' playpath=' + playpath + ' swfUrl=' + swf_url + ' pageUrl=' + page_url + ' token=' + token + ' swfVfy=1 timeout=15 live=1'
            
            return (True, True, content, url)
            
        return (False, False, content, url)

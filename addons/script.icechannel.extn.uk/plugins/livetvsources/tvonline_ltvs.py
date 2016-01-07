'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common


class tvplayer(LiveTVSource):
    implements = [LiveTVSource]
    
    name = 'TVPLAYER'
    display_name = 'TVPLAYER'
    
    source_enabled_by_default = 'true'
     

    


    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        
        from entertainment.net import Net
        import re

        net = Net(cached=False)        


        stream_id = id.replace('_','').lower()
        
 
        
        NEW_URL= "http://d3gbuig838qdtm.cloudfront.net/json/tvp/channels.json"
        
        html = net.http_GET(NEW_URL).content
        
        
        import json
        
        link=json.loads(html)

        data=link['data']
        

        for field in data:
            name= field['channel']['name'].encode("utf-8")

            url=field['channel']['id']
            if stream_id in name.replace(' ','').lower():
                
                self.AddLiveLink( list, id.replace('_',' ').upper(), url, language = language.title(),host= 'TVPLAYER',quality='HD')

    
    def Resolve(self, url):
        from entertainment.net import Net
        import re
        
        net = Net(cached=False)

        
        url='http://d2sy1af2shs9ve.cloudfront.net/tvplayer/streams/playlist/%s' % url
        
        
        response=net.http_GET(url).content

        import json
        link=json.loads(response)

        
         
        stream=link['stream']

        

        server='http://'+re.compile('http://(.+?)/').findall (stream)[0]

        m3u8=net.http_GET(stream).content     
        
        if not 'chunklist' in  m3u8 :
            
            if not 'http' in m3u8:

                match=re.compile('(.+?)\n').findall (m3u8)
                amount =len(match)-1
                g=server+match[amount]
            else:
                match=re.compile('http://(.+?)\n').findall (m3u8)
                amount =len(match)-1
                g='http://'+match[amount]
                
            M3U8_PATH=g
        else:
                
                M3U8_PATH=stream
        return M3U8_PATH        

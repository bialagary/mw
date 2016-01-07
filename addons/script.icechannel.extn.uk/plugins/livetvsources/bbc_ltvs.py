'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xml.dom.minidom as dom

class bbciplayer(LiveTVSource):
    implements = [LiveTVSource]
    
    name = 'BBC iPlayer'
    display_name = 'BBC iPlayer'
    
    source_enabled_by_default = 'true'
     

    
    def parseXML(self,url):
        from entertainment.net import Net
        net = Net(cached=False)
        xml = net.http_GET(url).content
        doc = dom.parseString(xml)
        root = doc.documentElement
        return root

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        
        from entertainment.net import Net
        import re

        net = Net(cached=False)        
        stream_id = None
        id=id.replace('bbc_one','bbc1').replace('bbc_two','bbc2').replace('bbc_three','bbc3').replace('bbc_four','bbc4').replace('news_ch','bbc_news24').replace('bbc_parliament','parliament').replace('bbc_alba','alba')   

        stream_id = id
        
        if not stream_id: return
        
        NEW_URL= "http://a.files.bbci.co.uk/media/live/manifests/hds/pc/llnw/%s.f4m"  % stream_id  
        html = net.http_GET(NEW_URL).content

        match=re.compile('<media href="(.+?)" bitrate="(.+?)"/>').findall(html.replace('amp;',''))
        for url , res in match:
            if int(res) > 800:
                res='HD'

            else:
                res='SD'
                
            self.AddLiveLink( list, id.replace('_',' ').upper(), url, language = language.title(),host= 'BBC iPLAYER ',quality=res)

    
    def Resolve(self, url):
        return url

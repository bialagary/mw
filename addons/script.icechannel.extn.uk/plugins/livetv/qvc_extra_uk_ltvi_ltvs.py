'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class qvc_extra_uk(LiveTVIndexer, LiveTVSource):
    implements = [LiveTVIndexer, LiveTVSource]
    
    display_name = "QVC Extra UK"
    
    name = 'qvc_extra_uk'
    
    base_url = 'http://qvcuk.com/ExtraChannel.content.html'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.uk'
    addon = xbmcaddon.Addon(addon_id)
    img = os.path.join( addon.getAddonInfo('path'), 'resources', 'images', name + '.png' )
    
    regions = [ 
            {
                'name':'United Kingdom', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'English', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'Shopping', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        if id == self.name:
            self.AddLiveLink(list, self.display_name, self.base_url, language='English', region='United Kingdom')
    
    def Resolve(self, url):
        resolved_media_url = ''
        
        from entertainment.net import Net
        net = Net(user_agent='Apple-iPhone/',cached=False)
        
        
        content = net.http_GET(self.base_url).content
        
        import re

                    
        resolved_media_url=re.compile('"ipadUrl":"(.+?)"').findall (content)[0]

        return resolved_media_url

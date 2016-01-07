'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class capital_tv_uk(LiveTVIndexer,LiveTVSource):
    implements = [LiveTVIndexer,LiveTVSource]
    
    display_name = "Capital TV"
    
    name = 'capital_tv_uk'
    
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
        {'name':'Music', 'img':'', 'fanart':''} 
        ]

    addon = None
    
    base_url = 'http://www.capitalfm.com/tv/player/'
    
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        if id == self.name:
            self.AddLiveLink(list, self.display_name, self.base_url, language='English', region='United Kingdom')
            
    def Resolve(self, url):
        resolved_media_url = ''
        
        from entertainment.net import Net
        net = Net()
        content =  net.http_GET(url).content
        
        import re
        playable_url = re.search('(http://.+?\.m3u8)', content)
        if playable_url:
            resolved_media_url = playable_url.group(1)
        
        return resolved_media_url
        
    
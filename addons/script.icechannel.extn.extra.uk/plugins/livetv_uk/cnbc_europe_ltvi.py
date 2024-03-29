'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class cnbc_europe(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "CNBC Europe"
    
    name = "cnbc_europe"
    
    other_names = "cnbc_europe,CNBC Europe"
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.extra.uk'
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
        {'name':'News', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    

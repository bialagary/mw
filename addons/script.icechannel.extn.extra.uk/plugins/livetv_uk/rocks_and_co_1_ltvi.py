'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class rocks_and_co_1(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Rocks & Co 1"
    
    name = "rocks_and_co_1"
    
    other_names = "rocks_and_co_1,Rocks & Co 1"
    
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
        {'name':'Shopping', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    

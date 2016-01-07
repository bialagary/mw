'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class history(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "History Channel"
    
    name = 'history'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.xunitytalk'
    addon = xbmcaddon.Addon(addon_id)
    img = os.path.join( addon.getAddonInfo('path'), 'resources', 'images', name + '.png' )
    
    regions = [ 
            {
                'name':'United States', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'English', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'General', 'img':'', 'fanart':''},
        {'name':'Entertainment', 'img':'', 'fanart':''},
        ]
    
    addon = None
    
'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class nicktoons_replay(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Nicktoons Replay"
    
    name = "nicktoons_replay"
    
    other_names = "nicktoons_replay,Nicktoons Replay"
    
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
        {'name':'+1 Channels', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
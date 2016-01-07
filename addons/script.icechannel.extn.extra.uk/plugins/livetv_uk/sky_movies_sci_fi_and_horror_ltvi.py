'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class sky_movies_sci_fi_and_horror(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Sky Movies Sci-fi & Horror"
    
    name = "sky_movies_sci_fi_and_horror"
    
    other_names = "sky_movies_sci-fi_and_horror,Sky Movies Sci-fi & Horror"
    
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
        {'name':'Movies', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    

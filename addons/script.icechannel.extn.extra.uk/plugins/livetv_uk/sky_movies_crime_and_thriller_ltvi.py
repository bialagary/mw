'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class sky_movies_crime_and_thriller(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "Sky Movies Crime & Thriller"
    
    name = "sky_movies_crime_and_thriller"
    
    other_names = "sky_movies_crime_and_thriller,Sky Movies Crime & Thriller"
    
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
    

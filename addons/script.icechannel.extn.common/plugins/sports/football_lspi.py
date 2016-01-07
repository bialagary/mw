'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Football(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Football"
    default_indexer_enabled = 'true'
    
    name = 'football'
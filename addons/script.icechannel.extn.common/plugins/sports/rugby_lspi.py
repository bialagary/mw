'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Rugby(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Rugby"
    default_indexer_enabled = 'true'
    
    name = 'rugby'
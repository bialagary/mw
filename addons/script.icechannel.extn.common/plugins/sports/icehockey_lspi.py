'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class IceHockey(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Ice Hockey"
    default_indexer_enabled = 'true'
    
    name = 'icehockey'
'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Tennis(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Tennis"
    default_indexer_enabled = 'true'
    
    name = 'tennis'
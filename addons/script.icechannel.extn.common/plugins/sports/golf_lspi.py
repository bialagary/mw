'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Golf(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Golf"
    default_indexer_enabled = 'true'
    
    name = 'golf'
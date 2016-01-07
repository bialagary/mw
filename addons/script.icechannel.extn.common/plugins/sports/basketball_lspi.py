'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Basketball(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "Basketball"
    default_indexer_enabled = 'true'
    
    name = 'basketball'
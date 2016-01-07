'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class AmericanFootball(SportsIndexer):
    implements = [SportsIndexer]
    
    display_name = "American Football"
    default_indexer_enabled = 'true'
    
    name = 'americanfootball'
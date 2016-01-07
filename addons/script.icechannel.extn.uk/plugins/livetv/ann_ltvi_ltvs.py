'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class ann(LiveTVIndexer, LiveTVSource):
    implements = [LiveTVIndexer, LiveTVSource]
    
    display_name = "ANN"
    
    name = 'ann'
    
    base_url = 'http://anntv.tv/new/webcast.aspx'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.uk'
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
        {'name':'Arabic', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'News', 'img':'', 'fanart':''} 
        ]
    
    addon = None
    
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        if id == self.name:
            self.AddLiveLink(list, self.display_name, self.base_url, language='Arabic', region='United Kingdom')
            
    def Resolve(self, url):
        resolved_media_url = ''
        
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(url).content
        
        player = 'http://anntv.tv/new/player.swf'
        
        import re
        
        content = re.search('<param name=[\'"]flashvars[\'"] value=[\'"](.+?)[\'"]>', content)
        if content:
            content = content.group(1)
            
            playpath = re.search('file=(.+?)[&\'"]', content)
            streamer = re.search('streamer=(.+?)[&\'"]', content)
        
            if streamer: streamer = streamer.group(1)
            if playpath: playpath = playpath.group(1)
        
            if not streamer and playpath and playpath.startswith('rtmp'):
                fs_index = playpath.rfind('/')
                if fs_index > 0:
                    streamer = playpath[:fs_index]
                    playpath = playpath[fs_index+1:]
                    
            if streamer and playpath:
                if playpath.endswith('.flv'):
                    playpath = playpath[:-4]
                elif playpath.endswith('.mp4'):
                    playpath = 'mp4:' + playpath
                    
                resolved_media_url = streamer + ' playpath=' + playpath + ' swfUrl=' + player + ' pageUrl=' + url + ' live=true timeout=20' 
        
        return resolved_media_url
            
'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay.interfaces import LiveResolver
from entertainment.plugnplay import Plugin
from entertainment import common

class castalbatv(LiveTVSource, LiveResolver):
    implements = [LiveTVSource, LiveResolver]
    
    display_name = "CASTALBA.TV"
    
    name = 'CASTALBA.TV'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://castalba.tv/'

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):

        search_term = id.replace('_', ' ')
        
        result = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, 'channel', title_extrctr='(' + search_term + ').+?\- castalba', exact_match=True, return_dict=True, item_count=5)
        
        if result:
            import re
            self.AddLiveLink( list, re.search( '(.+?) \- CastAlba', result.title ).group(1), result.url )
    
    def Resolve(self, url):
        resolved_media_url = ''
        
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(url).content
        
        (is_resolved, is_content_changed, media_url, url) = self.ResolveLive(content, url)
        
        if is_resolved:
            resolved_media_url = media_url
            
        return resolved_media_url
       
    def ResolveLive(self, content, url):
    
        import re        
        script_page = re.search('<script type=[\'"]text/javascript.+?id=[\'"](.+?)[\'"].+?ew=[\'"](.+?)[\'"].+?eh=[\'"](.+?)[\'"].+?src=[\'"]http://www\.castalba\.tv/js/embed\.js[\'"]', content)
        if script_page:
            channel_id = script_page.group(1)
            ew = script_page.group(2)
            eh = script_page.group(3)
            channel_url = self.base_url + 'embed.php?cid=' + channel_id + '&wh=' + ew + '&ht=' + eh
                                
            streamer = re.search('[\'"]streamer[\'"]: [\'"](.+?)[\'"]', content)
            
            if not streamer and 'castalba.tv' not in url:
                from entertainment.net import Net
                net = Net(cached=False)
                content = net.http_GET(channel_url).content
                streamer = re.search('[\'"]streamer[\'"]: [\'"](.+?)[\'"]', content)
            
            if streamer:
                streamer = streamer.group(1)
                playpath = re.search('[\'"]file[\'"]: [\'"](.+?)[\'"]', content).group(1)
                if playpath.endswith('.flv'):
                    playpath = playpath[:-4]
                elif playpath.endswith('.mp4'):
                    playpath = 'mp4:' + playpath
                
                player = re.search('[\'"]flashplayer[\'"]: [\'"](.+?)[\'"]', content).group(1)
                pageurl = channel_url
            
                resolved_media_url = streamer + ' playpath=' + playpath + ' swfUrl=' + player + ' pageUrl=' + pageurl + ' swfVfy=true live=true timeout=20'
                
                return (True, True, resolved_media_url, url)
            
        return (False, False, content, url)
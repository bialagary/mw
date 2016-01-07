'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class livestationcom(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "LIVESTATION.COM"
    
    name = 'LIVESTATION.COM'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://mobile.livestation.com/en/'    
    base_url_1 = 'http://www.livestation.com/en/'
    
    livestation_language_to_language = {
        'ar':'arabic',
        'fa':'persian',
        'en':'english',
        'es':'spanish',
        'ur':'urdu',
        'arabic':'arabic',
        'persian':'persian',
        'english':'english',
        'spanish':'spanish',
        'urdu':'urdu'
        }

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):

        search_term = id.replace('_', ' ')
        
        from entertainment.net import Net
        net = Net(cached=False)
        
        using_base_url_1 = False
        
        try:
            content = net.http_GET(self.base_url).content
            regex = '<a href="/(en/.+?/)([a-z]{2})">(.+?)</a>'
        except:
            content = net.http_GET(self.base_url_1).content
            regex = '<a href="/en/(.+?)" class="(.+?)" data\-action="(.+?)".+?data\-label="(.+?)"'
            using_base_url_1 = True
        
        import re
        for item in re.finditer(regex, content):
            item_title = item.group(4) if using_base_url_1 else item.group(3)
            item_title_id = common.CreateIdFromString( item_title )
            if item_title_id.startswith( id ):
                
                link_pt_1 = item.group(1)
                link_pt_lang = (item.group(2) + item.group(3)).lower() if using_base_url_1 else item.group(2)
                
                if using_base_url_1 and 'on_demand' in link_pt_lang: continue
                
                if using_base_url_1:
                    item_url = self.base_url + link_pt_1
                else:
                    item_url = self.base_url + link_pt_1 + link_pt_lang
                
                item_language = None
                if using_base_url_1:
                    for key,value in self.livestation_language_to_language.items():
                        if key in link_pt_lang:
                            item_language = value
                    if not item_language: item_language = 'english'
                else:
                    item_language = self.livestation_language_to_language.get( link_pt_lang, '' )
                                
                if language and item_language not in language and 'other' not in region:
                    continue
                
                self.AddLiveLink( list, item_title, item_url, language = item_language.title() )
            
    
    def Resolve(self, url):
        resolved_media_url = ''
        
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(url).content
        
        import re
        
        playable_path = re.search('<source src="(http\://.+?\.m3u8)"', content)
        if playable_path:
            resolved_media_url = playable_path.group(1)
            
        return resolved_media_url

'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class iliveto(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "ILIVE.TO"
    
    name = 'ILIVE.TO'
    
    source_enabled_by_default = 'true'
    
    base_url = 'https://www.streamlive.to/'
    
    ilive_language_to_language = {
        'english':'english',
        'spanish':'spanish',
        'portuguese':'portuguese',
        'french':'french',
        'german':'german',
        'russian':'russian',
        'vietnamese':'vietnamese',
        'italian':'italian',
        'filipino':'filipino',
        'thai':'thai',
        'chinese':'chinese',
        'indian':'hindi',
        'japanese':'japanese',
        'greek':'greek',
        'dutch':'dutch',
        'swedish':'swedish',
        'korean':'korean',
        'brazilian':'portugese',
        'romanian':'romanian'
        }
        
    ilive_language_to_region = {
        'english':'all',
        'brazilian':'brazil'
        }
    
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        search_term = id.replace('_', '+')

        from entertainment.net import Net
        net = Net()
        content = net.http_GET(self.base_url + 'channels/?q=' + search_term).content

        if '+' in search_term:
            content += net.http_GET(self.base_url + 'channels/?q=' + search_term.replace('+', '', 1)).content
        import re
        
        for item in re.finditer('(?s)(<a href="https://www.streamlive.to/view.+?</li>)', content):
            item = item.group(1)
           
            item_url = re.search('<a href="(.+?)"', item).group(1)
            #item_url = self.base_url + 'm/channel.php?n=' + re.search('<a href="https://www.streamlive.to/view/(.+?)/', item).group(1)
            item_img = re.search('src="(.+?)"', item).group(1)
            item_title = re.search('<strong>(.+?)</strong>', item,re.DOTALL).group(1).strip()
            item_language = re.search('<a href="https://www.streamlive.to/channels\?lang=[0-9]+">(.+?)</a>', item)
            if item_language:
                item_language = item_language.group(1)
            else:
                item_language = ''
            
            if language: 
                ilive_language = self.ilive_language_to_language.get( common.CreateIdFromString(item_language), '' )
                if ilive_language not in language and 'other' not in region:
                    continue

            if region: 
                ilive_region = self.ilive_language_to_region.get( common.CreateIdFromString(item_language), '' )
                if ilive_region not in region and ilive_region != 'all' and 'other' not in region:
                    continue

            self.AddLiveLink(list, item_title, item_url, 
                language=self.ilive_language_to_language.get( common.CreateIdFromString(item_language), '').title(), 
                region=self.ilive_language_to_region.get( common.CreateIdFromString(item_language), '').title(),
                img=item_img
                )
    
    def Resolve(self, url):
        resolved_media_url = ''
        import re
        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url, headers={'Referer':self.base_url}).content
        answer=re.compile('Question: (.+?) =').findall(content)[0].replace('x','*')

        data={'captcha':eval(answer)}
        content = net.http_POST(url,data, headers={'Referer':self.base_url}).content

        '''
        m3u8_url = re.search('[\'"](http.+?\.m3u8.+?)[\'"]', content)
        if m3u8_url:
            resolved_media_url = m3u8_url.group(1)
        '''
        token_url = re.compile('\$.getJSON\("(.+?)",').findall(content)[0]
        import datetime
        time_now=datetime.datetime.now()
        import time
        epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
        epoch_str = str('%f' % epoch)
        epoch_str = epoch_str.replace('.','')
        epoch_str = epoch_str[:-3]

        token_url = token_url + '&_=' + epoch_str
        token = re.compile('":"(.+?)"').findall(net.http_GET(token_url+'&_='+str(epoch), headers={'Referer':url}).content)[0]
        
        streamer = re.search('streamer: "(.+?)"', content).group(1)
        
        playpath = re.search('file: "(.+?)"', content).group(1)
        if playpath.endswith('.flv'):
            playpath = playpath[:-4]
        elif playpath.endswith('.mp4'):
            playpath = 'mp4:' + playpath
        
        player = re.search('flashplayer: "(.+?)"', content).group(1)
        pageurl = self.base_url #url
        streamer = streamer.replace('\/', '/')
        app = re.search('rtmp://[\.\w\:]*/(.*)', streamer).group(1)
        
        resolved_media_url = streamer + ' app=' + app + ' playpath=' + playpath + ' swfUrl=' + player + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=' + pageurl
        
        return resolved_media_url
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)

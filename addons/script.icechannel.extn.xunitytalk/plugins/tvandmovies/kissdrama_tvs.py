'''
    Ice Channel
    Copyright (C) 2013 the-one, Mikey1234, Coolwave
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class kissdrama(TVShowSource):
    implements = [TVShowSource]
    
    name = "Kissdrama"
    display_name = "Kissdrama"
    cookie_file = os.path.join(common.cookies_path, 'kissdrama')
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue,quality,episode):

        url=url+'|'+episode
        
        self.AddFileHost(list, quality, url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        new_url = 'http://www.kissdrama.net/index.php'
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers={'Referer':'http://www.kissdrama.net/results.php', 'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

         
        name = self.CleanTextForSearch(name)

        form_data={ 'c':'result', 'a':'retrieve', 'p':'{"KeyWord":"%s (%s)","Page":"1","NextToken":""}' % (name,year) }
        content = net.http_POST('http://www.kissdrama.net/index.php', form_data, headers).content
        
        helper = '%s (%s)' %(name,year)

        if len(episode)<2:
            episode='0%s' % episode
        
        match=re.compile('<h1 class="text"><a href="(.+?)" target="_blank">(.+?)</a>.+?width="20" height="20" />(.+?)</h3>',re.DOTALL).findall(content)
        urlselect  = []

        for url,TITLE, res in match:
            
            url= 'http://www.kissdrama.net/'+url
            if url not in urlselect:
                urlselect.append(url)

                quality = 'SD'
                res_lower = '.' + res.lower() + '.'
                for quality_key, quality_value in common.quality_dict.items():
                    if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', res_lower):
                        quality = quality_value
                        break 
        
                if year in TITLE:
                    if '>full<' in TITLE.lower():
                        self.GetFileHosts(url, list, lock, message_queue,quality,episode)
                    

    def Resolve(self, url):
        import re        
        from entertainment.net import Net
        
        episode=url.split('|')[1]
        url=url.split('|')[0]


        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        headers={'Referer':'http://www.kissdrama.net/results.php', 'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
        key = url.split('=')[1]

        form_data={ 'c':'result', 'a':'getplayerinfo', 'p':'{"KeyWord":"%s","Episode":%s,"Part":"01"}' % (key,episode) }
        content = net.http_POST('http://www.kissdrama.net/index.php', form_data, headers).content
        
        match=re.compile('src="http(.+?)"').findall(content)[0]
        
        if 'docs.google.com' in match:
            match='http'+match
            headers={'Referer':str(match), 'Host':'docs.google.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0','Connection':'keep-alive','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.5','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            
            html = net.http_GET(match, headers=headers).content.encode("utf-8").rstrip()
            video_url=re.search('fmt_stream_map".+?(http.+?),', html).group(1)
            video_url=video_url.replace('|', '').replace('\u003d','=').replace('\u0026','&')

            return video_url

        else:
            match='http'+match
            return match

        

        
                                                

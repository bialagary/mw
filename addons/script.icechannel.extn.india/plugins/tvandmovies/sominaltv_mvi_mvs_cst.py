'''
    Sominal TV
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import re

def _enk_dec_num(kode, enc):
    if re.search('fromCharCode', enc):
        x = ''
        for nbr in kode.split():
            x += chr(int(nbr) - 3)
        return x
    else:
        return None
    
def _enk_dec_swap(kode, enc):
    if re.search('charAt', enc):
        x = ''
        i = 0
        while i < (len(kode) - 1):
            x += (kode[i + 1] + kode[i])
            i += 2
        return (x + (kode[len(kode) - 1] if i < len(kode) else ''))
    else:
        return None
    
def _enk_dec_reverse(kode, enc):
    if re.search('reverse', enc):
        return kode[::-1]
    else:
        return None
        
def _enk_dec_underscores_enc(kode, enc):
    if re.search('\_k\_o\_d\_e\_', enc):
        return re.sub('\_', '', enc)
    else:
        return None
        
def _enk_dec_underscore_kode(kode, enc):
    if re.search('\_k\_o\_d\_e\_', kode):
        #return 'kode='+kode[11:]
        return re.sub('\_', '', kode)
    elif re.search('\_i\_f\_r\_a\_m\_e\_', kode):
        return re.sub('\_', '', kode)
    else:
        return None
    
ENK_DEC_FUNC = [_enk_dec_num, _enk_dec_swap, _enk_dec_reverse]


def dekode(html):
    kodeParts = re.compile('var kode\="kode\=\\\\"(.+?)\\\\";(.+?);"').findall(html)
    if len(kodeParts) == 0:
        return None
    kode = None
    while len(kodeParts) == 1:
        
        kode = kodeParts[0][0].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        enc = kodeParts[0][1].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')        
        for dec_func in ENK_DEC_FUNC:
            #print '-------------------------------11'        
            #print kode
            #print enc
            x = dec_func(kode, enc)
            if x is not None:
                kode = x           
                #print kode
        
        kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
        if len(kodeParts) != 1 and 'iframe' not in kode:
            x = _enk_dec_underscore_kode(kode, enc)
            if x is not None:
                kode = x
                kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
        if len(kodeParts) != 1 and 'iframe' not in kode:
            x = _enk_dec_swap(kode, enc)
            if x is not None:
                kode = x
                kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))

    dekoded = kode.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return dekoded            


class sominaltv(MovieIndexer, MovieSource, CustomSettings):
    implements = [MovieIndexer, MovieSource, CustomSettings]
    
    name = "sominaltv"
    display_name = "Sominal TV"
    base_url = 'http://www.sominaltvfilms.com/'    
    
    default_indexer_enabled = 'false'
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="user" label="User ID" type="text" default="" />\n'
        xml += '<setting id="pass" type="text" option="hidden" label="Password" default="" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        
        self.CreateSettings(self.name, self.display_name, xml)
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        import urllib
        
        if section != 'search':
            url = urllib.unquote_plus(url)
        
        new_url = url
                
        if not new_url.startswith(self.base_url):
            new_url = re.sub("http\://.*?/", self.base_url, url)
        
        if page == '':
            page = '1'
            
        from entertainment.net import Net
        cached = False if section == 'watchlist' else True
        net = Net(cached=cached)

        content = net.http_GET(new_url + '/page/' + page).content
        
        if total_pages == '' :
            re_page =  '<span class=[\'"]{1}pages[\'"]{1}>Page 1 of ([0-9]+)</span>' #'<a class=[\'"]{1}last[\'"]{1}.+?([0-9]+)[\'"]{1}'
            total_pages = re.search(re_page, content)
            if total_pages:
                total_pages = total_pages.group(1)
            else:
                if re.search('0 items found', content):
                    page = '0'
                    total_pages = '0'
                else:
                    page = '1'
                    total_pages = '1'

        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
        
        item_re = r'(?s)<div class=[\'"]{1}inner[\'"]{1}>.+?<a href=[\'"]{1}(.+?)[\'"]{1}.+?<img src=[\'"]{1}(.+?)[\'"]{1} alt=[\'"]{1}(.+?)[\'"]{1}.+?<p>(.+?)<'

        for item in re.finditer(item_re, content):
            
            item_url = item.group(1)
            
            item_img = item.group(2)
            
            item_alt = item.group(3)
            item_name = re.sub('\([0-9]+\).*', '', item_alt)
            item_year = re.search("\(([0-9]+)", item_alt)
            if item_year:
                item_year = item_year.group(1)
                item_title = item_name + ' (' + item_year + ')'
            else:
                item_year = ''
                item_title = item_name
            
            if total_pages == '':
                total_pages = '1'
                
            item_plot = re.sub('^\s', '', common.CleanText(item.group(4), True, True) )
            
            self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year, img=item_img, plot=item_plot)
            
        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
    
        if indexer != common.indxr_Movies:
            return

        url_type = ''
        content_type = ''
            
        if section == 'main':
            self.AddSection(list, indexer, 'recent', 'Recently Added')
            self.AddSection(list, indexer, 'popular', 'Most Popular')
            self.AddSection(list, indexer, 'latest_dvds', 'Latest DVDs')
            self.AddSection(list, indexer, 'theatres', 'In Theatres Now')
            self.AddSection(list, indexer, 'recent_blurays', 'Recent Blurays')
            self.AddSection(list, indexer, 'year', 'Year')
            self.AddSection(list, indexer, 'browse', 'Browse')
            self.AddSection(list, indexer, 'blurays', 'Blurays')                        
            self.AddSection(list, indexer, 'english_subtitled', 'English Subtitled')
        elif section in ('latest_dvds', 'theatres', 'recent_blurays') :
            
            from entertainment.net import Net
            net = Net()
            content = net.http_GET(self.base_url).content
            
            import re
            
            if section == 'latest_dvds': section_header='Latest DVDs'
            elif section == 'theatres': section_header='Now Playing in Theaters'
            elif section == 'recent_blurays': section_header='Recently Added BluRays'
            
            
            section_content = re.search('(?s)<h2><b>' + section_header + '(.+?)<h2><b>', content).group(1)
            
            item_re = r'(?s)<article.+?<a href=[\'"]{1}(.+?)[\'"]{1}.+?<img src=[\'"]{1}(.+?)[\'"]{1} alt=[\'"]{1}(.+?)[\'"]{1}'

            for item in re.finditer(item_re, section_content):
                
                item_url = item.group(1)
                
                item_img = item.group(2)
                
                item_alt = item.group(3)
                item_name = re.sub('\([0-9]+\).*', '', item_alt)
                item_year = re.search("\(([0-9]+)", item_alt)
                if item_year:
                    item_year = item_year.group(1)
                    item_title = item_name + ' (' + item_year + ')'
                else:
                    item_year = ''
                    item_title = item_name
                
                if total_pages == '':
                    total_pages = '1'
                    
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year, img=item_img)
        elif section in ('recent', 'popular') :
            
            from entertainment.net import Net
            net = Net()
            content = net.http_GET(self.base_url).content
            
            import re
            
            if section == 'recent': section_header='Recently Added'
            elif section == 'popular': section_header='Most Popular'
            
            section_content = re.search('(?s)<h3 class="widgettitle">' + section_header + '.+?<ul>(.+?)</ul>', content).group(1)
            
            item_re = r'(?s)<li.+?<a href=[\'"]{1}(.+?)[\'"]{1}.+?<img src=[\'"]{1}(.+?)[\'"]{1} alt=[\'"]{1}(.+?)[\'"]{1}'

            for item in re.finditer(item_re, section_content):
                
                item_url = item.group(1)
                
                item_img = item.group(2)
                
                item_alt = item.group(3)
                item_name = re.sub('\([0-9]+\).*', '', item_alt)
                item_year = re.search("\(([0-9]+)", item_alt)
                if item_year:
                    item_year = item_year.group(1)
                    item_title = item_name + ' (' + item_year + ')'
                else:
                    item_year = ''
                    item_title = item_name
                
                if total_pages == '':
                    total_pages = '1'
                    
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year, img=item_img)
        elif section== 'browse':
            self.AddSection(list, indexer, 'all', 'All', self.base_url+'browse', indexer)
            self.AddSection(list, indexer, 'hindi', 'Hindi', self.base_url+'hindi-movies', indexer)
            self.AddSection(list, indexer, 'telugu', 'Telugu', self.base_url+'telugu-movies', indexer)
            self.AddSection(list, indexer, 'tamil', 'Tamil', self.base_url+'tamil-movies', indexer)
            self.AddSection(list, indexer, 'malayalam', 'Malayalam', self.base_url+'malayalam-movies', indexer)
            self.AddSection(list, indexer, 'punjabi', 'Punjabi', self.base_url+'punjabi-movies', indexer)
            self.AddSection(list, indexer, 'hindi_dubbed', 'Hindi Dubbed', self.base_url+'category/hindi-dubbed', indexer)
        elif section== 'blurays':
            self.AddSection(list, indexer, 'all', 'All', self.base_url+'blurays', indexer)
            self.AddSection(list, indexer, 'hindi', 'Hindi', self.base_url+'hindi-blurays', indexer)
            self.AddSection(list, indexer, 'telugu', 'Telugu', self.base_url+'telugu-blurays', indexer)
            self.AddSection(list, indexer, 'tamil', 'Tamil', self.base_url+'tamil-blurays', indexer)
        elif section== 'english_subtitled':
            self.AddSection(list, indexer, 'all', 'All', self.base_url+'english-subtitles', indexer)
            self.AddSection(list, indexer, 'hindi', 'Hindi', self.base_url+'hindi-movies-english-subtitles', indexer)
            self.AddSection(list, indexer, 'telugu', 'Telugu', self.base_url+'telugu-movies-english-subtitles', indexer)
            self.AddSection(list, indexer, 'tamil', 'Tamil', self.base_url+'tamil-movies-english-subtitles', indexer)
            self.AddSection(list, indexer, 'malayalam', 'Malayalam', self.base_url+'malayalam-movies-english-subtitles', indexer)
            self.AddSection(list, indexer, 'punjabi', 'Punjabi', self.base_url+'punjabi-movies-english-subtitles', indexer)
        elif section== 'year':
            from datetime import date
            for i in range(date.today().year, 1999, -1):
                self.AddSection(list, indexer, 'year'+str(i), str(i), self.base_url+'/category/'+str(i), indexer)
            self.AddSection(list, indexer, 'year_pre_2000', 'Pre 2000', self.base_url+'/category/pre-2000', indexer)
            
            
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    
        
    
    def GetFileHosts(self, url, list, lock, message_queue): 

        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        
        global_quality = 'DVD'
        
        pg_title = re.search('<title>(.+?)</title>', content).group(1).lower()        
        if 'dvdscr' in pg_title: global_quality='DVDSCR'
        elif 'bluray' in pg_title: global_quality='HD'
        
        quality = global_quality
        old_quality = quality
        host_url = ''
        
        new_format = False
        for sq in re.finditer('(?:(?:class=[\'"]{1}btn)|(?:<p style="text\-align: center;"><span style="font\-size: 20px;))(.+?)</p>', content):

            new_format = True
            
            sq_item = sq.group(1)

            sq_name = re.search('<strong>(.+?)</strong>', sq_item)
            if sq_name: sq_name=sq_name.group(1).lower()
            else: sq_name=''
            
            if 'dvdscr' in sq_name: 
                old_quality = quality
                quality = 'DVDSCR'
            elif 'dvd' in sq_name: 
                old_quality = quality
                quality = 'DVD'
            elif 'bluray' in sq_name: 
                old_quality = quality
                quality = 'HD'
            
            sq_url = re.search('href=[\'"]{1}(.+?)[\'"]{1}', sq_item)
            if sq_url:
                sq_url = sq_url.group(1)
                if 'adf.ly' in sq_url: sq_url = re.sub('http.+?http', 'http', sq_url)
                if 'part' in sq_name or 'part' in sq_url: host_url += sq_url + '|||part|||'
                elif 'source' in sq_name or 'full' in sq_name: self.AddFileHost(list, old_quality, sq_url, host=self.display_name)
                elif 'premium' in sq_name or 'playsominaltv.com' in sq_url:
                    if host_url and len(host_url) > 0:
                        self.AddFileHost(list, old_quality, host_url, host=self.display_name)
                        host_url = ''
                    self.AddFileHost(list, global_quality, sq_url, host=self.display_name + ' (Premium)')
            else:
                if host_url and len(host_url) > 0:
                    self.AddFileHost(list, old_quality, host_url, host=self.display_name)
                    old_quality=quality
                    host_url = ''
                    
        if new_format == False:
            host_url = re.search('<a href=[\'"]{1}http://adf.ly/.+?/(.+?)[\'"]{1}', content)
            if host_url:
                host_url = host_url.group(1)

                host_content = net.http_GET(host_url).content
                video_url = ''
                for i, video_content in enumerate(re.finditer('<iframe.+?src=[\'"]{1}(.+?)[\'"]{1}', host_content)):
                    if i==0: video_url = video_content.group(1)
                    else: video_url += '|||part|||' + video_content.group(1)
                if video_url and len(video_url) > 0: self.AddFileHost(list, global_quality, video_url)

        
        
    def Resolve(self, url):
        
        from entertainment.net import Net
        net = Net()
        
        if 'playsominaltv.com' in url:
            
            net._cached = False
            
            premium_url = 'http://www.playsominaltv.com/login/?redirect_to=' + url
            content = net.http_GET(premium_url, headers={'Referer':url}).content
            params={'log':self.Settings().get_setting('user'), 'pwd':self.Settings().get_setting('pass'), 'wp-submit':'1'}
            for hidden_param in re.finditer('(<input.+?type=[\'"]{1}hidden[\'"]{1}.+?/>)', content):
                hidden_param_input = hidden_param.group(1)
                param_name = re.search('name=[\'"]{1}(.+?)[\'"]{1}', hidden_param_input).group(1)
                param_value = re.search('value=[\'"]{1}(.+?)[\'"]{1}', hidden_param_input).group(1)
                params.update( { param_name : param_value } )
            content = net.http_POST('http://www.playsominaltv.com/login/',params,headers={'Referer':premium_url}).content
        
        if 'playsominaltv.com' in url or 'sominaltvfilms.com' in url or 'desionlinetheater.com' in url:
            content = net.http_GET(url).content
            content=dekode(content)
            if content:
                source_url=re.search('<iframe.+?src.+?(http.+?)[\'"\\\\]{1}', content)
                if source_url:
                    return MovieSource.Resolve(self, source_url.group(1))
        else:
            return MovieSource.Resolve(self, url)
            
        return url
        
            
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue): 
    
        from entertainment.net import Net
        net = Net()
        
        title = self.CleanTextForSearch(title) 
        title_id = common.CreateIdFromString(title)
        
        name = self.CleanTextForSearch(name) 
        name_id = common.CreateIdFromString(name)
        
        import urllib
        search_page_url = self.base_url + '?s=' + urllib.quote_plus(title) + '&submit=Search'
        
        content = net.http_GET(search_page_url).content
        
        item_re = r'(?s)<div class=[\'"]{1}inner[\'"]{1}>.+?<a href=[\'"]{1}(.+?)[\'"]{1}.+?<img src=[\'"]{1}(.+?)[\'"]{1} alt=[\'"]{1}(.+?)[\'"]{1}.+?<p>(.+?)<'

        for item in re.finditer(item_re, content):
            
            item_url = item.group(1)
            
            item_alt = item.group(3)
            item_name = re.sub('\([0-9]+\).*', '', item_alt)
            item_year = re.search("\(([0-9]+)", item_alt)
            if item_year:
                item_year = item_year.group(1)
                item_title = item_name + ' (' + item_year + ')'
            else:
                item_year = ''
                item_title = item_name

            if common.CreateIdFromString(item_title) == title_id or common.CreateIdFromString(item_name) == name_id:
                self.GetFileHosts(item_url, list, lock, message_queue)
            else:
                break

            
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 

        from entertainment.net import Net
        net = Net() 
        
        keywords = self.CleanTextForSearch(keywords) 
        
        if page == '': page = '1'
        
        import urllib
        search_for_url = self.base_url + '/page/' + page + '?s=' + urllib.quote_plus(keywords) + '&submit=Search'
        
        content = net.http_GET(search_for_url).content        
        
        if "<div class='big-title'>Oops!</div>" in content:            
            return
        
        keywords_lower = keywords.lower().split(' ')
        match_total = float( len(keywords_lower) )
        
        if total_pages == '':
            total_pages = '1'

        if int(page) == int(total_pages):
            total_pages = str(int(total_pages) + 1)
            
        item_re = r'(?s)<div class=[\'"]{1}inner[\'"]{1}>.+?<a href=[\'"]{1}(.+?)[\'"]{1}.+?<img src=[\'"]{1}(.+?)[\'"]{1} alt=[\'"]{1}(.+?)[\'"]{1}.+?<p>(.+?)<'

        info_added = False
        
        for item in re.finditer(item_re, content):
            item_alt = item.group(3)
            
            if 'trailer' in item_alt.lower(): continue
            
            item_name = re.sub('\([0-9]+\).*', '', item_alt)
            item_year = re.search("\(([0-9]+)", item_alt)
            if item_year:
                item_year = item_year.group(1)
                item_title = item_name + ' (' + item_year + ')'
            else:
                item_year = ''
                item_title = item_name
                
            item_match = '.' + item_name + '.' + item_year + '.'
            item_match_lower = item_match.lower()
            item_match_count = 0
            for kywd in keywords_lower:
                if re.search('[^a-zA-Z0-9]'+kywd+'[^a-zA-Z0-9]', item_match_lower): 
                    item_match_count+=1

            if item_match_count/match_total > 0.5:
                if info_added == False:                    
                    self.AddInfo(list, indexer, 'search', self.base_url, type, page, total_pages)
                    info_added = True
                
                item_url = item.group(1)
                
                if 'trailer' in item_url.lower(): continue

                item_img = item.group(2)
                
                item_plot = re.sub('^\s', '', common.CleanText(item.group(4), True, True) )
            
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year, img=item_img, plot=item_plot)
            
        if info_added == False:
            self.AddInfo(list, indexer, 'search', self.base_url, type, page, page)
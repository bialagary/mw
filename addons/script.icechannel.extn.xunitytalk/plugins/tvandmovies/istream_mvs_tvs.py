'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
from BeautifulSoup import BeautifulSoup as soup

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class iStream(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
    
    name = "iStream"
    display_name = "iStream"
    
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import base64
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)

        def unpack_js(p, k):
            k = k.split('|')
            for x in range(len(k) - 1, -1, -1):
                if k[x]:
                    p = re.sub('\\b%s\\b' % base36encode(x), k[x], p)
            return p

        def base36encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
            if not isinstance(number, (int, long)):
                raise TypeError('number must be an integer')
     
            if number == 0:
                return alphabet[0]
            base36 = ''
            sign = ''
            if number < 0:
                sign = '-'
                number = - number
            while number != 0:
                number, i = divmod(number, len(alphabet))
                base36 = alphabet[i] + base36
            return sign + base36
        
        sources = [] ; final = []
        html = soup(net.http_GET(url).content)


        links = html.findAll('script')
        for link in links:
            try:
                if 'eval' in link.contents[0]:
                    r = re.search('return p}\(\'(.+?);\',\d+,\d+,\'(.+?)\'\.split',link.contents[0])
                    if r: p, k = r.groups()
                    try: sources.append((base64.b64decode(unpack_js(p, k).split('"')[1]).split('>')[1].split('<')[0]))
                    except:pass
            except IndexError : pass
        for link in sources:
            if 'www' not in link.split('//')[1].split('.')[0]:
                final.append((link.split('//')[1].split('.')[0],link))
            else: final.append((link.split('//')[1].split('.')[1],link))
        for title,blob in final:

            if not 'watchfreeinhd' in title.lower():

                self.AddFileHost(list, 'SD', blob)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        import cgi
        search_term = re.sub('\A(a|A|the|THE|The)\s','',name)
        search_term_escaped = cgi.escape(search_term)
        
        if type == 'tv_episodes':
            tv_search_term = '%s</a>'%search_term
            tv_search_term_escaped = '%s</a>'%search_term_escaped

            episode_term = 'episode %sx%s'%(season,episode)
            
            tv_url = 'http://watchmoviesonline.mobi/?&search='+name.replace(' ','+')+'&listtype=m1'

            content = net.http_GET(tv_url).content
            
            html=content.split('<td style="vertical-align:top;">')
            
            for p in html:
                
                if tv_search_term in p or tv_search_term_escaped in p or re.sub('</a>\Z', ' </a>', tv_search_term) in p or re.sub('</a>\Z', ' </a>', tv_search_term_escaped) in p:
                    
                    match=re.compile('<a href="(.+?)" style="').findall(p)

                    for url in match:
                        
                        ep_url = re.search('title/(.+?)/', url)
                        if ep_url:
                            ep_url = ep_url.group(1)
                            
                            new_tv_url='http://watchmoviesonline.mobi'+url+'?m='+ep_url+'&s='+season+'&e='+episode

                            self.GetFileHosts(new_tv_url, list, lock, message_queue)
                        
                
            

                

            
        elif type == 'movies':
            
            movie_search_term = '%s</a> (%s)<div'%(search_term,year)
            movie_search_term_escaped = '%s</a> (%s)<div'%(search_term_escaped,year)

            movie_url = 'http://watchmoviesonline.mobi/?&search='+name.replace(' ','+') + '+' + year+'&listtype=m1'

            content = net.http_GET(movie_url).content
            
            #if 'Sorry for this interruption but we have detected an elevated amount of request from your IP' in content:
            #    go_back_link = re.search('<a href="http://watchmoviesonline.mobi/human?goback=(.+?)"', content)
            #    if go_back_link:
            #        go_back_link = 'http://watchmoviesonline.mobi/human?goback=' + go_back_link.group(1)
            #        content = net.http_GET(go_back_link, headers={}).content
            
            
            html=content.split('<td style="vertical-align:top;">')
            
            for p in html:
                
                if movie_search_term in p or movie_search_term_escaped in p:

                    if year in p:

                        match=re.compile('<a href="(.+?)" style="').findall(p)

                        for url in match:

                            self.GetFileHosts('http://watchmoviesonline.mobi'+url, list, lock, message_queue)
                        
            if not list:
            
                movie_url = 'http://watchmoviesonline.mobi/?&search='+name.replace(' ','+')+'&listtype=m1'

                content = net.http_GET(movie_url).content
                
                html=content.split('<td style="vertical-align:top;">')
                
                for p in html:
                    
                    if search_term in p:

                        if year in p:

                            match=re.compile('<a href="(.+?)" style="').findall(p)

                            for url in match:

                                self.GetFileHosts('http://watchmoviesonline.mobi'+url, list, lock, message_queue)
                            

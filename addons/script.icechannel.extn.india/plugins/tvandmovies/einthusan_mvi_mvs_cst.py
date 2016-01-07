'''
    einthusan    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui



do_no_cache_keywords_list = ["alert('Please Login!');"]

class einthusan(MovieIndexer,MovieSource,CustomSettings):
    implements = [MovieIndexer,MovieSource,CustomSettings]
    
    name = "einthusan"
    display_name = "Einthusan"
    base_url = 'http://www.einthusan.com'
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/3be7233fb53b60bcad8f724d33ae8a514d91a588/Einthusan.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    cookie_file = os.path.join(common.cookies_path, 'einthusan-login.cookie')
    icon = common.notify_icon
    
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your username" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)


    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'Recently Posted':
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'www.einthusan.com', 'Origin': 'http://www.einthusan.com',
                       'Referer': 'http://www.einthusan.com/index.php?lang=hindi',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}


            net.http_GET('http://www.einthusan.com/etc/login.php')
            net.http_POST('http://www.einthusan.com/etc/login.php', {'username': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            lang = url.split('=')[1].split('&')[0]
            print lang
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = 'http://www.einthusan.com/movies/index.php?lang='+lang+'&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page='+page

            import urllib        
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url+'&page='+str(page)).content                          
              
            if total_pages == '':
                r= '>([0-9]*)</a></div></div><div id="footer"'
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'Recently Posted', url, type, str(page), total_pages)
            
            match=re.compile('<h1><a class="movie-title" href="..(.+?)">(.+?)</a></h1>').findall(html)
            for url, name in match:
                name = self.CleanTextForSearch(name)
                name=re.sub('\((Hindi|hindi|Tamil|tamil|Telugu|telugu|Malayalam|malayalam)\)','', name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url, name=name)


        else:
            print 'BLUERAY____________________________________________________________________'
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'www.einthusan.com', 'Origin': 'http://www.einthusan.com',
                       'Referer': 'http://www.einthusan.com/index.php?lang=hindi',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}


            net.http_GET('http://www.einthusan.com/etc/login.php')
            net.http_POST('http://www.einthusan.com/etc/login.php', {'username': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            lang = url.split('=')[1].split('&')[0]
            print lang
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = 'http://www.einthusan.com/bluray/index.php?lang='+lang+'&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page='+page

            import urllib        
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url+'&page='+str(page)).content                          
              
            if total_pages == '':
                r= '>([0-9]*)</a></div></div><div id="footer"'
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'Recently Postedb', url, type, str(page), total_pages)
            
            match=re.compile('<h1><a class="movie-title" href="..(.+?)">(.+?) Blu-ray</a></h1>').findall(html)
            for url, name in match:
                name = self.CleanTextForSearch(name)
                name=re.sub('\((Hindi|hindi|Tamil|tamil|Telugu|telugu|Malayalam|malayalam)\)','', name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url, name=name)           

        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        net = Net()

        url_type = ''
        content_type = ''
        

        if section == 'main':
            self.AddSection(list, indexer,'tamil','[COLOR red]Tamil[/COLOR]',self.base_url +'/index.php?lang=tamil',indexer)
            self.AddSection(list, indexer,'hindi','[COLOR purple]Hindi[/COLOR]',self.base_url +'/index.php?lang=hindi',indexer)
            self.AddSection(list, indexer,'telugu','[COLOR royalblue]Telugu[/COLOR]',self.base_url +'/index.php?lang=telugu',indexer)
            self.AddSection(list, indexer,'malayalam','[COLOR green]Malayalam[/COLOR]',self.base_url +'/index.php?lang=malayalam',indexer)

        elif section == 'tamil' or  section == 'hindi' or  section == 'telugu' or  section == 'malayalam':
            self.AddSection(list, indexer,'activity','HD Movies',self.base_url +'/movies/index.php?lang='+section,indexer)
            self.AddSection(list, indexer,'activityb','Blu-ray',self.base_url +'/bluray/index.php?lang='+section,indexer)
                       
        elif section == 'activity':
            self.AddSection(list, indexer,'Recently Posted','Recently Posted',url+'&organize=Activity&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'alphabetical','Alphabetical',url+'&organize=Alphabetical&filtered=RecentlyViewed&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Cast','Cast',url+'&organize=Cast&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Year','Year',url+'&organize=Year&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Rating','Rating',url+'&organize=Rating&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Director','Director',url+'&organize=Director&filtered=RecentlyPosted&org_type=Activity',indexer)

        elif section == 'activityb':
            self.AddSection(list, indexer,'Recently Postedb','Recently Posted',url+'&organize=Activity&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'alphabeticalb','Alphabetical',url+'&organize=Alphabetical&filtered=RecentlyViewed&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Castb','Cast',url+'&organize=Cast&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Yearb','Year',url+'&organize=Year&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Ratingb','Rating',url+'&organize=Rating&filtered=RecentlyPosted&org_type=Activity',indexer)
            self.AddSection(list, indexer,'Directorb','Director',url+'&organize=Director&filtered=RecentlyPosted&org_type=Activity',indexer)


        elif section == 'alphabetical':
            r = re.findall(r'<a href=".+?Alphabetical">(.+?)</a>', net.http_GET(url).content, re.I)
            for abc in r[0:]:
                abc_title = abc.upper()
                self.AddSection(list, indexer, 'Recently Posted', abc_title, url+'&organize=Alphabetical&filtered='+abc+'&org_type=Alphabetical', indexer)

        elif section == 'Cast':
            r = re.findall(r'=Cast">(.+?)</a>', net.http_GET(url).content, re.I)
            for cast in r[0:]:
                cast = common.CleanText(cast, True, True)
                cast_title = cast.upper()
                self.AddSection(list, indexer, 'Recently Posted', cast_title, url+'&organize=Cast&filtered='+cast+'&org_type=Cast', indexer)

        elif section == 'Year':
            r = re.findall(r'=Year">(.+?)</a>', net.http_GET(url).content, re.I)
            for year in r[0:]:
                year = common.CleanText(year, True, True)
                year_title = year.upper()
                self.AddSection(list, indexer, 'Recently Posted', year_title, url+'&organize=Year&filtered='+year+'&org_type=Year', indexer)

        elif section == 'Rating':
            r = re.findall(r'=Rating">(.+?)</a>', net.http_GET(url).content, re.I)
            for rating in r[0:]:
                rating = common.CleanText(rating, True, True)
                rating_title = rating.upper()
                self.AddSection(list, indexer, 'Recently Posted', rating_title, url+'&organize=Rating&filtered='+rating+'&org_type=Rating', indexer)

        elif section == 'Director':
            r = re.findall(r'=Director">(.+?)</a>', net.http_GET(url).content, re.I)
            for director in r[0:]:
                director = common.CleanText(director, True, True)
                director_title = director.upper()
                self.AddSection(list, indexer, 'Recently Posted', director_title, url+'&organize=Director&filtered='+director+'&org_type=Director', indexer)

        #####################################################################################################################################################

        elif section == 'alphabeticalb':
            r = re.findall(r'<a href=".+?Alphabetical">(.+?)</a>', net.http_GET(url).content, re.I)
            for abc in r[0:]:
                abc_title = abc.upper()
                self.AddSection(list, indexer, 'Recently Posted', abc_title, url+'&organize=Alphabetical&filtered='+abc+'&org_type=Alphabetical', indexer)

        elif section == 'Castb':
            r = re.findall(r'=Cast">(.+?)</a>', net.http_GET(url).content, re.I)
            for cast in r[0:]:
                cast = common.CleanText(cast, True, True)
                cast_title = cast.upper()
                self.AddSection(list, indexer, 'Recently Posted', cast_title, url+'&organize=Cast&filtered='+cast+'&org_type=Cast', indexer)

        elif section == 'Yearb':
            r = re.findall(r'=Year">(.+?)</a>', net.http_GET(url).content, re.I)
            for year in r[0:]:
                year = common.CleanText(year, True, True)
                year_title = year.upper()
                self.AddSection(list, indexer, 'Recently Posted', year_title, url+'&organize=Year&filtered='+year+'&org_type=Year', indexer)

        elif section == 'Ratingb':
            r = re.findall(r'=Rating">(.+?)</a>', net.http_GET(url).content, re.I)
            for rating in r[0:]:
                rating = common.CleanText(rating, True, True)
                rating_title = rating.upper()
                self.AddSection(list, indexer, 'Recently Posted', rating_title, url+'&organize=Rating&filtered='+rating+'&org_type=Rating', indexer)

        elif section == 'Directorb':
            r = re.findall(r'=Director">(.+?)</a>', net.http_GET(url).content, re.I)
            for director in r[0:]:
                director = common.CleanText(director, True, True)
                director_title = director.upper()
                self.AddSection(list, indexer, 'Recently Posted', director_title, url+'&organize=Director&filtered='+director+'&org_type=Director', indexer)
            
                        

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net(cached=False)
        net.set_cookies(self.cookie_file)
        content = net.http_GET(url).content
        
        resolved_url = re.compile("{ 'file': '(.+?)'").findall(content)[0]

        self.AddFileHost(list, 'HD', resolved_url,'EINTHUSAN.COM')
                
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)

        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')
            

        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                   'Host': 'www.einthusan.com', 'Origin': 'http://www.einthusan.com',
                   'Referer': 'http://www.einthusan.com/index.php?lang=hindi',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}


        net.http_GET('http://www.einthusan.com/etc/login.php')
        net.http_POST('http://www.einthusan.com/etc/login.php', {'username': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
        net.save_cookies(self.cookie_file)
        net.set_cookies(self.cookie_file)  
                                
        name = self.CleanTextForSearch(name)
        
        import urllib
        
        movie_url=self.GoogleSearchByTitleReturnFirstResultOnlyIfValid('einthusan.com', name, 'watch.php', item_count=10, title_extrctr='(.+?) (?:Hindi|hindi|Tamil|tamil|Telugu|telugu|Malayalam|malayalam) movie')
        if movie_url:
            self.GetFileHosts(movie_url, list, lock, message_queue)
                        
            
    #def Resolve(self, url):
        #import re
        #from entertainment.net import Net
        #net = Net(cached=False)
        #net.set_cookies(self.cookie_file)
        #content = net.http_GET(url).content
        #fileid = re.compile('"file": "(.+?)"').findall(content)[0]
        
        #resolved_url = net.http_GET('http://noobroom5.com'+fileid, headers={'Rrferer':url}, auto_read_response=False).get_url()
        #return resolved_url
         

    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 

        from entertainment.net import Net
        net = Net() 
        
        keywords = self.CleanTextForSearch(keywords) 
        
        if page == '': page = '1'
        
        if total_pages == '':
            total_pages = '1'

        if int(page) == int(total_pages):
            total_pages = str(int(total_pages) + 1)
        
        search_results = self.GoogleSearch('einthusan.com', keywords, 'watch.php', int(page))

        if search_results and len(search_results) > 0:
            
            import re
            
            keywords_lower = keywords.lower().split(' ')
            match_total = float( len(keywords_lower) )
            
            info_added = False
            
            for si in search_results:
                si_url = si['url']
                si_title = si['title']
                item_name = re.search('^(.+?) (?:Hindi|hindi|Tamil|tamil|Telugu|telugu|Malayalam|malayalam)', si_title).group(1)
                item_year = ''
                item_title = item_name
                item_url = si_url
                
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
                
                    self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year)
                
            if info_added == False:
                self.AddInfo(list, indexer, 'search', self.base_url, type, page, page)    
            
        else:
            self.AddInfo(list, indexer, 'search', self.base_url, type, page, page)

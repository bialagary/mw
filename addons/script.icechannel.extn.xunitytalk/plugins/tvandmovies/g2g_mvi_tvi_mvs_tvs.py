'''
    g2g.so  # OdrtKapH2dNRpVHxhBtg 
    Copyright (C) 2013 
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
#from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui


class g2g(MovieIndexer,TVShowIndexer,MovieSource,TVShowSource):
    implements = [MovieIndexer,TVShowIndexer,MovieSource,TVShowSource]
    
    name = "g2g"
    display_name = "g2g.so"
    base_url = 'http://g2g.so/'
    #img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/92bed8a40419803f31f90e2268956db50d306997/flixanity.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'
    cookie_file = os.path.join(common.cookies_path, 'g2glogin.cookie')
    icon = common.notify_icon
    
    '''
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your noobroom email" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '<setting label="Premium account will allow for 1080 movies and the TV Shows section" type="lsep" />\n'
        xml += '<setting id="premium" type="bool" label="Enable Premium account" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
    '''

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'latest':
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            #total_pages = '7'
            
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
                   
                
            self.AddInfo(list, indexer, 'latest', url, type, str(page), total_pages)

            for item in re.finditer(r'<span class="leftgg"> <a href="(.+?)" id=".+?"><img onerror=.+?href=".+?" id=".+?">(.+?)(\([\d]{4}\)) .+?Online Streaming</a>',html,re.I|re.DOTALL):
                url='http://g2g.so/forum/'+item.group(1)
                url=url.split('&')[0]
                print url
                name=item.group(2)
                item_year=item.group(3).replace('(','').replace(')','')
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)

        if section == 'tvshows':
            
            new_url = url
                        
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content 
                
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?)"',html,re.I):
                url='http://g2g.so/tvseries/'+item.group(1)
                print url
                url=url.split('&')[0]
                print url
                name=item.group(2)
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_Content,name,'','tv_seasons', url=url, name=name)

        if section == 'tvshowslatest':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            total_pages='6'
            '''
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
            '''           
            self.AddInfo(list, indexer, 'tvshowslatest', url, type, str(page), total_pages)   
                                        
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?) S(\d+)E(\d+)"',html,re.I):
                url='http://g2g.so/episodes/'+item.group(1)
                url=url.split('&')[0]
                print url
                name=item.group(2)
                season=item.group(3)
                episode=item.group(4)
                name = self.CleanTextForSearch(name)
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + episode)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, name+' S'+season+'E'+episode, item_id, 'tv_episodes', url=url, name=name, season=season, episode=episode)
                   
        else:
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + 'index.php?&page=' + page
                print new_url
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)
            import urllib
            
            html = net.http_GET(new_url).content
            #total_pages='7'
            '''
            if total_pages == '':
                r= 'title="Last Page - Results .+? to .+? of (.+?)">Last'
                total_pages = re.compile(r).findall(html)[0]
            '''           
            #self.AddInfo(list, indexer, 'latest2', url, type, str(page), total_pages)   
                
            for item in re.finditer(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src=".+?" alt="(.+?)(\([\d]{4}\))"',html,re.I):
                url='http://g2g.so/movies/'+item.group(1)
                print url
                url=url.split('&')[0]
                print url
                name=item.group(2)
                item_year=item.group(3).replace('(','').replace(')','')
                name = self.CleanTextForSearch(name)
                #url = net.http_GET(url).get_url()
                #print url
                self.AddContent(list,indexer,common.mode_File_Hosts,name+' ('+item_year+')','',type, url=url, name=name, year=item_year)
                
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        name = (name).lower()
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        net.set_cookies(self.cookie_file)

        content = net.http_GET(url).content
        
        if type == 'tv_seasons':
            match=re.compile('<br><br><b>(.+?)x').findall(content)
            for seasonnumber in match:                
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=url, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':
            match=re.compile("<br><b>"+season+"x(.+?)\s-\s<a style=.+?color.+?\shref='/(.+?)'>(.+?)</a>").findall(content)
            for item_v_id_2,url,item_title  in match:
                season = "0%s"%season if len(season)<2 else season
                item_v_id_2 = "0%s"%item_v_id_2 if len(item_v_id_2)<2 else item_v_id_2
                item_url = self.base_url + url
                item_v_id_2 = str(int(item_v_id_2))
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
                    
       
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'latest','Latest Movies','http://g2g.so/forum/forumdisplay.php?4-Movies&sort=lastpost&order=desc',indexer)
                self.AddSection(list, indexer,'latest','Number of Views','http://g2g.so/forum/forumdisplay.php?4-Movies&s=&pp=25&daysprune=-1&sort=views&order=desc',indexer)
                self.AddSection(list, indexer,'latest','Thread Rating','http://g2g.so/forum/forumdisplay.php?4-Movies&s=&pp=25&daysprune=-1&sort=voteavg&order=desc',indexer)
                self.AddSection(list, indexer,'latest','ABC','http://g2g.so/forum/forumdisplay.php?4-Movies&sort=title&order=asc',indexer)
                self.AddSection(list, indexer,'genre','Genere','http://g2g.so/movies/genre.php?showC=27',indexer)         
                           
            elif section == 'genre':
                r = re.findall(r'<!--- <a href=".+?" target="_self"> ---><a href="(.+?)" target="_self"><img class="image" src="http://g2g.so/uploads/thumbnails/(.+?)-G2G.so.jpg"', net.http_GET(url).content, re.I)
                for url,genres in r[0:]:
                    genres_title = genres.upper()
                    url='http://g2g.so/movies/'+url
                    url=url.split('&')[0]
                    self.AddSection(list, indexer, 'genres_title', genres_title, url, indexer)              

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

        elif indexer == common.indxr_TV_Shows:
            
            if section == 'main':
                self.AddSection(list, indexer,'tvshows','TV Shows (Coming soon)','http://g2g.so/tvseries/',indexer)
                self.AddSection(list, indexer,'tvshowslatest','Latest Episodes','http://g2g.so/episodes/',indexer)

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

            
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re
        from entertainment.net import Net
        net = Net()

        print url
        content = net.http_GET(url).content
        
        match=re.compile('class="movie_version_link"> <a href="(.+?)".+?document.writeln\(\'(.+?)\'\)',re.DOTALL).findall(content)
    
        for item_url ,HOST in match:
            self.AddFileHost(list, 'SD', item_url,host=HOST.upper())       
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        #net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        net = Net()        
               
        if type == 'movies':
            


            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            URL= self.base_url+'?type=movie&keywords=%s' %name.replace(' ','+')
            content = net.http_GET(URL).content
            
            match =re.compile('href="(.+?)" target="_blank"><img class="image" src=".+?" alt="(.+?)"').findall(content)
            for item_url , name in match:
                if year in name:
                    print item_url
                    self.GetFileHosts(item_url, list, lock, message_queue)

        '''elif type == 'tv_episodes':
            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            URL= self.base_url+'?type=tv&keywords=%s' %name.replace(' ','+')
            content = net.http_GET(URL).content
            
            match =re.compile('href="(.+?)" target="_blank"><img class="image" src=".+?" alt="(.+?)"').findall(content)

            for url , name in match:
                if year in name:

                    link = net.http_GET(url).content
                    match1=re.compile('<a href="(.+?)">(.+?)<').findall(link)

                    for item_url, episodes in match1:
  
                        if 'season-%s'%season in item_url:
                            if 'E%s'%episode in episodes:
                                print item_url
                                self.GetFileHosts(item_url, list, lock, message_queue)'''
                        
            

    def Resolve(self, url):
        from entertainment.net import Net
        import re
  
        net = Net()                
        import base64
        content = net.http_GET(url).content
        URL=base64.b64decode(re.compile('external/.+?/(.+?)"').findall(content)[0])
        print '###############################'
        print URL
        from entertainment import istream
        play_url = istream.ResolveUrl(URL)
        print play_url
        return play_url
            
            
        

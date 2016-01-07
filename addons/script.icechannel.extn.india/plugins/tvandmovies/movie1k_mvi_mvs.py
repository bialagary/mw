'''
    Istream
    Movie1k
    Copyright (C) 2013 Xuintytalk

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common

#from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import MovieIndexer
#from entertainment.plugnplay.interfaces import TVShowIndexer

class movie1k(MovieIndexer,MovieSource):#,TVShowIndexer, TVShowSource
    implements = [MovieIndexer,MovieSource]#,TVShowIndexer, TVShowSource
	
    #unique name of the source
    name = "movie1k"
    source_enabled_by_default = 'false'
    default_indexer_enabled = 'false'
    #display name of the source
    display_name = "Movie1k"
    
    #base url of the source website
    base_url = 'http://www.movie1k.ag'

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        if section == 'category/hollywood-movies':
            new_url = url
            print new_url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('alt="Watch .+?: (.+?)\(([\d]{4})\) .+?<a href="(.+?)" rel="bookmark">.+?</a></h3>').findall(html)
            for name,year,url in match:
                print url
                print name
                print year
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)

        elif section == 'category/hindi-movies':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('alt="Watch .+?: (.+?)\(([\d]{4})\) .+?<a href="(.+?)" rel="bookmark">.+?</a></h3>').findall(html)
            for name,year,url in match:
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)

        elif section == 'category/hindi-dubbed-movies':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('alt="Watch .+?: (.+?)\(([\d]{4})\) .+?<a href="(.+?)" rel="bookmark">.+?</a></h3>').findall(html)
            for name,year,url in match:
                #name=name.split('(')[0]
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)

        elif section == 'tag/box':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('alt="Watch .+?: (.+?)\(([\d]{4})\) .+?<a href="(.+?)" rel="bookmark">.+?</a></h3>').findall(html)
            for name,year,url in match:
                #name=name.split('(')[0]
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)

        elif section == 'category/tv-show':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('<h3 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?) Season (.+?) Episode (.+?)</a></h3>').findall(html)
            for url,name,Sea_num,eps_num in match:
                name = self.CleanTextForSearch(name)
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name+'[COLOR royalblue] ('+sea_eps+')[/COLOR]', 
                    item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)

        else:
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url+'page/'+page+'/'

            
            from entertainment.net import Net
            
            net = Net()
            import urllib #/tag/action/page/2/
            import re
            url = urllib.unquote_plus(url)
            new_url = self.base_url+'/tag/'+section+'/'
            
            html = net.http_GET(new_url+'page/'+str(page)+'/').content
            if total_pages == '':
                r= '<ul><li class="page_info">Page 1 of (.+?)</li><li class="active_page">'
                total_pages = re.compile(r).findall(html)[0]
                
            self.AddInfo(list, indexer, section, '', type, str(page), total_pages)

            match=re.compile('alt="Watch .+?: (.+?)\(([\d]{4})\) .+?<a href="(.+?)" rel="bookmark">.+?</a></h3>').findall(html)
            for name,year,url in match:
                #name=name.split('(')[0]
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)
           
            
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()
        url_type = ''
        content_type = ''

        if indexer == common.indxr_Movies:
            if section == 'main':
                #self.AddSection(list, indexer,'lastest','Latest Released Post',self.base_url,indexer)
                self.AddSection(list, indexer,'tag/box','Box Office Most Popular Movies',self.base_url+'/tag/box/',indexer)
                self.AddSection(list, indexer,'category/hollywood-movies','Hollywood Movies',self.base_url+'/category/hollywood-movies/',indexer)
                self.AddSection(list, indexer,'category/hindi-movies','Hindi Movies',self.base_url+'/category/hindi-movies/',indexer)
                self.AddSection(list, indexer,'category/hindi-dubbed-movies','Hindi Dubbed Movies',self.base_url+'/category/hindi-dubbed-movies/',indexer)
                self.AddSection(list, indexer,'genres','Genres',self.base_url,indexer)

            elif section == 'genres':
                r = re.findall(r'<strong><em><a href="/tag/(.+?)/">.+?</a></em></strong><br />', net.http_GET(url).content, re.I)
                for genres in r[0:]:
                    genres_title = genres.upper()
                    genres_title = genres_title.replace('-',' ')
                    genres_title = genres_title.replace('BOX','BOX OFFICE MOVIES')
                    self.AddSection(list, indexer, genres, genres_title, self.base_url+'/tag/'+genres+'/', indexer)

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

        elif indexer == common.indxr_TV_Shows:
            if section == 'main':
                self.AddSection(list, indexer,'category/tv-show','TV-Shows List',self.base_url +'/category/tv-show/',indexer)

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)            

    


    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        import urllib2
        from entertainment.net import Net
        net = Net()
        print url
        content = net.http_GET(url).content
        #print content
        #<td >(.+?)</td>\s*<td ><a href="(.+?)" target="_blank">Watch Full Movie</a>
        r = '<td >(.+?)</td>\s*<td.+?href="(.+?)" target="_blank">.+? Full Movie</a>'
        match  = re.compile(r).findall(content)

        for host,url in match:
            url=url.replace('http://www.movie1k.ag/watch.php?idl=','').replace('http://www.movie1k.ws/watch.php?idl=','')
            
            if 'embed' in url:
                
                if 'flashx' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.linkembed.net/flashx.php?vid=','')
                    url = 'http://play.flashx.tv/player/embed.php?hash=%s' % fileID                    

                elif 'nowvideo' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.linkembed.net/nowvideo.php?vid=','')
                    url = 'http://www.nowvideo.sx/video/%s' % fileID

                elif 'movshare' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.linkembed.net/movshare.php?vid=','')
                    url = 'http://www.movshare.php?vid=%s' % fileID

                elif 'novamov' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.linkembed.net/novamov.php?vid=60d48cc70e8a6','')
                    url = 'https://www.novamov.php/?vid=%s' % fileID

                elif 'videoweed' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.linkembed.net/videoweed.php?vid=','')
                    url = 'http://embed.videoweed.es/embed.php?v=%s' % fileID

                elif 'sockshare' in url:
                    fileID=url.replace('http://www.movie1k.ws/watch.php?idl=http://www.sockshare.com/embed/','')
                    url = 'http://www.sockshare.com/embed/%s' % fileID
                    
            
            self.AddFileHost(list, 'DVD', url, host=host.upper())
            
            
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        import urllib2
        import re
        from entertainment.net import Net
        net = Net()
                
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        #Movies = http://www.movie1k.ws/?s=Ice+Soldiers
        #TV Shows = http://www.movie1k.ag/watch-103452-arrow-season-2-episode-19/

        #season_pull = "%s"%season if len(season)<2 else season
        #episode_pull = "%s"%episode if len(episode)<2 else episode

        tv_url='http://www.movie1k.ws/?s=%s+Season+%s+Episode+%s' %(name.replace(' ','+'),season,episode)
        movie_url='http://www.movie1k.ws/?s=%s' %(name.replace(' ','+'))

        if type == 'movies':
            print movie_url
            html = net.http_GET(movie_url).content
            name_lower = common.CreateIdFromString(name)        
            for item in re.finditer(r'<a href="(.+?)" rel="bookmark">(.+?)</a>', html):
                item_url = item.group(1)
                item_year = item.group(2)
                #if item_year == year:
                self.GetFileHosts(item_url, list, lock, message_queue)
                    
            
        elif type == 'tv_episodes':
            print 'tv epiosdes##############################################################################'
            html = net.http_GET(tv_url).content
            name_lower = common.CreateIdFromString(name)        
            for item in re.finditer(r'<a href="(.+?)" rel="bookmark">.+? Season .+? Episode .+?</a>', html):
                item_url = item.group(1)
                print item_url
                print 'item_url'
                self.GetFileHosts(item_url, list, lock, message_queue)
                

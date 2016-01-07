'''
    anime ultima
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import TVShowSource
#from entertainment.plugnplay.interfaces import MovieIndexer
#from entertainment.plugnplay.interfaces import MovieSource

import re

class animeultima(TVShowIndexer,TVShowSource):
    implements = [TVShowIndexer,TVShowSource]
	
    #unique name of the source
    name = "animeultima"
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    #display name of the source
    display_name = "[COLOR blue]Anime[/COLOR][COLOR red]Ultima[/COLOR] "
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/8c081be69d176084e52cbe946bb6681ec617a84d/animeultima.png'
    #base url of the source website
    base_url = 'http://www.animeultima.io/'

    

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        if section == 'watch-anime':
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            match=re.compile('<li><a href="http:/\/\www.+?animeultima..+?/(.+?)" title=".+?">(.+?)</a></li>').findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'watch-live-action-anime':
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            match=re.compile('<a title=".+?" href="(.+?)">(.+?)</a>.+?<span class=".+?">.+?<').findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name in match:
                name = self.CleanTextForSearch(name)
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'ongoing anime':
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            match=re.compile('<a title=".+?" href="(.+?)">(.+?)</a>.+?<span class=".+?">.+?<').findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name in match:
                name = self.CleanTextForSearch(name)
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'topanime':
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            match=re.compile('<li><a href="(.+?)">(.+?)</a> <strong>').findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name in match:
                name = self.CleanTextForSearch(name)
                
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'hdfluffy':
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            up=re.compile('<a name="(.+?)" href="(.+?)"').findall(html)
            for name,url in up:
                name = self.CleanTextForSearch(name)
                #content2 = net.http_GET(url).content
                #match=re.compile('<a href="(.+?)" title="Watch .+?">').findall(content2)[0]
                item_id = common.CreateIdFromString(name)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, name, item_id, 'tv_seasons', url=url, name=name)

        if section == 'genres_title':
            #url = url.replace(' ','+')
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url +page+'/' #http://www.animeultima.io/genres/watch-action-animes/2/
            
            from entertainment.net import Net
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            html = net.http_GET(new_url+str(page)+'/').content

            if total_pages == '':
                r= '<a href="/genres/watch-.+?-animes/(.+?)/">.+?</a></div><div class="genre-anime">\s*<a href=".+?">\s*<span class="genre-anime-thumb"' 
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'genres_title', url, type, str(page), total_pages)
            
            match=re.compile('<div class="genre-anime">\s*<a href="/(.+?)">\s*<span class="genre-anime-thumb".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for url, name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)
         

        if section == 'abc_title':
            Alpha=[]
            new_url = url        
            from entertainment.net import Net        
            net = Net()
            import urllib
            url = urllib.unquote_plus(url)        
            html = net.http_GET(url).content
            
            letter = url.split('#')[1]
            letter = letter.replace('number','0-9')
            r= '<li><a href="(.+?)" title=".+?">(.+?)</a></li>'
            total_pages = re.compile(r).findall(html)

            for i in range(0,len(total_pages)):
                if total_pages[i][1][:1].isdigit() == True and letter == "0-9":
                        Alpha.append(total_pages[i])
                elif total_pages[i][1][:1] == letter:
                        Alpha.append(total_pages[i])
            for urls,name in Alpha:
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)
            
            
        
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
    
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        name = (name).lower()
        
        import re
        #tv_url= custom_url+'%s/index.html' %(name.lower().replace(' ','_'))
        
        new_url = url
               
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(new_url).content
        
        ''' Virtual Seasons Code Start '''
        num_episodes_per_virtual_season = 25
        ''' Virtual Seasons Code End '''
        
        if type == 'tv_seasons':

            item_url = new_url
            
            ''' Virtual Seasons Code Start '''
            
            match=re.compile('<td class="epnum">(.+?)</td><td class="title"><a href="(.+?)">(.+?)</a>').findall(content)
            
            total_episodes = len(match)
            total_seasons = total_episodes / num_episodes_per_virtual_season # ) + ( 1 if total_items % num_episodes_per_virtual_season >= 1 else 0) 
            
            for x in range( 0, total_seasons ):
                start_index = (x*num_episodes_per_virtual_season)
                item_title = "Episodes %04d - %04d" % (start_index+1, start_index+num_episodes_per_virtual_season)
                item_id = common.CreateIdFromString(title + ' ' + item_title)

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, season=str(x+1))
                
            if total_episodes % num_episodes_per_virtual_season >= 1:
                
                start_index = (total_seasons*num_episodes_per_virtual_season)
                item_title = "Episodes %04d - %04d" % (start_index+1, total_episodes)
                item_id = common.CreateIdFromString(title + ' ' + item_title)

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, season=str(total_seasons+1))
            
            ''' Virtual Seasons End '''
            
            
            
            
               
        elif type == 'tv_episodes':
        
            match=re.compile('<td class="epnum">(.+?)</td><td class="title"><a href="(.+?)">(.+?)</a>').findall(content)

            ''' Virtual Seasons Code Start '''
            
            start_index = ( int(season) - 1 ) * num_episodes_per_virtual_season
            match = match[ start_index : start_index + num_episodes_per_virtual_season  ]
            ''' Virtual Seasons Code Start '''
            
            for epnum,url,item_title  in match:
                epnum = epnum.split('-')[0]
                epnum = str(int(epnum))
                item_url = url
                season = str('1')
                item_id = common.CreateIdFromString(item_title + '_season_' + season + '_episode_' + epnum)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=epnum)
                
    

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net()
        url_type = ''
        content_type = ''

        
        if section == 'main':
            self.AddSection(list, indexer,'watch-anime','[COLOR blue]FULL [/COLOR][COLOR red]LISTING[/COLOR]',self.base_url+'watch-anime/',indexer)
            self.AddSection(list, indexer,'ongoing anime','[COLOR blue]ONGOING [/COLOR][COLOR red]ANIME[/COLOR]',self.base_url,indexer)
            self.AddSection(list, indexer,'A-Z','[COLOR blue]A-Z [/COLOR][COLOR red]LISTING[/COLOR]',self.base_url+'watch-anime/',indexer)
            self.AddSection(list, indexer,'watch-live-action-anime','[COLOR blue]ANIME [/COLOR][COLOR red]MOVIES[/COLOR]',self.base_url+'watch-anime-movies/',indexer)
            self.AddSection(list, indexer,'watch-live-action-anime','[COLOR blue]LIVE [/COLOR][COLOR red]ACTION[/COLOR]',self.base_url+'watch-live-action-anime/',indexer)
            self.AddSection(list, indexer,'topanime','[COLOR blue]TOP [/COLOR][COLOR red]ANIME[/COLOR]',self.base_url+'top-animes/',indexer)
            self.AddSection(list, indexer,'genres','[COLOR blue]GENRES[/COLOR]','http://www.animeultima.io/genres/',indexer)

        elif section == 'genres':
            r = re.findall(r'<a class="ctag" href="/genres/watch-(.+?)-animes/">.+?</a>', net.http_GET(url).content, re.I)
            for genres in r[0:]:
                genres_title = genres.upper()
                genres_title = genres_title.replace('-',' ')
                self.AddSection(list, indexer, 'genres_title', genres_title, self.base_url+'genres/watch-'+genres+'-animes/', indexer)

        
        elif section == 'A-Z':#<a href="#dot">.</a>
            r = re.findall(r'<a href="#.+?">(.+?)</a>', net.http_GET(url).content, re.I)
            for abc in r[0:]:
                abc_title = abc.upper()
                abc_title = abc_title.replace('DOT','.')
                abc_title = abc_title.replace('#','0-9')
                self.AddSection(list, indexer, 'abc_title', abc_title, self.base_url+'watch-anime/#'+abc.replace('#','number'), indexer)
            
            

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()
        
        content = net.http_GET(url).content
        r2 = '<iframe src="(.+?)".+?<strong>Video Site:</strong> (.+?)<br />'
        hostlink2  = re.compile(r2,re.DOTALL).findall(content)
        
        r = '<a rel="nofollow" href="(.+?)">.+?title="Trusted uploader" class="trusted" /></a></div>(.+?) video by <' 
        hostlink  = re.compile(r).findall(content)
       
        for url,host in hostlink + hostlink2:
            host = host.upper()
            if 'AUENGINE' in host:
                try:
                    import urllib
                    content2 = net.http_GET(url).content
                    Au=urllib.unquote(re.compile("url: '(.+?)'").findall(content2)[-1])
                    url = net.http_GET(Au, auto_read_response=False).get_url()
                except:pass

            '''
            if 'MP4UPLOAD' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    mp4upload=re.compile('<iframe title="MP4Upload" type="text/html" frameborder="0" scrolling="no" width=".+?" height=".+?" src="(.+?)">').findall(content)[0]
                    content2 = net.http_GET(mp4upload).content
                    mp4=re.compile("file: '(.+?)',").findall(content2)[0]
                    url = net.http_GET(mp4, auto_read_response=False).get_url()
                except:pass

            if 'NOVAMOV' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    nova="http://www.novamov.com/video/%s"%re.compile('<div class="player-embed" id="pembed".+?iframe src="http://embed.+?novamov.+?com/embed.+?v=(.+?)&.+?" frameborder="0"').findall(content)[0]
                    content2 = net.http_GET(nova).content
                    key=re.compile('flashvars.filekey="(.+?)"').findall(str(content2))[0].replace('.','%2e').replace('-','%2d')
                    content3 = net.http_GET('http://www.novamov.com/api/player.api.php?pass=undefined&codes=1&user=undefined&file=%s&key=%s'%(nova.replace('http://www.novamov.com/video/',''),key)).content
                    vid=re.compile('url=(.+?)&title').findall(content3)[0]
                    url = net.http_GET(vid, auto_read_response=False).get_url()
                except:pass

            if 'VIDEOWEED' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    videoweed="http://www.videoweed.es/file/%s"%re.compile('<div class="player-embed" id="pembed".+?iframe src="http://embed.+?videoweed.+?com/embed.+?v=(.+?)&.+?" frameborder="0"').findall(net().http_GET(url).content)[0]
                    content2 = net.http_GET(videoweed).content
                    key=re.compile('flashvars.filekey="(.+?)"').findall(str(content2))[0].replace('.','%2e').replace('-','%2d')
                    content3 = net.http_GET('http://www.videoweed.es/api/player.api.php?pass=undefined&codes=1&user=undefined&file=%s&key=%s'%(videoweed.replace('http://www.videoweed.es/file/',''),key)).content
                    vid=re.compile('url=(.+?)&title').findall(content3)[0]
                    url = net.http_GET(vid, auto_read_response=False).get_url()
                except:pass

            if 'DAILYMOTION' in host:
                try:
                    import urllib
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    daily=re.compile('<div class="player-embed" id="pembed"><embed src="(.+?)" type="application/x-shockwave-flash"').findall(content)[0]
                    #redirect = urllib.unquote(net.http_GET(net.http_GET(daily).get_url().replace('swf/','')).content)
                    #dail = urllib.unquote(re.compile('"video_url":"(.+?)"',re.DOTALL).findall(redirect)[0])
                    url = net.http_GET(daily, auto_read_response=False).get_url()
                except:pass

            if 'YOURUPLOAD' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    yu=re.compile('<iframe title="YourUpload" type="text/html" frameborder="0" scrolling="no" width="650" height="370" src="(.+?)">').findall(content)[0]
                    data2 = net.http_GET(yu).content
                    yupload=re.compile('var video =\s*{file: "(.+?)"').findall(data2)[0]
                    url = net.http_GET(yupload, auto_read_response=False).get_url()
                except:pass

            if 'UPLOADC' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    uploadc=re.compile('<iframe src="(.+?)" frameborder="0"',re.DOTALL).findall(content)[0]
                    content2 = net.http_GET(uploadc).content
                    c = re.compile("'file','(.+?)'",re.DOTALL).findall(content2)[0]
                    url = net.http_GET(c, auto_read_response=False).get_url()
                except:pass

            if 'VIDBOX' in host: #VIDBOX IS NOT WORKING
                try:            
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    box=re.compile('<iframe title="VidBox" type="text/html" frameborder="0" scrolling="no" width="650" height="370" src="(.+?)"').findall(content)[0]
                    content2 = net.http_GET(box).content
                    vidb=re.compile("url: '(.+?)'").findall(content2)[0]
                    url = net.http_GET(vidb, auto_read_response=False).get_url()
                except:pass

            if 'VEEVR' in host:
                try:
                    url = 'http://www.animeultima.io'+url
                    content = net.http_GET(url).content
                    veevr=re.compile('<div class="player-embed" id="pembed"><iframe src="(.+?)"').findall(content)[0]
                    url = net.http_GET(veevr, auto_read_response=False).get_url()
                except:pass
            '''
            if not 'AUENGINE' in host:
                url='http://www.animeultima.io' + url
                
                self.AddFileHost(list,'DVD', url, host+'.COM')
        
              
        
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        import urllib2
        import re
        from entertainment.net import Net
        net = Net()

        
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        
        #TV Shows = http://www.animeultima.io/search.html?searchquery=pokemon+xy+2013
        
        
        if type == 'tv_episodes':
            season_pull = "0%s"%season if len(season)<2 else season
            episode_pull = "%s"%episode if len(episode)<2 else episode

            tv_url=self.base_url+'search.html?searchquery=%s+%s' %(name.lower().replace(' ','+'),year)
            html = net.http_GET(tv_url).content
        
            r = '<ol id="searchresult"><li><h2><a href="(.+?)"><b>.+?</b> .+?</a>' 
            search_result  = re.compile(r).findall(html)[0]
            
            content2 = net.http_GET(search_result).content
            eps=re.compile('<td class="epnum">'+episode_pull+'</td><td class="title"><a href="(.+?)">.+?</a></td><td class=.+?</td><td class="td-lang-subbed">').findall(content2)
            for url in eps:
                tv_url=url
                self.GetFileHosts(tv_url, list, lock, message_queue)

    
    def Resolve(self,url):
        
        import re
        from entertainment.net import Net
        net = Net()
        html = net.http_GET(url).content
        if 'auengine' in url.lower():
            match=re.compile("file: '(.+?)'").findall(html)
            amount =len(match)-1
            return match [amount]

        if 'mp4upload' in url.lower():
            match=re.compile('http://mp4upload.com/embed(.+?)"').findall(html)[0]
            html = net.http_GET('http://mp4upload.com/embed'+match).content
            match=re.compile("'file': '(.+?)'").findall(html)
            amount =len(match)-1
            return match [amount]


            

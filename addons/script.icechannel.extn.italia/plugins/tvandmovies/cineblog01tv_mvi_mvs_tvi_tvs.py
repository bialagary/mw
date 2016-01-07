'''
    cineblog01.tv    
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui


class cineblog01tv(MovieIndexer,MovieSource,TVShowIndexer,TVShowSource):
    implements = [MovieIndexer,MovieSource,TVShowIndexer,TVShowSource]
    
    name = "CineBlog01.TV (Italia)"
    display_name = "CineBlog01.TV (Italia)"
    base_url = 'http://cineblog01.tv'
    tv_base_url = 'http://cineblog01.tv/serietv'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        from entertainment.net import Net
        import re
        
        if page == '':
            page = '1'
            
        base_url_for_match = self.base_url
        if indexer == common.indxr_TV_Shows:
            base_url_for_match = self.tv_base_url
            
        if url.startswith('%s/?' % base_url_for_match):
            new_url = url.replace('%s/?' % base_url_for_match, '%s/page/%s/?' % (base_url_for_match, page) )
        else:
            if not url.endswith('/'):                
                new_url = url + '/page/' + page
            else:
                new_url = url + 'page/' + page
        
        net = Net()
        
        content = net.http_GET(new_url).content
        
        if total_pages == '':
            page_count = re.search('<li class=[\'"]page_info[\'"]>Pagina 1 di ([0-9]+)</li>', content)
            if page_count: total_pages = page_count.group(1)
            else: total_pages = 1
            
        self.AddInfo(list, indexer, section, url, type, str(page), str(total_pages) )

        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        for movie in re.finditer('(?s)<div id=[\'"]item[\'"]>.+?<div id=[\'"]covershot[\'"]><a href=[\'"](.+?)[\'"].+?<img.+?src=[\'"](.+?)[\'"]>.+?<h3>(.+?)</h3>.+?<div id=[\'"]description[\'"]><p>(.+?)</p>', content):
            movie_url =  movie.group(1)
            movie_img = movie.group(2).replace(' ', '%20')
            movie_title = movie.group(3)
            movie_year = re.search("\(([0-9]+)\)$", movie_title)
            if movie_year:
                movie_year = movie_year.group(1)
                movie_name = re.sub("\(([0-9]+)\)$", "", movie_title)
            else:
                movie_year = ''
                movie_name = movie_title
            movie_description = movie.group(4).replace('&nbsp;', '').replace('&#160;', '')
            self.AddContent(list, indexer, mode, movie_title, '',type, url=movie_url, name=movie_name, year=movie_year, img=movie_img, plot=movie_description) 
        
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(url).content.replace('&#215;', ' ').replace('&#8211;', '-') 
        content = common.CleanText(content, True, True)
        
        import re
        if type == 'tv_seasons':
            season_list = []
            for item in re.finditer('([0-9]+) [0-9]+ .+?<(?:br|/p)', content):
                season_num = item.group(1)
                if season_num not in season_list:
                    
                    season_list.append(season_num)
                    item_title = 'Season ' + season_num
                    item_id = common.CreateIdFromString(title + ' ' + item_title)
                    self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=url, name=name, year=year, season=season_num)
                    
        elif type == 'tv_episodes':
            for item in re.finditer( season + ' ([0-9]+) (.*)', content):
                item_v_id = item.group(1)
                item_title = item.group(2).split(' - ')[0]
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=url+'|||||'+season+'|||||'+item_v_id, name=name, year=year, season=season, episode=item_v_id)
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        import re
        
        net = Net()
        
        base_url_for_match = self.base_url
        if indexer == common.indxr_TV_Shows:
            base_url_for_match = self.tv_base_url
            

        if section == 'main':
            if indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, 'serie-tv-home', 'Serie-Tv Home', base_url_for_match, indexer)
            else:
                self.AddSection(list, indexer, 'film-home', 'Film Home', base_url_for_match, indexer)
            content = net.http_GET(base_url_for_match).content
            for menu_item in re.finditer('(?s)<select name=[\'"]select(.+?)</select>', content):
                menu_item_title = re.search( '<option.+?>(.+?)</option>', menu_item.group(1) ).group(1)
                self.AddSection(list, indexer, common.CreateIdFromString(menu_item_title), menu_item_title, base_url_for_match, indexer)
        elif url == base_url_for_match and section not in ('serie-tv-home', 'film-home'):
            content = net.http_GET(url).content
            for menu_item in re.finditer('(?s)<select name=[\'"]select(.+?)</select>', content):
                is_item_menu_title = True
                for menu_sub_item in re.finditer( '<option value=[\'"](.*)[\'"]>(.+?)</option>', menu_item.group(1) ):
                    menu_item_title = menu_sub_item.group(2)
                    if is_item_menu_title == True:
                        menu_item_title_id = common.CreateIdFromString(menu_item_title)
                        if menu_item_title_id != section:
                            break
                        is_item_menu_title = False
                        continue                            
                    self.AddSection(list, indexer, common.CreateIdFromString(menu_item_title), menu_item_title, self.base_url + menu_sub_item.group(1), indexer)
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re
        from entertainment.net import Net
        net = Net()

        url_splits = url.split('|||||')
        url = url_splits[0]
        content = net.http_GET(url).content.replace('&#215;', ' ').replace('&#8211;', '-')         
        content = common.CleanText(content, True, True)
        
        if '>HOME-SERIE-TV<' in content:
            links = re.search(url_splits[1] + ' ' + url_splits[2] + ' (.*)' , content)
            if links:
                for link in re.finditer('<a.+?href=[\'"](.+?)[\'"][^>]*>(.+?)<', links.group(1)):
                    self.AddFileHost(list, 'NA', link.group(1) + '|||||' + url, re.sub('<.+?>', '', link.group(2)).upper() )
        else:
            links = re.search('(?s)<td valign=[\'"]top[\'"]>(.+?)<td valign=[\'"]bottom[\'"]>', content)
            if links:
                links = links.group(1)
                for link in re.finditer('<a href=[\'"](.+?)[\'"].+?>(.+?)</a>', links):
                    link_url = link.group(1)
                    if 'link_non_disponibili' in link_url: continue
                    self.AddFileHost(list, 'NA', link_url + '|||||' + url, host=link.group(2).upper())
                    
            for link in re.finditer('<div data\-counter.+?src[=\'"]{1,2}(.+?)[\'">]', content):
                link_url = link.group(1)
                self.AddFileHost(list, 'NA', link_url + '|||||' + url )
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net()
        
        import urllib
        
        if type == 'tv_episodes':
            search_title = self.CleanTextForSearch(name).lower().strip()
            episode = '%02d' % int(episode)
        else:
            search_title = self.CleanTextForSearch(title).lower().strip()            
        
        base_url_for_match = self.base_url
        if type == 'tv_episodes':
            base_url_for_match = self.tv_base_url
        
        search_url ='%s/?s=%s' %(base_url_for_match, urllib.quote_plus(search_title))
        
        content = net.http_GET(search_url).content
        
        if 'Nessun Film risponde ai criteri di ricerca impostati' in content:
            return
            
        keywords_lower = name.lower().split(' ')
        match_total = float( len(keywords_lower) )
        
        postfix_url = ''
        if type == 'tv_episodes':
            postfix_url = '|||||' + season + '|||||' + episode
        
        for movie in re.finditer('(?s)<div id=[\'"]item[\'"]>.+?<div id=[\'"]covershot[\'"]><a href=[\'"](.+?)[\'"].+?<img src=[\'"](.+?)[\'"]>.+?<h3>(.+?)</h3>.+?<div id=[\'"]description[\'"]><p>(.+?)</p>', content):
            movie_url = None
            movie_title = movie.group(3)

            movie_year = re.search("\(([0-9]+)\)$", movie_title)
            if movie_year:
                movie_year = movie_year.group(1)
                movie_name = re.sub("\(([0-9]+)\)$", "", movie_title)
            else:
                movie_year = ''
                movie_name = movie_title                
            movie_name_lower = movie_name.lower()
            
            match_count = 0
            for kw in keywords_lower:
                if kw in movie_name_lower:
                    match_count = match_count + 1
                
            if match_count >= match_total:
                if movie_year and len(movie_year) > 0 and year and len(year) > 0:
                    if  movie_year == year:
                        movie_url =  movie.group(1)
                else:    
                    movie_url =  movie.group(1)
                
            if movie_url:
                self.GetFileHosts(movie_url + postfix_url, list, lock, message_queue)
                break
            
                    
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        if page and len(str(page)) > 0 and total_pages and len(str(total_pages)) > 0 and int(page) > int(total_pages):
            return
        
        if page=='': page='1'
        
        from entertainment.net import Net
        net = Net()
        
        base_url_for_match = self.base_url
        if indexer == common.indxr_TV_Shows:
            base_url_for_match = self.tv_base_url
            
        search_url ='%s/page/%s/?s=%s' %(base_url_for_match, page, keywords.replace(' ','+'))

        import re
        
        content = net.http_GET(search_url).content
        
        if 'Nessun Film risponde ai criteri di ricerca impostati' in content:
            return
        
        if total_pages == '':
            page_count = re.search('<li class=[\'"]page_info[\'"]>Pagina 1 di ([0-9]+)</li>', content)
            if page_count: total_pages = page_count.group(1)
            else: total_pages = 1
            
        self.AddInfo(list, indexer, 'search', self.base_url, type, str(page), str(total_pages))
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        for movie in re.finditer('(?s)<div id=[\'"]item[\'"]>.+?<div id=[\'"]covershot[\'"]><a href=[\'"](.+?)[\'"].+?<img src=[\'"](.+?)[\'"]>.+?<h3>(.+?)</h3>.+?<div id=[\'"]description[\'"]><p>(.+?)</p>', content):
            movie_url =  movie.group(1)
            movie_img = movie.group(2).replace(' ', '%20')
            movie_title = movie.group(3)
            movie_year = re.search("\(([0-9]+)\)$", movie_title)
            if movie_year:
                movie_year = movie_year.group(1)
                movie_name = re.sub("\(([0-9]+)\)$", "", movie_title)
            else:
                movie_year = ''
                movie_name = movie_title
            movie_description = movie.group(4).replace('&nbsp;', '').replace('&#160;', '')
            self.AddContent(list,indexer,mode,movie_title,'',type, url=movie_url, name=movie_name, year=movie_year, img=movie_img, plot=movie_description) 

    def Resolve(self, url):
        url_splits = url.split('|||||')
        url = url_splits[0]
        refurl = url_splits[1]
        from entertainment.net import Net
        net = Net()
        if url.startswith('http://cineblog01'):
            html = net.http_GET(url, headers={'Referer':refurl}).content

            import re
            link = re.search('<meta http\-equiv=[\'"]refresh[\'"].+?url=(.+?)[\'"] />', html)            
            if link:
                url = link.group(1)
            else:
                link = re.search('window.location.href = [\'"](.+?)[\'"]', html)
                if link:
                    url = link.group(1)
                
        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url
        

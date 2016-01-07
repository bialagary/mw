'''
    Istream
    Project Free TV
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
import re

class projectfreetv(TVShowIndexer, TVShowSource,CustomSettings):
    implements = [TVShowIndexer, TVShowSource,CustomSettings]
	
    #unique name of the source
    name = "projectfreetv"
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    #display name of the source
    display_name = "Project Free TV"

    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/1120740c0028d16de328516e4f0c889aa949b65e/pojectfreetv.png'
    
    #base url of the source website
    base_url_tv = 'http://www.free-tv-video-online.me/internet/'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_url" type="labelenum" label="URL" default="http://www.free-tv-video-online.me/" values="Custom|http://www.free-tv-video-online.me/|http://pftv.uncensor.co.uk/" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    def get_url(self):
        custom_url = self.Settings().get_setting('custom_url')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            custom_url = ('http://' + custom_url)
        if not custom_url.endswith('/'):
            custom_url += '/'
        if not custom_url.endswith('internet/'):
            custom_url += 'internet/'
        return custom_url

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        custom_url = self.get_url()
        new_url = url
        
        from entertainment.net import Net
        
        net = Net()
        import urllib
        url = urllib.unquote_plus(url)
        
        html = net.http_GET(url).content
        #new_url = self.base_url+section+'/'
        
        if section == 'index_last':
            match=re.compile('<a href="(.+?)"><b>(.+?) - Season .+? Episode .+? <').findall(html)
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url_tv+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'index_last_3_days':
            match=re.compile('<a href="(.+?)"><b>(.+?) - Season .+? Episode .+? <').findall(html)
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url_tv+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'index_last_7_days':
            match=re.compile('<a href="(.+?)"><b>(.+?) - Season .+? Episode .+? <').findall(html)
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url_tv+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'index_last_30_days':
            match=re.compile('<a href="(.+?)"><b>(.+?) - Season .+? Episode .+? <').findall(html)
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url_tv+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        if section == 'index_last_365_days':
            match=re.compile('<a href="(.+?)"><b>(.+?) - Season .+? Episode .+? <').findall(html)
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url_tv+url
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        else:
            r = re.search('<a name="%s">(.+?)(<a name=|</table>)' % section, html, re.DOTALL)
            if r:
                match = re.compile('class="mnlcategorylist"><a href="(.+?)"><b>(.+?)</b></a>').findall(r.group(1))
                for url,name in match:
                    name = self.CleanTextForSearch(name)
                    url = self.base_url_tv+url
                    self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        
            
  
        
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        custom_url = self.get_url()
        #custom_url = self.get_url()
        name = (name).lower()
        
        import re
        tv_url= custom_url+'%s/index.html' %(name.lower().replace(' ','_'))
        
        new_url = url
               
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(tv_url).content
        
        if type == 'tv_seasons':
            match=re.compile('<td width="99%" class="mnlcategorylist"><a href="(.+?)"><b>Season (.+?)</b></a>').findall(content)
            for url, seasonnumber in match:                
                item_url = custom_url+'%s/' %(name.lower().replace(' ','_'))
                item_url1 = item_url+url
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url1, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':
            tv_url2=custom_url+'%s/season_%s.html' %(name.lower().replace(' ','_'),season)
            from entertainment.net import Net
            net = Net()
            content2 = net.http_GET(tv_url2).content
            match=re.compile('<td class="episode"><a name=".+?"></a><b>.+?. (.+?)</b></td>\s*<td class="mnllinklist" align="right"><div class="right">S.+?E(.+?)&').findall(content2)
            for item_title, item_v_id_2  in match:
                item_v_id_2 = str(int(item_v_id_2))
                item_url = tv_url2 + '?episode=' + item_v_id_2
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
            
    

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net()
        custom_url = self.get_url()
        url_type = ''
        content_type = ''

        
        if section == 'main':
            self.AddSection(list, indexer,'index_last','Last 24 Hours',custom_url+'index_last.html',indexer)
            self.AddSection(list, indexer,'index_last_3_days','Last 3 Days',custom_url+'index_last_3_days.html',indexer)
            self.AddSection(list, indexer,'index_last_7_days','Last 7 Days',custom_url+'index_last_7_days.html',indexer)
            self.AddSection(list, indexer,'index_last_30_days','This Month',custom_url+'index_last_30_days.html',indexer)
            self.AddSection(list, indexer,'index_last_365_days','Last 90 Days',custom_url+'index_last_365_days.html',indexer)
            #self.AddSection(list, indexer,'NewSeason','New Season',self.base_url_tv+'browse/NewSeason/',indexer)
            #self.AddSection(list, indexer,'Genres','Genres',self.base_url_tv+'browse',indexer)
            self.AddSection(list, indexer,'az','A-Z',custom_url,indexer)

        elif section == 'tvschedule':
            self.AddSection(list, indexer,'latest','Yesterday',custom_url+'/tvschedule/-1',indexer)
            self.AddSection(list, indexer,'latest','Today',custom_url+'/tvschedule/1',indexer)
            self.AddSection(list, indexer,'latest','Tomorrow',custom_url+'/tvschedule/2',indexer)

        

        elif section == 'az':
            self.AddSection(list, indexer,'#','0-9',custom_url +'##',indexer)
            self.AddSection(list, indexer,'A','A',custom_url +'#A',indexer)
            self.AddSection(list, indexer,'B','B',custom_url +'#B',indexer)
            self.AddSection(list, indexer,'C','C',custom_url +'#C',indexer)
            self.AddSection(list, indexer,'D','D',custom_url +'#D',indexer)
            self.AddSection(list, indexer,'E','E',custom_url +'#E',indexer)
            self.AddSection(list, indexer,'F','F',custom_url +'#F',indexer)
            self.AddSection(list, indexer,'G','G',custom_url +'#G',indexer)
            self.AddSection(list, indexer,'H','H',custom_url +'#H',indexer)
            self.AddSection(list, indexer,'I','I',custom_url +'#I',indexer)
            self.AddSection(list, indexer,'J','J',custom_url +'#J',indexer)
            self.AddSection(list, indexer,'K','K',custom_url +'#K',indexer)
            self.AddSection(list, indexer,'L','L',custom_url +'#L',indexer)
            self.AddSection(list, indexer,'M','M',custom_url +'#M',indexer)
            self.AddSection(list, indexer,'N','N',custom_url +'#N',indexer)
            self.AddSection(list, indexer,'O','O',custom_url +'#O',indexer)
            self.AddSection(list, indexer,'P','P',custom_url +'#P',indexer)
            self.AddSection(list, indexer,'Q','Q',custom_url +'#Q',indexer)
            self.AddSection(list, indexer,'R','R',custom_url +'#R',indexer)
            self.AddSection(list, indexer,'S','S',custom_url +'#S',indexer)
            self.AddSection(list, indexer,'T','T',custom_url +'#T',indexer)
            self.AddSection(list, indexer,'U','U',custom_url +'#U',indexer)
            self.AddSection(list, indexer,'V','V',custom_url +'#V',indexer)
            self.AddSection(list, indexer,'W','W',custom_url +'#U',indexer)
            self.AddSection(list, indexer,'X','X',custom_url +'#X',indexer)
            self.AddSection(list, indexer,'Y','Y',custom_url +'#Y',indexer)
            self.AddSection(list, indexer,'Z','Z',custom_url +'#Z',indexer)
            
            

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net()
        custom_url = self.get_url()
        episode = re.search('\?episode=(.*)', url).group(1)
        url = re.sub('\?.*', '', url)

        content = net.http_GET(url).content#<a onclick='visited(1980258)' href="http://www.free-tv-video-online.me/player/novamov.php?id=uauyj7jxjsw83" target="_blank">
        r = '<a onclick=.+? href="(.+?)" target="_blank">\s*<div>.+?Episode '+episode+'</div>\s*<span>\s*Loading.*<br/>\s*.+?Host: (.+?)<br/>' 
        match  = re.compile(r).findall(content)

        
        for url,host in match:            
            self.AddFileHost(list, 'SD', url, host=host.upper())


    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        custom_url = self.get_url()
        
        import urllib2
        import re
        from entertainment.net import Net
        net = Net()

        search_term = name
        category = ''
        if type == 'tv_episodes':
            category = 'category=4'
        elif type == 'movies':
            category = 'category=5'
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        #Movies = http://oneclickwatch.org/?s=Escape+Plan+2013
        #TV Shows = http://www.free-tv-video-online.me/search/?q=2%20broke%20Girls&md=all
        #tv shows = http://www.free-tv-video-online.me/internet/%s/season_%s.html
        
        if type == 'tv_episodes':
            season_pull = "%s"%season if len(season)<2 else season
            episode_pull = "%s"%episode if len(episode)<2 else episode

            tv_url=custom_url+'%s/season_%s.html?episode=%s' %(name.lower().replace(' ','_'),season_pull,episode_pull)
            
            self.GetFileHosts(tv_url, list, lock, message_queue)

                    
    def Resolve(self, url):
        custom_url = self.get_url()
        if 'http' in url:
            #print url
            
            from entertainment.net import Net
            import re        
            net = Net()
            content = net.http_GET(url).content
            
            # get host from url
            host = re.search('/([A-Za-z0-9]+?)\.php', url).group(1)
            #print host
            
            id = re.search('\?id=(.*)', url).group(1)
            #print id
            
            # iframe source
            iframe_src = re.search('(?i)<iframe.+?src=[\'"](.+?' + id + '.+?)[\'" >]', content).group(1)
            #print iframe_src
            
            if iframe_src.endswith("'") or iframe_src.endswith('"'): iframe_src = iframe_src[:-1]
            if host.lower() in iframe_src.lower():
                final = iframe_src
            else:
                content = net.http_GET(iframe_src).content
                final = re.search('(?i)<iframe.+?src=[\'"](.+?' + id + '.+?)[\'"]', content).group(1)
            
            #print final
            return TVShowSource.Resolve(self, final)
            
        return ''

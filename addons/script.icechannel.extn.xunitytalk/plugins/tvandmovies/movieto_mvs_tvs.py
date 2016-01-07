'''
    Istream
    Scenelog.org
    Copyright (C) 2013 Coolwave, Jas0npc, the-one, voinage

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource





class movieto(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
	
    #unique name of the source
    name = "movie.to"
    source_enabled_by_default = 'true'
    #display name of the source
    display_name = "MovieTo"
    
    #base url of the source website
    base_url = 'http://movietv.to/'

    
    def GetFileHosts(self, url, list, lock, message_queue,ref):

            self.AddFileHost(list, '720P', url+'|'+ref,host='MOVIE.TO')



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net

        net = Net(cached=False,user_agent='Magic Browser')
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)


        wait=False
        new_url='http://movietv.to/index/loadmovies'
        if type == 'tv_episodes':
            types='tv'
            r='href="/series/(.+?)".+?movie-title">(.+?)</h2>'
            NEW='http://movietv.to/series/'
        else:
            types='movie'
            r='href="/movies/(.+?)".+?movie-title">(.+?)</h2>'
            NEW='http://movietv.to/movies/'
            
        data={'loadmovies':'showData','page':'1','abc':'All','genres':'','sortby':'Popularity','quality':'All','type':types,'q':name}
        content=net.http_POST(new_url,data,headers={'Referer':'http://movietv.to'}).content
        
       
        match=re.compile(r,re.DOTALL).findall (content)
        print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        print match
        for URL , TITLE in match:
                print TITLE
                print URL
                if name.lower() in TITLE.lower():
                    if type == 'tv_episodes':
                        id=URL.split('-')[0]
                        LINKURL='http://movietv.to/series/getLink?id=%s&s=%s&e=%s' % (id,season,episode)
                        contents=net.http_GET(LINKURL).content
                        import json
                        match=json.loads(contents)['url']
                        

                    else:
                        
                        contents=net.http_GET(NEW+URL).content
                        
                        match=re.compile('<source src="(.+?)" type=\'video/mp4\'>').findall(contents)[0]
                    
                    self.GetFileHosts(match, list, lock, message_queue,URL)

                    

    def Resolve(self, url):
        import re
        import urllib
        
        ref=url.split('|')[1]
        url=url.split('|')[0]
        url=url.split('&end')[0]
        
        #cookie = match=re.compile('__cfduid=(.+?);').findall(open(self.cookie_file).read())[0]
        
        url += "|Referer=http://movietv.to/movies/"+ref
        return url.replace('\\','')
                                

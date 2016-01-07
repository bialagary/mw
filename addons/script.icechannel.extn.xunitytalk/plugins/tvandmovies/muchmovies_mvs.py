'''
    Ice Channel
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

class muchmovies(MovieSource):
    implements = [MovieSource]
    
    name = "MuchMovies"
    display_name = "Much Movies"
    base_url = 'http://umovies.me'
    
    source_enabled_by_default = 'true'
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    UA ='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5'
    
    
    def GetFileHosts(self, url, list, lock, message_queue):
        url=url.replace('umovies.me','muchmovies.org')
        self.AddFileHost(list, 'HD', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net


        
        net = Net(user_agent=self.UA)        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','-')+'-'+year
        
        import re
        url='http://umovies.me/search/'+search_term
        try:
            net.set_cookies(self.cookie_file)
            link = net.http_GET(url).content
            print '##########################'
            print 'NET'
            
        except:
            from entertainment import cloudflare            
            link = cloudflare.solve(url,self.cookie_file,self.UA)
 
        match = re.compile('lass="movies list inset">.+?href="(.+?)">.+?class="label">(.+?)<',re.DOTALL).findall(link)

        for movie_url, TITLE in match:
            if year in TITLE:
                self.GetFileHosts('http://umovies.me'+movie_url, list, lock, message_queue)
                
            
    def Resolve(self, url):
        
        import re        
        from entertainment.net import Net
        net = Net(user_agent=self.UA)
        url=url.replace('muchmovies.org','umovies.me')
        try:
            net.set_cookies(self.cookie_file)
            content = net.http_GET(url).content
            print '##########################'
            print 'NET'
        except:
            from entertainment import cloudflare
            content=cloudflare.solve(url,self.cookie_file,self.UA)
        content = content.replace('\n','')
        
        link=content.split('href=')
        for p in link:

            if '.mp4' in p:
                resolved_media_url = re.compile('"(.+?)"').findall(p)[0]
                host =resolved_media_url.split('//')[1]
                host = host.split('/')[0]
                cookie =open(self.cookie_file).read()
                __cfduid =re.compile('__cfduid=(.+?);').findall(cookie)[0]
                cf_clearance =re.compile('cf_clearance="(.+?)"').findall(cookie)[0]
                COOKIE = '__cfduid=%s; cf_clearance=%s' % (__cfduid,cf_clearance)

                resolved_media_url = resolved_media_url+'|User-Agent='+self.UA+'&Referrer='+url+'&host='+host+'&Cookie='+COOKIE
                print resolved_media_url
        return resolved_media_url
            
                
                

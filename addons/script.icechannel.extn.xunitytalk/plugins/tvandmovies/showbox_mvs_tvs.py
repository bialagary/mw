'''
       
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class showbox(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Showbox"
    display_name = "Showbox"
   
    source_enabled_by_default = 'true'    

    base_link = 'http://mobapps.cc'
    data_link = ['http://mobapps.cc/data/data_en.zip']

    moviedata_link = 'movies_lite.json'
    tvdata_link = 'tv_lite.json'
    movie_link = '/api/serials/get_movie_data/?id=%s'
    show_link = '/api/serials/es?id=%s'
    episode_link = '/api/serials/e/?h=%s&u=%01d&y=%01d'
    vk_link = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s'

    def get_movie(self, title,year):
     
        import zipfile, StringIO,json,urllib2,urlparse
        for datalink in self.data_link:
            data = urllib2.urlopen(datalink).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.moviedata_link)
            zip.close()

            result = json.loads(result)
            for field in result:
                id = field['id']
                name=field['title']
                years = field['year']
                if title.lower() in name.lower():
                    if year in years:
                        url = self.movie_link % id
                        url = url.encode('utf-8')
                        print url
                        return url

    def get_show(self,title,season,episode):
     
        import zipfile, StringIO,urllib2,json,urlparse
        for datalink in self.data_link:      
            data = urllib2.urlopen(datalink).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.tvdata_link)
            zip.close()

            result = json.loads(result)
            for field in result:
                id = field['id']
                name=field['title']
                if title.lower() in name.lower():

                    url = self.show_link % id
         
                    url = url.encode('utf-8')
           
                    return self.get_episode(url, season, episode)


    def get_episode(self, url, season, episode):
        if url == None: return
        url = url.rsplit('id=', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = url.encode('utf-8')
        return url


    def vk(self,url):

        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        url = url.replace('http://', 'https://')
        result = net.http_GET(url).content

        u = re.compile('url(720|540|480)=(.+?)&').findall(result)

        url = []
        try: url += [[{'quality': '720P', 'url': i[1]} for i in u if i[0] == '720'][0]]
        except: pass
        try: url += [[{'quality': 'HD', 'url': i[1]} for i in u if i[0] == '540'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '480'][0]]
        except: pass

        if url == []: return
        return url

        
    def GetFileHosts(self, url, list, lock, message_queue):

        import re,urlparse,json
        from entertainment.net import Net
        net = Net(cached=False,user_agent='android-async-http/1.4.1 (http://loopj.com/android-async-http)')

        
        url= self.base_link + url
        

        par = urlparse.parse_qs(urlparse.urlparse(url).query)
        try: num = int(par['h'][0]) + int(par['u'][0]) + int(par['y'][0])
        except: num = int(par['id'][0]) + 537
        
        result=net.http_GET(url).content
   
        result = json.loads(result)
        try: result = result['langs']
        except: pass
        i = [i for i in result if i['lang'] in ['en', '']][0]

        url = (str(int(i['apple']) + num), str(int(i['google']) + num), i['microsoft'])

        url = self.vk_link % url
        url = self.vk(url)
        for i in url:
            quality=i['quality']
            url= i['url']

      
            self.AddFileHost(list, quality, url,host='SHOWBOX')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
        name = self.CleanTextForSearch(name)
        import urllib


        if type == 'tv_episodes':
          item_url=self.get_show(name,season,episode)
        else:
          item_url =self.get_movie(name,year) 
        
        self.GetFileHosts(item_url, list, lock, message_queue)









            

'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

class cartoonhd(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Cartoon HD"
    display_name = "Cartoon HD"
    base_url = 'http://cartoonhd.mobi/'
   
    source_enabled_by_default = 'true'

    cookie_file = os.path.join(common.cookies_path, 'cartoonhd.cookie')            
    
    def GetFileHosts(self, url, list, lock, message_queue,type):

        import re,time,base64
        from entertainment.net import Net
        net = Net(cached=False)
     
        
       
        headers={'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'www.cartoonhd.mobi',
                'Origin':'http://www.cartoonhd.mobi',
                'Pragma':'no-cache',
                'Referer':'http://www.cartoonhd.mobi',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
                'X-Requested-With':'XMLHttpRequest'}

        cookie = net.http_GET('http://cartoonhd.mobi/index.php',headers=headers).content
        #cookie=net.get_cookies()
        #print cookie
        
        net.save_cookies(self.cookie_file)
        COOKIE=re.compile('__utmx="(.+?)"').findall(open(self.cookie_file).read())[0]
        #print COOKIE
        net.set_cookies(self.cookie_file)                         
                             
        content = net.http_GET(url,headers=headers).content
        
        TIME = time.time()- 3600
  
        TIME= str(TIME).split('.')[0]
  
        TIME= base64.b64encode(TIME,'strict')
 
        TIME=TIME.replace('==','%3D%3D')
        
        token=re.compile("var tok='(.+?)'").findall(content)[0]        
        match=re.compile('elid="(.+?)"').findall(content)
        id = match[0]
        #COOKIE='flixy=%s; %s=%s' % (token,id,TIME)

        headers={'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Length':'94',
                #'Cookie':COOKIE,
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'www.cartoonhd.mobi',
                'Origin':'http://www.cartoonhd.mobi',
                'Pragma':'no-cache',
                'Referer':url,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
                'X-Requested-With':'XMLHttpRequest',
                'Authorization': 'Bearer '+COOKIE.replace('%3D','=')}

        
        OPTION= re.compile('<option value="(.+?)" data-type="(.+?)">').findall(content)

        if type == 'tv_episodes':
            get='getEpisodeEmb'
        else:
            get='getMovieEmb'

        new_search='http://www.cartoonhd.mobi/ajax/embeds.php'

        data={'action':get,'idEl':id,'token':token,'elid':TIME}
   
        import requests
        content = requests.post(new_search, data=data, headers=headers).content
        #print content
        
        for option , server in OPTION:
            #print option
            #print server
            if '-' in server:
                quality= server.split('-')[1].strip().upper()
                name= server.split('-')[0].strip().upper()
                if '320P' in quality:
                    quality= 'SD'  
            else:
                quality= 'SD'
                name= server.upper()             

            r = '"%s".+?iframe src="(.+?)"' % option
            #print r
            FINAL_URL  = re.compile(r,re.IGNORECASE).findall(content.replace('\\',''))[0]
            
            if 'mail.ru' in FINAL_URL:
                matchme=re.compile('"metadataUrl":"(.+?)"').findall(net.http_GET(FINAL_URL).content)[0]
                quality,url=self.GrabMailRu(matchme,list)
    
            else:
            
                self.AddFileHost(list, quality, FINAL_URL.split('"')[0],host=name)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        

      name=name.lower()
      if type == 'tv_episodes':
        name=name.lower()
        item_url = 'http://cartoonhd.mobi/show/%s/season/%s/episode/%s' %(name.replace(' ','-'),season,episode)
    
      else:
        item_url = 'http://www.cartoonhd.mobi/full-movie/watch-%s-online-free' % (name.replace(' ','-'))
        
      self.GetFileHosts(item_url, list, lock, message_queue,type)
              

    def GrabMailRu(self,url,list):
        print url
        
        from entertainment.net import Net
        net = Net(cached=False)

        
        import json,re
        items = []

        data = net.http_GET(url).content
        cookie = net.get_cookies()
        for x in cookie:

             for y in cookie[x]:

                  for z in cookie[x][y]:
                       
                       l= (cookie[x][y][z])
                       
        r = '"key":"(.+?)","url":"(.+?)"'
   
        match = re.compile(r,re.DOTALL).findall(data)
        for quality,stream in match:
            test = str(l)
            test = test.replace('<Cookie ','')
            test = test.replace(' for .my.mail.ru/>','')
            url=stream +'|Cookie='+test
            Q=quality.upper()
            if Q == '1080P':
                Q ='1080P'
            elif Q == '720P':
                Q ='720P'                
            elif Q == '480P':
                Q ='HD'
            else:
                Q ='SD'                
            self.AddFileHost(list, Q, url,host='MAIL.RU') 

             

    def Resolve(self, url):                 
         
        if 'mail.ru' in url:
            resolved = url
        if 'mvsnap' in url:
            resolved =url            
        if 'googleusercontent.com' in url:
            import urllib
            page = urllib.urlopen(url)
            resolved=page.geturl()
            
        elif 'googlevideo.com' in url:
            resolved =url
        else:
        
            from entertainment import istream
            resolved =istream.ResolveUrl(url)
        return resolved    









            

'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc
import sys

class cartoonhdextra(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "CARTOONEXTRA"
    display_name = "CARTOONEXTRA"
    cartoon = xbmc.translatePath('special://home/userdata/addon_data/script.icechannel/databases/cartoon2')
    HEADERS={'User-Agent':'Apache-HttpClient/UNAVAILABLE (java 1.4)','Host':'gearscenter.com','Connection':'keep-alive'}
    source_enabled_by_default = 'true'
    DATAKEY='M2FiYWFkMjE2NDYzYjc0MQ=='
    FILMKEY = 'MmIyYTNkNTNkYzdiZjQyNw=='

    API='http://gearscenter.com/gold-server/gapiandroid205/?'
    
    def GetStream(self,url,key):
        from entertainment import pyaes as pyaes
        import base64

        key = base64.b64decode(key)
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
        url = base64.decodestring(url)
        url = decrypter.feed(url) + decrypter.feed()
        return str(url)

    def extra(self):
        import random
        import time
        import hashlib

        ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
        COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
        EXTRA_URL = ('&os=android&version=2.0.5&versioncode=205&param_1=F2EF57A9374977FD431ECAED984BA7A2&'
             'deviceid=%s&param_3=7326c76a03066b39e2a0b1dc235c351c&param_4=%s'
             '&param_5=%s&token=%s&time=%s&devicename=Google-Nexus-%s-%s')

        now = str(int(time.time()))
        build = random.choice(ANDROID_LEVELS.keys())
        device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
        country = random.choice(COUNTRIES)
        return EXTRA_URL % (device_id, country, country.lower(), hashlib.md5(now).hexdigest(), now, build, ANDROID_LEVELS[build])

    
        
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        import json
        from entertainment.net import Net
        net = Net(cached=False)

        CATID=url
  
        new_url = self.API+'option=content&id=%s' % url +self.extra()
        
        link = json.loads(net.http_GET(new_url,headers=self.HEADERS).content)

        if len(season)<2:
            season='0'+season
        if len(episode)<2:
            episode='0'+episode
          
        data=json.loads(self.GetStream(link['data'],self.DATAKEY))
        data=data['listvideos']
       
        if len(data)>1:
         
            for field in data:            
                name=field['film_name'].encode('utf8').upper()
                if type == 'tv_episodes':
                    if 'S%sE%s' % (season,episode) in name:
                        ID=str(field['film_id'])
                        self.TIDYME(list, CATID, ID)
                       
                else:
                    ID=str(field['film_id'])
                    self.TIDYME(list, CATID, ID)
        else:    

            for field in data:
                ID=str(field['film_id'])
                self.TIDYME(list, CATID, ID)
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import json
        from entertainment.net import Net
        net = Net(cached=False)
        
        new_url = self.API+'option=search&page=1&total=0&block=0&q=%s' % name.replace(' ','+') +self.extra()
        
        link = json.loads(net.http_GET(new_url,headers=self.HEADERS).content)
       
        data=json.loads(self.GetStream(link['data'],self.DATAKEY))

        for field in data['categories']:
            TITLE=field['catalog_name'].encode('utf8')
            action=str(field['catalog_id'])


            if name in TITLE:
                if not type == 'tv_episodes':
                    self.GetFileHosts(action, list, lock, message_queue,type,season,episode)
                else:    
                    if year in TITLE:
                        self.GetFileHosts(action, list, lock, message_queue,type,season,episode)

        
    def TIDYME(self,list, CATID, ID):
        import re,json
        from entertainment.net import Net
        net = Net(cached=False)
        new_url = self.API+'option=filmcontent&id=%s&cataid=%s' % (ID,CATID) +self.extra()
          
        link = json.loads(net.http_GET(new_url,headers=self.HEADERS).content)
        data=json.loads(self.GetStream(link['data'],self.DATAKEY))
        data=data['videos']

        for field in data:
            FILM = field['film_link']
            
            DATA=self.GetStream(FILM,self.FILMKEY)
            match=re.compile('(.+?)#(.+?)#').findall(DATA)               
            for FINAL_URL , quality in match:
                quality=quality+'P'
                self.AddFileHost(list, quality, FINAL_URL,host='GOOGLEVIDEO')         



    def Resolve(self, url):                 
        

        return url    









            

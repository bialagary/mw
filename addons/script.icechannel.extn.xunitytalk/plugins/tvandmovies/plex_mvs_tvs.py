'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common


class plex(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Plex"
    display_name = "Plex"
    source_enabled_by_default = 'false'

        
    servers   =['http://67.149.3.223:80',
                'http://64.121.99.133:32400',
                'http://74.131.52.183:32400',
                'http://209.95.51.98:32400',
                'http://208.109.209.222:32400',
                'http://73.220.90.64:32400',
                'http://173.164.3.18:32400',
                'http://64.233.212.55:32400',
                'http://174.75.32.26:32400',
                'http://99.150.246.18:32400',
                'http://96.2.12.103:32400',
                'http://67.61.56.229:32400',
                'http://162.229.232.134:32400',
                'http://96.44.147.109:32400',
                'http://67.183.13.152:32400',
                'http://198.72.233.76:8060',
                'http://162.253.180.90:32400',
                'http://68.191.144.25:32400',
                'http://98.202.250.91:32400',
                'http://96.44.146.4:32400',
                'http://24.127.179.16:32400',
                'http://50.183.14.93:32400',
                'http://24.21.124.179:32400',
                'http://96.28.110.128:32400',
                'http://50.162.155.164:32400',
                'http://98.248.19.71:32400',
                'http://104.190.156.162:32400',
                'http://174.34.240.5:32400',
                'http://24.49.43.216:32400',
                'http://67.165.142.35:32400',
                'http://173.79.20.141:32400',
                'http://73.13.38.192:32400',
                'http://64.88.195.24:32400',
                'http://66.254.113.103:32400',
                'http://173.8.91.59:32400',
                'http://64.130.117.2:32400',
                'http://24.160.179.15:32400',
                'http://50.16.67.34:32400',
                'http://74.141.135.17:32400',
                'http://174.52.99.241:32400',
                'http://68.231.1.54:32400',
                'http://208.103.26.32:32400',
                'http://74.136.35.139:32400',
                'http://73.232.254.34:32400',
                'http://67.160.175.179:32400',
                'http://96.42.77.237:32400',
                'http://73.52.172.154:32400',
                'http://23.255.223.78:32400',
                'http://68.14.73.67:32400',
                'http://24.2.43.206:32400',
                'http://73.231.24.99:81',
                'http://99.119.13.100:32400',
                'http://209.6.236.182:32400',
                'http://50.246.211.5:32400',
                'http://173.60.132.133:80',
                'http://96.44.145.155:32400',
                'http://72.71.243.161:32400',
                'http://50.170.218.176:32400',
                'http://108.183.16.153:32400',
                'http://50.160.8.127:32400',
                'http://73.221.75.146:32400',
                'http://76.17.26.78:32400',
                'http://67.182.157.53:32400',
                'http://97.91.147.9:32400',
                'http://173.160.101.125:32400',
                'http://24.130.115.148:32400',
                'http://68.41.213.234:32400',
                'http://192.95.97.58:32400',
                'http://24.251.114.229:32400',
                'http://23.240.185.129:32400',
                'http://24.13.36.172:32400',
                'http://68.102.246.249:32400']
    


    def OPEN_URL(self,url):
        import urllib2
        response = urllib2.urlopen(url, timeout = 3)
        link=response.read()
        response.close()
        return link    
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

            
        self.AddFileHost(list, res, url,host='PLEX')

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        #import re
        #from entertainment.net import Net
        
        #net = Net(cached=False)
        
        import re,urllib
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        name=name.lower()
        
        for s in self.servers:
            if type == 'tv_episodes':
                try:
                    url=s+'/search?local=1&query='+name.replace(' ','%20')
                    link=self.OPEN_URL(url)
                    title=re.compile('title="(.+?)"').findall(link)[0]
                    title=title.lower()
                    title=title.replace('the ','')
                    name=name.replace('the ','')                  
                    if name.lower() == title.lower():
                        child=re.compile('key="(.+?)"').findall(link)[0]
                        LINK=self.OPEN_URL(s+child)
                        SEASONS=re.compile('ratingKey=".+?" key="(.+?)".+?title="(.+?)"').findall(LINK)
                        for CHILDREN ,SEASON in SEASONS:

                            if season in SEASON:

                                content=self.OPEN_URL(s+CHILDREN)
                                MATCHED=re.compile('ratingKey=".+?" key="(.+?)".+?index="(.+?)".+?videoResolution="(.+?)"',re.DOTALL).findall(content)
                    
                                for KEY , ep, res in MATCHED:
        
                                    if ep == episode:
      
                                        path=s+'/video/:/transcode/universal/start?path='+urllib.quote(s)+urllib.quote(KEY)

                                       
                                        if res.isdigit():
                                            res= res+'P'
                                        else:
                                            res=res.upper()
                                            
                                        self.GetFileHosts(path, list, lock, message_queue,res)                
                except:pass
            else:    
                try:
                    url=s+'/search?local=1&query='+name.replace(' ','%20')
                    link=self.OPEN_URL(url)
                    title=re.compile('title="(.+?)"').findall(link)[0]
                    YEAR=re.compile('year="(.+?)"').findall(link)[0]
                    title=title.lower()
                    title=title.replace('the ','')
                    name=name.replace('the ','')
                    if name.lower() == title.lower():
                        if year in YEAR:
                            key=re.compile('key="(.+?)"').findall(link)[0]
                            path=s+'/video/:/transcode/universal/start?path='+urllib.quote(s)+urllib.quote(key)
                            res=re.compile('videoResolution="(.+?)"').findall(link)[0].upper()
                            if res.isdigit():
                                res =res+'P'
                                
                            self.GetFileHosts(path, list, lock, message_queue,res)
                          
                except:pass

            


    def Resolve(self, url):
        import random,string
        random1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])   
        random = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
        MOVIE_URL=url+'&mediaIndex=0&partIndex=0&protocol=http&offset=0&fastSeek=1&directPlay=0&directStream=1&subtitleSize=100&audioBoost=100&maxVideoBitrate=4000&videoQuality=100&session='+random+'&subtitles=burn&copyts=1&Accept-Language=en&X-Plex-Chunked=1&X-Plex-Product=Plex+Web&X-Plex-Version=2.4.23&X-Plex-Client-Identifier='+random1+'&X-Plex-Platform=Chrome&X-Plex-Platform-Version=47.0&X-Plex-Device=Windows&X-Plex-Device-Name=Plex+Web+(Chrome)'        
        return MOVIE_URL
 
        

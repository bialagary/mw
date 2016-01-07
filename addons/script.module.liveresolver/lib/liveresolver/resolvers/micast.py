# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    #try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
            
        result = client.request(url, referer=referer)
        print(result)
        rtmp = re.findall('.*file:\s*"([^\'"]+).*',result)[0].replace('/liveedge',':443/liveedge')
        
        url = rtmp + ' swfUrl=http://micast.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + url
        return url
    #except:
     # return


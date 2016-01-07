# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client

def resolve(url):
    try:
        result = client.request(url, referer = url)
        pageUrl = re.findall('.*?iframe\s*src=["\']([^"\']+)["\'].*',result)[0]
        result = client.request(pageUrl, referer = url)
        rtmp = re.findall('.*file\w+\s*[:=]\s*"([^\'",]+).*',result)[0].replace(' ','')
        url = rtmp + ' swfUrl=http://direct-stream.biz/jwplayer/jwplayer.flash.swf flashver=WIN\2019,0,0,226 live=1 timeout=14 swfVfy=1 pageUrl=' + pageUrl
        return url
    
    except:
        return


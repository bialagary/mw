# -*- coding: utf-8 -*-


import re,urlparse
from resources.lib.modules import client

def resolve(url):
    try:
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['file'][0]
        referer = 'http://abcast.net/embed.php?file=%s'%id
        result = client.request(url, referer=referer)
        streamer = re.compile("&streamer=(.+?)&").findall(result)[-1]
        file = re.compile("file=(.+?)&").findall(result)[-1]
        url=streamer + ' playPath='+ file  + ' swfUrl=http://abcast.net/juva.swf live=1 timeout=15 swfVfy=1 pageUrl=' + url
        return url
    except:
        return


# -*- coding: utf-8 -*-


import re,urlparse,json,urllib
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        url = 'http://streamup.global.ssl.fastly.net/app/%ss-stream/playlist.m3u8'%id
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})
        return url
    except:
       return



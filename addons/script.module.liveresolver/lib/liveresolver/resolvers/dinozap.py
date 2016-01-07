# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64
from liveresolver.modules import client

def resolve(url):
    try:
        pageUrl = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url)
        embed = re.findall('.*<iframe src="([^"]+)".*',result)[0]
        result = client.request(embed)
        result = urllib.unquote(result)
        ssx1 = base64.b64decode(re.findall('id="ssx1" value="(.+?)"',result)[0])
        ssx4 = base64.b64decode(re.findall('id="ssx4" value="(.+?)"',result)[0])
        token = re.findall('securetoken:\s*(.+?)\s*\}',result)[0]
        app = re.findall('.*rtmp://[\.\w:]*/([^"\']+)',ssx4)[0]
        url = ssx4 + ' app=' + app + ' playpath=' + ssx1 + ' swfUrl=http://www.playerapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf live=true flashver=WIN\2019,0,0,245 token='+ token + ' timeout=15 pageUrl=' + pageUrl
        return url
    except:
        return


# -*- coding: utf-8 -*-


import re,urlparse,json
from liveresolver.modules import client
import urllib

def resolve(url):
    
    try:
        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except: referer = url

        try:
            channel = urlparse.parse_qs(urlparse.urlparse(url).query)['channel'][0]
        except:
            try:
                channel = re.compile('/view/(\d+)/').findall(url)[0]
            except:
                channel = re.compile('/embed/(\d+)&').findall(url)[0]

        page = url.replace('embed','view')
        try:
            ss = page.find('&')
            page = page[:ss]
        except: pass
        result = client.request(page,referer=referer)
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]
        file = re.compile('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=WIN\\2019,0,0,226 live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        return url
    except:
        return



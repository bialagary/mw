# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client

def resolve(url):
    try:
        try:
            cid  = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0] 
        except:
            cid = re.compile('channel/(.+?)(?:/|$)').findall(url)[0]

        url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380'%cid
        pageUrl=url
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer='http://castalba.tv'
        
        result = client.request(url, referer=referer)
        result=urllib.unquote(result)
        if 'm3u8' in result:
            try:
                url = re.compile('file\s*=\s*\'(.+?)\'').findall(result)[0]
            except:
                url = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
        else:
            try:
                filePath = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
            except:
                file = re.findall('var file\s*=\s*(?:\'|\")(.+?)(?:\'|\")',result)[0]
                file2 = re.findall("'file':\s*unescape\(file\)\s*\+\s*unescape\('(.+?)'\)",result)[0]
                filePath = file+file2
            swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]
            try:
                streamer=re.compile("(?:var)?\s*'?streamer'?\s*(?:\:|=)\s*(?:unescape\()?'(.+?)'").findall(result)[0]
            except:
                streamer = re.compile("var sts\s*=\s*'(.+?)'").findall(result)[0]
                
            url = streamer + ' playpath=' + filePath +' swfUrl=' + swf + ' flashver=WIN\\2019,0,0,226 live=true timeout=15 swfVfy=true pageUrl=' + pageUrl


        return url
    
    except:
        return


# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,decryptionUtils


def resolve(url):
	#swf='http://static.zoomtv.me/player/jwplayer.6.5.3.swf'
    referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    headers = { 'referer': referer,
                             'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                             'Connection' : 'keep-alive',
                             'Host' : 'www.zoomtv.me',
                             'Origin' : urlparse.urlparse(referer).netloc
                             }
    fid = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
    cx = urlparse.parse_qs(urlparse.urlparse(url).query)['cx'][0]
    pid = urlparse.parse_qs(urlparse.urlparse(url).query)['pid'][0]
    url = 'http://www.zoomtv.me/embed.php?v=%s&vw=660&vh=450'%fid
    post_data = {'cx' : cx,
    			'lg' : '1' ,
    			'pid' : pid }
    result = client.request(url, post=urllib.urlencode(post_data),headers = headers, mobile=True)

    result = decryptionUtils.doDemystify(result)
    print(result)
    rtmp = re.findall('(rtmp://.+?/zmtvliveme)',result)[0]
    junk,file = re.findall('file',result)[0]
    junk,ts = re.findall('.*[^\w](\w+)\s*=.{0,20}(1[\d]{9})\b.*ts.{0,20}\1.*',result)[0]
    junk,sg = re.findall('.*?[^\w](\w+)\s*=.{0,20}([a-z0-9]{32})\b.*sg.{0,20}\1.*',result)[0]
    res  = client.request(req,referer='http://static.zoomtv.me/player/jwplayer.6.7.4.swf')
    
    if not rtmp:
        rtmp = 'rtmp://94.102.49.62:1935/zmliveme'
    url = rtmp + ' playpath=' + file + ' swfUrl=http://static.zoomtv.me/player/jwplayer.6.7.4.swf flashver=WIN\2019,0,0,245 conn=S:' + file + ' conn=S:' + ts + ' conn=S:' + sg + ' conn=S:V&gt;JWhui^@2ESdu0?}&gt;AN live=1 timeout=15 token=Q!lrB@G1)ww(-dQ4J4 swfVfy=1 pageUrl=' + url
    return url
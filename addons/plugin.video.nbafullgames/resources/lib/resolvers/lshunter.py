# -*- coding: utf-8 -*-


import re,urlparse
from resources.lib.modules import client

def resolve(url):
    try:
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        referer = url
        result = client.request(url, referer=referer)
        streamer = result.replace('//file', '')
        streamer = re.compile("file *: *'(.+?)'").findall(streamer)[-1]

        url=streamer + ' swfUrl=http://www.lshstream.com/jw/jwplayer.flash.swf flashver=WIN/2019,0,0,226 live=1 token=SECURET0KEN#yw%.?()@W! timeout=14 swfVfy=1 pageUrl=http://cdn.lshstream.com/embed.php?u=' + id

        return url
    except:
        return


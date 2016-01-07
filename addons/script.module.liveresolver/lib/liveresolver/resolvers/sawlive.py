# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,base64
from liveresolver.modules import client
from liveresolver.modules import jsunpack

def resolve(url):
    try:
        page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
        page = 'http://%s/embed/%s' % (page[0], page[1])
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = page

        try: host = urlparse.parse_qs(urlparse.urlparse(url).query)['host'][0]
        except: host = 'sawlive.tv'

        headers={'User-Agent': client.agent(),'Host': host, 'Referer': referer, 'Connection': 'keep-alive'}
        
        result = client.request(page, referer=referer)
        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: pass
        result += unpacked
        result = urllib.unquote_plus(result)
        result = re.sub('\s\s+', ' ', result)
        url = client.parseDOM(result, 'iframe', ret='src')[-1]
        url = url.replace(' ', '')

        var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
        for i in range(100):
            for v in var: url = url.replace("'%s'" % v[0], v[1])
            for v in var: url = url.replace("(%s)" % v[0], "(%s)" % v[1])

        url = re.sub(r"'unescape\((.+?)\)'", r'\1', url)
        url = re.sub(r"'(.+?)'", r'\1', url)

        #js functions replaced
        funcs = re.findall('function\s*(.+?)\((.+?)\){return\s*"?(.+?)\"?\;\}',result)
        params = re.findall(r"(un.+?)\((.+?)\)", url)
        funcs2 = re.findall('function\s*(.+?)\((.+?)\){var\s(.+?)\s*=\s*\'(.+?)\';return\s*"?(.+?)\"?\;\}',result)
        for p in params:
            for f in funcs:
                if p[0]==f[0]:
                    if 'unescape(' not in f[2]:
                        url = url.replace('%s(%s)'%(f[0],p[1]),f[2])
                    else:
                        url = url.replace('%s(%s)'%(p[0],p[1]),p[1])

            for f in funcs2:
                if p[0]==f[0]:
                    url = url.replace('%s(%s)'%(f[0],p[1]),f[3])
        result = client.request(url, headers=headers)
        file = re.compile("'file'.+?'(.+?)'").findall(result)[0]

        try:
            if not file.startswith('http'): raise Exception()
            url = client.request(file, output='geturl')
            if not '.m3u8' in url: raise Exception()
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
            return url
        except:
            pass

        strm = re.compile("'streamer'.+?'(.+?)'").findall(result)[0]
        swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]

        url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=30' % (strm, file, swf, url)
        return url
    except:
        return



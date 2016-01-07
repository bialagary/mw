"""
    Kodi urlresolver plugin
    Copyright (C) 2014  smokdpi

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
"""


from t0mm0.common.net import Net
from urlresolver import common
from urlresolver.plugnplay import Plugin
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
import re
import urllib
import urllib2
import xbmcgui


class AaaaGoogleResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "si_googlevideo"
    domains = ["googlevideo.com", "picasaweb.google.com", "googleusercontent.com", "plus.google.com", "googledrive.com"]

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.pattern = 'http[s]*://(.*?(?:\.googlevideo|(?:picasaweb|plus)\.google|google(?:usercontent|drive))\.com)/(.*?(?:videoplayback\?|\?authkey|host/)*.+)'
        self.net = Net()
        self.user_agent = common.IE_USER_AGENT
        self.net.set_user_agent(self.user_agent)
        self.headers = {'User-Agent': self.user_agent}

    def get_url(self, host, media_id):
        return 'https://%s/%s' % (host, media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r: return r.groups()
        else: return False

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return re.match(self.pattern, url)

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        self.headers['Referer'] = web_url
        stream_url = ''
        vid_sel = web_url
        if ('picasaweb.' in host) or ('plus.' in host):
            vid_sel = ''
            videos = []
            vid_id = re.search('(?:.*?#|.+/)(.+?)(?:\?|$)', web_url)
            if vid_id:
                vid_id = vid_id.group(1)
                resp = self.net.http_GET(web_url, headers=self.headers)
                if 'picasaweb.' in host:
                    html = re.search('\["shared_group_' + re.escape(vid_id) + '"\](.+?),"ccOverride":"false"}',
                                     resp.content, re.DOTALL)
                    if html:
                        videos = re.compile(',{"url":"(https://.+?\.google(?:video|usercontent)\.com/.+?)","height":([0-9]+?),"width":([0-9]+?),"type":"video/.+?"}').findall(html.group(1))
                elif 'plus.' in host:
                    html = re.search('"' + re.escape(vid_id) + '",\[\](.+?),"https://video.googleusercontent.com/.*?"',
                                     resp.content, re.DOTALL)
                    if html:
                        temp = re.compile('\[(\d+),(\d+),(\d+),"(.+?)"\]').findall(html.group(1))
                        if temp:
                            for i, w, h, v in temp:
                                videos.append([str(v).replace('\\u003d', '='), int(h)])
                vid_list = []
                url_list = []
                best = 0
                quality = 0
                if videos:
                    if len(videos) > 1:
                        for index, video in enumerate(videos):
                            if int(video[1]) > quality:
                                best = index
                            quality = int(video[1])
                            vid_list.extend(['GoogleVideo - %sp' % quality])
                            url_list.extend([video[0]])
                    if len(videos) == 1:
                        vid_sel = videos[0][0]
                    else:
                        if self.get_setting('auto_pick') == 'true':
                            vid_sel = url_list[best]
                        else:
                            result = xbmcgui.Dialog().select('Choose a link', vid_list)
                            if result != -1:
                                vid_sel = url_list[result]
                            else:
                                raise UrlResolver.ResolverError('No link selected')
        if vid_sel:
            if ('redirector.' in vid_sel) or ('googleusercontent' in vid_sel):
                stream_url = urllib2.urlopen(vid_sel).geturl()
            elif 'google' in vid_sel:
                stream_url = vid_sel
            if stream_url:
                return self.__add_headers_for_kodi(stream_url)

        raise UrlResolver.ResolverError('File not found')

    def get_settings_xml(self):
        xml = PluginSettings.get_settings_xml(self)
        xml += '<setting id="%s_auto_pick" type="bool" label="Automatically pick best quality" default="false" visible="true"/>' % (self.__class__.__name__)
        return xml

    def __add_headers_for_kodi(self, url):
        _referer = urllib.quote_plus('http://%s/' % self.domains[0])
        _user_agent = urllib.quote_plus(self.net._user_agent)
        _connection_timeout = '60'
        _cookies = ''
        for _cookie in self.net._cj:
            _cookies += urllib.quote_plus('%s=%s;' % (_cookie.name, _cookie.value))
        if _cookies:
            return '%s|Referer=%s&User-Agent=%s&Connection-Timeout=%s&Cookie=%s' % \
                   (url, _referer, _user_agent, _connection_timeout, _cookies)
        else:
            return '%s|Referer=%s&User-Agent=%s&Connection-Timeout=%s' % \
                   (url, _referer, _user_agent, _connection_timeout)

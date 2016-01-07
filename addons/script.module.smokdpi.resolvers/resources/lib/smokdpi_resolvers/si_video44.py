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
from urlresolver import HostedMediaFile
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
from urlresolver import common
import urllib
import re


class AaaaVideo44Resolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "si_video44.net"
    domains = ["video44.net", "easyvideo.me"]

    def __init__(self):
        p = self.get_setting('priority') or 99
        self.priority = int(p)
        self.net = Net()
        self.pattern = 'http://((?:www.)?(?:video44.net|easyvideo.me))/gogo/.*?file=([%0-9a-zA-Z\-_\.]+).*?'
        self.user_agent = common.IE_USER_AGENT
        self.net.set_user_agent(self.user_agent)
        self.headers = {'User-Agent': self.user_agent}

    def get_url(self, host, media_id):
        media_id = re.sub(r'%20', '_', media_id)
        return 'http://%s/gogo/?sv=1&file=%s' % (host, media_id)

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r: return r.groups()
        else: return False

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return re.match(self.pattern, url) or self.name in host

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        self.headers['Referer'] = web_url
        html = self.net.http_GET(web_url, headers=self.headers).content
        r = re.search('file\s*:\s*"(.+?)"', html)
        if not r:
            r = re.search('playlist:.+?url:\s*\'(.+?)\'', html, re.DOTALL)
        if r:
            if 'google' in r.group(1):
                return HostedMediaFile(url=r.group(1)).resolve()
            else:
                return self.__add_headers_for_kodi(r.group(1))
        else:
            raise UrlResolver.ResolverError('File not found')

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

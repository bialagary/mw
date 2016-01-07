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
from urlparse import urlparse
import urllib
import urllib2
import re
from lib import jsunpack


class AaaaPlay44Resolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "si_play44.net"
    domains = ["play44.net", "byzoo.org", "playpanda.net", "playbb.me", "videozoo.me", "videowing.me"]

    def __init__(self):
        p = self.get_setting('priority') or 99
        self.priority = int(p)
        self.net = Net()
        self.pattern = 'http://((?:www\.)*(?:play44|byzoo|playpanda|playbb|videozoo|videowing)\.(?:me|org|net)/(?:embed[/0-9a-zA-Z]*?|gplus)(?:\.php)*)\?.*?((?:vid|video|id)=[%0-9a-zA-Z_\-\./]+|.*)[\?&]*.*'
        self.user_agent = common.IE_USER_AGENT
        self.net.set_user_agent(self.user_agent)
        self.headers = {'User-Agent': self.user_agent}

    def get_url(self, host, media_id):
        if media_id: return 'http://%s?%s' % (host, media_id)
        else: return 'http://%s' % host

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
        stream_url = ''
        new_host = urlparse(web_url).netloc
        html = self.net.http_GET(web_url, headers=self.headers).content
        if 'videozoo' not in new_host:
            r = re.search('(?:playlist:|timer\s*=\s*null;).+?url\s*[:=]+\s*[\'"]+(.+?)[\'"]+', html, re.DOTALL)
        else:
            r = re.search('\*/\s+?(eval\(function\(p,a,c,k,e,d\).+)\s+?/\*', html)
            if r:
                try:
                    r = jsunpack.unpack(r.group(1))
                    if r:
                        r = re.search('\[{"url":"(.+?)"', r.replace('\\', ''))
                except:
                    if r:
                        re_src = re.search('urlResolvers\|2F(.+?)\|', r.group(1))
                        re_url = re.search('php\|3D(.+?)\|', r.group(1))
                        r = None
                        if re_src and re_url:
                            stream_url = 'http://%s/%s.php?url=%s' % (new_host, re_src.group(1), re_url.group(1))
                            stream_url = self._redirect_test(stream_url)
        if r:
            stream_url = urllib.unquote_plus(r.group(1))
            if 'http' not in stream_url:
                stream_url = 'http://' + host + '/' + stream_url.replace('/gplus.php', 'gplus.php').replace('/picasa.php', 'picasa.php')
            stream_url = self._redirect_test(stream_url)
            """ Rebuild stream_url with only st= and e= flags """
            s = re.search('(http://.+/)(.+?)\?.*(st=[0-9a-zA-Z_\-]+).*?(e=[0-9]+).*', stream_url)
            if s:
                stream_url = str(s.group(1)) + str(s.group(2)) + '?' + str(s.group(3)) + '&' + str(s.group(4))
        if stream_url:
            if 'google' in stream_url:
                return HostedMediaFile(url=stream_url).resolve()
            else:
                return self.__add_headers_for_kodi(stream_url)
        else:
            raise UrlResolver.ResolverError('File not found')

    def _redirect_test(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', self.user_agent)]
        opener.addheaders = [('Referer', urlparse(url).netloc)]
        try:
            """ Quick test for redirected stream_url """
            resp = opener.open(url)
            if url != resp.geturl():
                return resp.geturl()
            else:
                return url
        except urllib2.HTTPError, e:
            if e.code == 403:
                if url != e.geturl():
                    return e.geturl()
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

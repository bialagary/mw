"""
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


from urlresolver import HostedMediaFile
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re


class AaaaAShortcut(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "aaaa_ashortcut"
    domains = ["*"]

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.pattern = '^(zc)://([0-9]+?)(?:/|$)'

    def get_url(self, host, media_id):
        if host == 'zc':
            url = 'http://zerocast.tv/embed.php?a=%s&id=&width=640&height=480&autostart=true&strech='
            return url % media_id
        else:
            raise UrlResolver.ResolverError('No shortcut found')

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r: return r.groups()
        else: return False

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return re.match(self.pattern, url) or self.name in host

    def get_media_url(self, host, media_id):
        url = self.get_url(host, media_id)
        return HostedMediaFile(url=url).resolve()

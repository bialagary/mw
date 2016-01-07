"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import scraper
import re
import urlparse
import urllib
from salts_lib import kodi
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

BASE_URL = 'http://oneclicktvshows.com'
FORMATS = ['x265', 'x264', 'webrip', 'webdl']

class OCTV_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'OneClickTVShows'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        if 'format' in item:
            label = '[%s] (%s) %s ' % (item['quality'], item['format'], item['host'])
        else:
            label = '[%s] %s ' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            
            for match in re.finditer('<a[^>]+href="([^"]+)[^>]+>(.*?)</a>', html):
                stream_url, title = match.groups()
                title = re.sub('<span[^>]*>|</span>', '', title)
                title = title.strip()
                if title[-2:].upper() in ('MB', 'GB'):
                    _title, season, episode, height, extra = self._parse_episode_link(title)
                    if int(season) == int(video.season) and int(episode) == int(video.episode):
                        host = urlparse.urlparse(stream_url).hostname
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': self._height_get_quality(height), 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                        for vid_format in FORMATS:
                            if vid_format in extra.lower():
                                hoster['format'] = vid_format
                                break
                        hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return super(OCTV_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        return show_url

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=8)
        results = []
        for match in re.finditer('<div\s+class="home_post_box"\s+onClick="location\.href=\'([^\']+).*?<h3>([^<]+)', html, re.DOTALL):
            url, match_title = match.groups()
            result = {'url': self._pathify_url(url), 'title': match_title, 'year': ''}
            results.append(result)

        return results

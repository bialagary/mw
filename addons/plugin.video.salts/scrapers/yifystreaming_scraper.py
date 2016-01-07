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
import urllib
import urlparse
import re
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib import dom_parser

BASE_URL = 'http://yify-streaming.com'
CATEGORIES = {VIDEO_TYPES.MOVIE: 'category-movies', VIDEO_TYPES.EPISODE: 'category-tv-series'}

class YifyStreaming_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'yify-streaming'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            q_str = ''
            match = re.search('<h2>([^<]+)', html)
            if match:
                q_str = match.group(1)
                
            match = re.search('href=[\'"]([^\'"]+)[^>]*>Download Now<', html)
            if match:
                stream_url = match.group(1)
                host = urlparse.urlparse(stream_url).hostname
                hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': self._blog_get_quality(video, q_str, host), 'host': host, 'rating': None, 'views': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        self.create_db_connection()
        url = None

        if video.video_type == VIDEO_TYPES.MOVIE:
            result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name())
            if result:
                url = result[0][0]
                log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url))
            else:
                results = self.search(video.video_type, video.title, video.year)
                if results:
                    url = results[0]['url']
        else:
            result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
            if result:
                url = result[0][0]
                log_utils.log('Got local related url: |%s|%s|%s|' % (video, self.get_name(), url))
            else:
                url = self._get_episode_url('', video)
                if url:
                    self.db_connection.set_related_url(VIDEO_TYPES.EPISODE, video.title, video.year, self.get_name(), url, video.season, video.episode)

        return url

    def _get_episode_url(self, show_url, video):
        search_title = '%s S%02dE%02d' % (video.title, int(video.season), int(video.episode))
        results = self.search(video.video_type, search_title, '')
        for result in results:
            if re.search('S%02dE%02d' % (int(video.season), int(video.episode)), result['title'], re.I):
                return result['url']
    
    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
            
        elements = dom_parser.parse_dom(html, 'li', {'class': '[^"]*post-\d+[^"]*'})
        results = []
        for element in elements:
            match = re.search('href="([^"]+)[^>]+>\s*([^<]+)', element, re.DOTALL)
            if match:
                url, match_title_year = match.groups()
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)\s*(.*)', match_title_year)
                if match:
                    match_title, match_year, extra_title = match.groups()
                    match_title += ' [%s]' % (extra_title)
                else:
                    match_title = match_title_year
                    match_year = ''
                
                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': self._pathify_url(url)}
                    results.append(result)

        return results

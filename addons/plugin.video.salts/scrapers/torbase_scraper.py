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
import json
import xbmcvfs
import xbmc
import os
from salts_lib import log_utils
from salts_lib import kodi
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import XHR
from salts_lib.constants import QUALITIES

BASE_URL = 'http://torba.se'
SEARCH_URL = '/api/movies/list.json?genres=All+genres&limit=40&order=recent&q=%s&year=All+years'
PLAYER_URL = '/api/movies/player.json?slug=%s'
M3U8_PATH = os.path.join(xbmc.translatePath(kodi.get_profile()), 'torbase.m3u8')
M3U8_TEMPLATE = [
    '#EXTM3U',
    '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="{audio_group}",DEFAULT=YES,AUTOSELECT=YES,NAME="Stream 1",URI="{audio_stream}"',
    '',
    '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={bandwidth},NAME="{stream_name}",AUDIO="{audio_group}"',
    '{video_stream}']

class TorbaSe_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'torba.se'

    def resolve_link(self, link):
        try:
            xbmcvfs.delete(M3U8_PATH)
            query = urlparse.parse_qs(link)
            query = dict([(key, query[key][0]) if query[key] else (key, '') for key in query])
            f = xbmcvfs.File(M3U8_PATH, 'w')
            for line in M3U8_TEMPLATE:
                line = line.format(**query)
                f.write(line + '\n')
            f.close()
            return M3U8_PATH
        except:
            return None

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            slug = re.sub('^/v/', '', source_url)
            source_url = PLAYER_URL % (slug)
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            html = html.replace('\\"', '"')
            match = re.search('<iframe[^>]+src="([^"]+)', html)
            if match:
                st_url = match.group(1)
                html = self._http_get(st_url, cache_limit=.5)
                match = re.search('{\s*file\s*:\s*"([^"]+)', html)
                if match:
                    pl_url = urlparse.urljoin(st_url, match.group(1))
                    playlist = self._http_get(pl_url, cache_limit=.5)
                    sources = self.__get_streams_from_m3u8(playlist.split('\n'), st_url)
                    for source in sources:
                        hoster = {'multi-part': False, 'host': self._get_direct_hostname(source), 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': source, 'direct': True}
                        hosters.append(hoster)
                
        return hosters

    def __get_streams_from_m3u8(self, playlist, st_url):
        sources = {}
        quality = QUALITIES.HIGH
        audio_group = ''
        audio_stream = ''
        stream_name = 'Unknown'
        bandwidth = 0
        for line in playlist:
            if line.startswith('#EXT-X-MEDIA'):
                match = re.search('GROUP-ID="([^"]+).*?URI="([^"]+)', line)
                if match:
                    audio_group, audio_stream = match.groups()
            if line.startswith('#EXT-X-STREAM-INF'):
                match = re.search('BANDWIDTH=(\d+).*?NAME="(\d+p)', line)
                if match:
                    bandwidth, stream_name = match.groups()
                    quality = self._height_get_quality(stream_name)
            elif line.endswith('m3u8'):
                stream_url = urlparse.urljoin(st_url, line)
                query = {'audio_group': audio_group, 'audio_stream': audio_stream, 'stream_name': stream_name, 'bandwidth': bandwidth, 'video_stream': stream_url}
                stream_url = urllib.urlencode(query)
                sources[stream_url] = quality
                
        return sources
        
    def get_url(self, video):
        return super(TorbaSe_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, headers=XHR, cache_limit=1)
        results = []
        if html:
            try:
                js_result = json.loads(html)
            except ValueError:
                log_utils.log('Invalid JSON returned: %s: %s' % (search_url, html), log_utils.LOGWARNING)
            else:
                if 'result' in js_result:
                    for item in js_result['result']:
                        match_title = item['title']
                        match_year = str(item['year']) if 'year' in item else ''
    
                        if not year or not match_year or year == match_year:
                            result = {'title': match_title, 'year': match_year, 'url': '/v/' + item['slug']}
                            results.append(result)

        return results

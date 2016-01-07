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
import os
import time
import urllib2
import hashlib
from salts_lib import kodi
from salts_lib.trans_utils import i18n
from salts_lib import pyaes
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES

BASE_URL = 'http://shush.se'
IV = '\0' * 16

class Shush_Proxy(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.__update_scraper_py()
        try:
            import shush_scraper
            self.__scraper = shush_scraper.Shush_Scraper(timeout)
        except Exception as e:
            log_utils.log('Failure during shush scraper creation: %s' % (e), log_utils.LOGWARNING)
            self.__scraper = None
   
    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])
    
    @classmethod
    def get_name(cls):
        return 'Shush.se'
    
    def resolve_link(self, link):
        if self.__scraper is not None:
            return self.__scraper.resolve_link(link)
    
    def format_source_label(self, item):
        if self.__scraper is not None:
            return self.__scraper.format_source_label(item)
    
    def get_sources(self, video):
        if self.__scraper is not None:
            return self.__scraper.get_sources(video)
            
    def get_url(self, video):
        if self.__scraper is not None:
            return self.__scraper.get_url(video)
    
    def search(self, video_type, title, year):
        if self.__scraper is not None:
            return self.__scraper.search(video_type, title, year)
        else:
            return []
    
    def _get_episode_url(self, show_url, video):
        if self.__scraper is not None:
            return self.__scraper._get_episode_url(show_url, video)

    @classmethod
    def get_settings(cls):
        settings = super(Shush_Proxy, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-scraper_url" type="text" label="    %s" default="" visible="eq(-4,true)"/>' % (name, i18n('scraper_location')))
        settings.append('         <setting id="%s-scraper_password" type="text" label="    %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('scraper_key')))
        return settings
    
    def __update_scraper_py(self):
        try:
            py_path = os.path.join(kodi.get_path(), 'scrapers', 'shush_scraper.py')
            exists = os.path.exists(py_path)
            scraper_url = kodi.get_setting('%s-scraper_url' % (self.get_name()))
            scraper_password = kodi.get_setting('%s-scraper_password' % (self.get_name()))
            if scraper_url and scraper_password and (not exists or os.path.getmtime(py_path) < time.time() - (4 * 60 * 60)):
                try:
                    req = urllib2.urlopen(scraper_url)
                    cipher_text = req.read()
                except Exception as e:
                    log_utils.log('Failure during %s scraper get: %s' % (self.get_name(), e), log_utils.LOGWARNING)
                    return
                
                if cipher_text:
                    scraper_key = hashlib.sha256(scraper_password).digest()
                    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(scraper_key, IV))
                    new_py = decrypter.feed(cipher_text)
                    new_py += decrypter.feed()
                    
                    old_py = ''
                    if os.path.exists(py_path):
                        with open(py_path, 'r') as f:
                            old_py = f.read()
                    
                    log_utils.log('%s path: %s, new_py: %s, match: %s' % (self.get_name(), py_path, bool(new_py), new_py == old_py), log_utils.LOGDEBUG)
                    if old_py != new_py:
                        with open(py_path, 'w') as f:
                            f.write(new_py)
        except Exception as e:
            log_utils.log('Failure during %s scraper update: %s' % (self.get_name(), e), log_utils.LOGWARNING)

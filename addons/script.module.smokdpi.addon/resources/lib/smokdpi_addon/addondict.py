# -*- coding: UTF-8 -*-
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


import ast
import re
from datetime import datetime


class AddonDict(dict):

    def __init__(self, dict_type=0):
        """

        :param dict_type: int: 0 - video
                                1 - music <not fully implemented/never tested>
                                2 - picture <not fully implemented/never tested>
                                3 - directory
        """

        super(AddonDict, self).__init__()
        if not isinstance(dict_type, int): raise TypeError
        if 3 >= dict_type >= 0: self.type = dict_type
        else: self.type = 0
        self.template()
        self.__not_strings_ = ['type', 'context', 'count', 'size', 'multi-part', 'parts', 'playcount', 'watched', 'year',
                               'tracknumber', 'castandrole', 'cast', 'overlay', 'rating', 'episode', 'season', 'top250',
                               'contextmenu_items', 'context_replace']

    def template(self):
        """

        :return:
        """
        self['mode'] = ''
        self['site'] = ''
        self['sub_site'] = ''
        self['context'] = 3
        self['contextmenu_items'] = []
        self['context_replace'] = False
        self['type'] = self.type  # used for conversion from string dict/re-initilizing
        self['content'] = ''  # string  (files, songs, artists, albums, movies, tvshows, episodes, musicvideos)
        self['title'] = ''  # string
        self['src_title'] = ''  # string - title to be used for host in playback module
        self['src_quality'] = 'sd'  # string - quality of source to be used for host in playback module ('HD', 'HQ', 'SD', 'LQ')
        self['url'] = ''
        self['count'] = 0  # integer  (12) - can be used to store an id for later, or for sorting purposes
        self['size'] = 0  # long  (1024) - size in bytes
        self['date'] = datetime.now().strftime("%d.%m.%Y")  # string  (%d.%m.%Y / 01.01.2009) - file date
        self['multi-part'] = False
        self['parts'] = []
        self['imgs_prepacked'] = 'false'
        if self.type == 0:
            self['backdrop_url'] = ''
            self['cover_url'] = ''
            self['thumb_url'] = ''
            self['banner_url'] = ''
            self['poster'] = ''
            self['imdb_id'] = ''
            self['tmdb_id'] = ''
            self['tvdb_id'] = ''
            self['episode_id'] = ''
            self['genre'] = ''  # string  (Comedy)
            self['year'] = 0  # integer  (2009)
            self['episode'] = 0  # integer  (4)
            self['season'] = 0  # integer  (1)
            self['top250'] = 0  # integer  (192)
            self['tracknumber'] = 0  # integer  (3)
            self['rating'] = 0.0  # float  (6.4) - range is 0..10
            self['watched'] = 0  # depreciated - use playcount instead
            self['playcount'] = 0  # integer  (2) - number of times this item has been played
            self['overlay'] = 6  # integer  (2) - range is 0..8.  See GUIListItem.h for values
            self['cast'] = []  # list  (Michal C. Hall)
            self['castandrole'] = []  # list  (Michael C. Hall|Dexter)
            self['director'] = ''  # string  (Dagur Kari)
            self['mpaa'] = ''  # string  (PG-13)
            self['plot'] = ''  # string  (Long Description)
            self['plotoutline'] = ''  # string  (Short Description)
            self['originaltitle'] = ''  # string  (Big Fan)
            self['duration'] = '1500'  # string  - duration in seconds (95)
            self['studio'] = ''  # string  (Warner Bros.)
            self['tagline'] = ''  # string  (An awesome movie) - short description of movie
            self['writer'] = ''  # string  (Robert D. Siegel)
            self['tvshowtitle'] = ''  # string  (Heroes)
            self['premiered'] = ''  # string  (2005-03-04)
            self['status'] = ''  # string  (Continuing) - status of a TVshow
            self['code'] = self['imdb_id']  # string  (tt0110293) - IMDb code
            self['aired'] = ''  # string  (2008-12-07)
            self['credits'] = ''  # string  (Andy Kaufman) - writing credits
            self['lastplayed'] = ''  # string  (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
            self['album'] = ''  # string  (The Joshua Tree)
            self['votes'] = ''  # string  (12345 votes)
            self['trailer'] = ''  # string  (/home/user/trailer.avi)
        elif self.type == 1:
            self['cover_url'] = ''
            self['backdrop_url'] = ''
            self['tracknumber'] = 0  # integer  (8)
            self['duration'] = '210'  # integer  (245) - duration in seconds
            self['year'] = 0  # integer  (1998)
            self['genre'] = ''  # string  (Rock)
            self['album'] = ''  # string  (Pulse)
            self['artist'] = ''  # string  (Muse)
            self['rating'] = ''  # string  (3) - single character between 0 and 5
            self['lyrics'] = ''  # string  (On a dark desert highway...)
            self['playcount'] = 0  # integer  (2) - number of times this item has been played
            self['lastplayed'] = ''  # string  (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
        elif self.type == 2:
            self['picturepath'] = ''  # string  (/home/username/pictures/img001.jpg)
            self['exif*'] = ''  # string  (See CPictureInfoTag::TranslateString in PictureInfoTag.cpp for valid strings)

    def labels(self):
        """

        :return:
        """
        labels = {}
        try: self.keys()
        except: return labels
        info_keys = ['title', 'count', 'size', 'date', 'genre', 'year', 'episode', 'season', 'top250', 'tracknumber',
                     'rating', 'watched', 'playcount', 'overlay', 'cast', 'castandrole', 'director', 'mpaa', 'plot',
                     'plotoutline', 'originaltitle', 'duration', 'studio', 'tagline', 'writer', 'tvshowtitle',
                     'premiered', 'status', 'code', 'aired', 'credits', 'lastplayed', 'album', 'votes', 'trailer',
                     'tracknumber', 'duration', 'year', 'genre', 'album', 'artist', 'rating', 'lyrics', 'playcount',
                     'lastplayed', 'picturepath', 'exif*']
        for key, value in self.iteritems():
            if key in self.__not_strings_ and isinstance(value, str): labels[key] = eval(value)
            else: labels[key] = value
        return labels

    def media_type(self, return_type=0):
        """
        Return media_type for metahandler from self['content'] type
        :param return_type: int: 0 - returns: int ( 0 - video, 1 - music, 2 - picture, 3 - other file )
                                 1 - returns: more specific string value(used with metahandlers)
                                     (file, picture, music, movie, tvshow, musicvideo)
        """
        if not self['content']: return None
        content = self['content'].lower()
        if not isinstance(return_type, int):
            try: return_type = int(return_type)
            except: return_type = 0
        if return_type == 0:
            if re.match('.*(tvshow|episode|movie|musicvid).*', content): return 0
            elif re.match('.*(song|artist|album).*', content): return 1
            elif self.type == 2: return 2
            else: return 3
        elif return_type == 1:
            if re.match('.*(tvshow|episode).*', content): return 'tvshow'
            elif re.match('.*(movie).*', content): return 'movie'
            elif re.match('.*(musicvid).*', content): return 'musicvideo'
            elif re.match('.*(song|artist|album).*', content): return 'music'
            elif self.type == 2: return 'picture'
            else: return 'file'

    def str_update(self, string_dict):
        """
        Merge a str(dict)/dict.__str__ with self
        :param string_dict: str: string representation of a dict
        :return: XBMCDict of string dict
        """
        if not isinstance(string_dict, str): raise TypeError
        to_dict = ast.literal_eval(string_dict)
        for key, value in to_dict.iteritems():
            if key in self.__not_strings_ and isinstance(value, str): self[key] = eval(value)
            else: self[key] = value
        return self

    def update(self, E=None, **F):
        """

        """
        try: E.keys()
        except: E = {}
        for key, value in E.iteritems():
            if key in self.__not_strings_ and isinstance(value, str): self[key] = eval(value)
            else: self[key] = value
        return self

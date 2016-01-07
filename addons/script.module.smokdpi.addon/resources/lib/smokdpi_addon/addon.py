# -*- coding: UTF-8 -*-
"""
    Original Source:
        Eldorado (original: t0mm0)
        script.module.addon.common\lib\addon\common\addon.py
        https://github.com/Eldorados/script.module.addon.common/blob/master/lib/addon/common/addon.py

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


import re
import os
try:
    import cPickle as pickle
except:
    import pickle
import xbmc
import xbmcgui
import xbmcplugin
import time
import ast
import urllib
import urllib2
import httplib
import common
from addondict import AddonDict
from contextmenu import ContextMenu
from BeautifulSoup import BeautifulSoup


class Addon:

    def __init__(self, argv=common.argv):
        if not argv: return
        self.addon = common.thisaddon
        self.module = common.thismodule
        self.common = common
        self.addon_name = common.addon_name
        self.icon = common.icon
        self.fanart = common.fanart
        self.language = common.language
        self.alert = common.alert
        self.error = common.error
        self.image = common.image
        self.art = common.art
        self.build_plugin_url = common.build_plugin_url
        self.parse_query = common.parse_query
        self.argv = argv
        self.url = common.url
        self.handle = common.handle
        self.queries = common.queries
        self.net = common.net
        self._view_content_type = ''

    def resolve_url(self, stream_url):
        """
        Tell XBMC that you have resolved a URL (or not!).
        
        This method should be called as follows:
        
        #. The user selects a list item that has previously had ``isPlayable``
           set (this is true for items added with :meth:`add_item`, 
           :meth:`add_music_item` or :meth:`add_music_item`)
        #. Your code resolves the item requested by the user to a media URL
        #. Your addon calls this method with the resolved URL
        
        Args:
            stream_url (str or ``False``): If a string, tell XBMC that the 
            media URL ha been successfully resolved to stream_url. If ``False`` 
            or an empty string tell XBMC the resolving failed and pop up an 
            error messsage.
        """
        if stream_url:
            xbmcplugin.setResolvedUrl(self.handle, True, xbmcgui.ListItem(path=stream_url))
        else:
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())
    
    def get_playlist(self, pl_type, new=False):
        """
        Return a :class:`xbmc.Playlist` object of the specified type.
        
        The available playlist types are defined in the :mod:`xbmc` module and 
        are currently as follows::
        
            xbmc.PLAYLIST_MUSIC = 0
            xbmc.PLAYLIST_VIDEO = 1
            
        .. seealso::
            
            :meth:`get_music_playlist`, :meth:`get_video_playlist`
            
        Args:
            pl_type (int): The type of playlist to get.
            
            new (bool): If ``False`` (default), get the current 
            :class:`xbmc.Playlist` object of the type specified. If ``True`` 
            then return a new blank :class:`xbmc.Playlist`.

        Returns:
            A :class:`xbmc.Playlist` object.
        """
        pl = xbmc.PlayList(pl_type)
        if new:
            pl.clear()
        return pl
     
    def get_music_playlist(self, new=False):
        """
        Convenience method to return a music :class:`xbmc.Playlist` object.
        
        .. seealso::
        
            :meth:`get_playlist`
        
        Kwargs:
            new (bool): If ``False`` (default), get the current music 
            :class:`xbmc.Playlist` object. If ``True`` then return a new blank
            music :class:`xbmc.Playlist`.
        Returns:
            A :class:`xbmc.Playlist` object.
       """
        self.get_playlist(xbmc.PLAYLIST_MUSIC, new)

    def get_video_playlist(self, new=False):
        """
        Convenience method to return a video :class:`xbmc.Playlist` object.
        
        .. seealso::
        
            :meth:`get_playlist`
        
        Kwargs:
            new (bool): If ``False`` (default), get the current video 
            :class:`xbmc.Playlist` object. If ``True`` then return a new blank
            video :class:`xbmc.Playlist`.
            
        Returns:
            A :class:`xbmc.Playlist` object.
        """
        self.get_playlist(xbmc.PLAYLIST_VIDEO, new)

    def add_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False, img='',
                 fanart='', resolved=False, total_items=0, playlist=False, item_type='video', 
                 is_folder=False):
        """
        Adds an item to the list of entries to be displayed in XBMC or to a 
        playlist.
        
        Use this method when you want users to be able to select this item to
        start playback of a media file. ``queries`` is a dict that will be sent 
        back to the addon when this item is selected::
        
            add_item({'host': 'youtube.com', 'media_id': 'ABC123XYZ'}, 
                     {'title': 'A youtube vid'})
                     
        will add a link to::
        
            plugin://your.plugin.id/?host=youtube.com&media_id=ABC123XYZ
        
        .. seealso::
        
            :meth:`add_music_item`, :meth:`add_video_item`, 
            :meth:`add_directory`
            
        Args:
            queries (dict): A set of keys/values to be sent to the addon when 
            the user selects this item.
            
            infolabels (dict): A dictionary of information about this media 
            (see the `XBMC Wiki InfoLabels entry 
            <http://wiki.xbmc.org/?title=InfoLabels>`_).
            
        Kwargs:
            
            properties (dict): A dictionary of properties that can be set on a list item
            (see the `XBMC Wiki InfoLabels entry and locate Property() elements
            <http://wiki.xbmc.org/?title=InfoLabels>`_).
            
            contextmenu_items (list): A list of contextmenu items
            
            context_replace (bool): To replace the xbmc default contextmenu items
                    
            img (str): A URL to an image file to be used as an icon for this
            entry.
            
            fanart (str): A URL to a fanart image for this entry.
            
            resolved (str): If not empty, ``queries`` will be ignored and 
            instead the added item will be the exact contentes of ``resolved``.
            
            total_items (int): Total number of items to be added in this list.
            If supplied it enables XBMC to show a progress bar as the list of
            items is being built.
            
            playlist (playlist object): If ``False`` (default), the item will 
            be added to the list of entries to be displayed in this directory. 
            If a playlist object is passed (see :meth:`get_playlist`) then 
            the item will be added to the playlist instead
    
            item_type (str): The type of item to add (eg. 'music', 'video' or
            'pictures')
        """
        infolabels = self.unescape_dict(infolabels)
        if not resolved:
            if not is_folder:
                queries['play'] = 'True'
            play = self.build_plugin_url(queries)
        else: 
            play = resolved
        listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
        listitem.setInfo(item_type, infolabels)
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty('fanart_image', fanart)
        
        if properties:
            for prop in properties.items():
                listitem.setProperty(prop[0], prop[1])

        if contextmenu_items:
            listitem.addContextMenuItems(contextmenu_items, replaceItems=context_replace)        
        if playlist is not False:
            playlist.add(play, listitem)
        else:
            xbmcplugin.addDirectoryItem(self.handle, play, listitem,
                                        isFolder=is_folder, 
                                        totalItems=total_items)

    def add_video_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                       img='', fanart='', resolved=False, total_items=0, playlist=False):
        """
        Convenience method to add a video item to the directory list or a 
        playlist.
        
        See :meth:`add_item` for full infomation
        """
        self.add_item(queries, infolabels, properties, contextmenu_items, context_replace, img, fanart,
                      resolved, total_items, playlist, item_type='video')

    def add_music_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                       img='', fanart='', resolved=False, total_items=0, playlist=False):
        """
        Convenience method to add a music item to the directory list or a 
        playlist.
        
        See :meth:`add_item` for full infomation
        """
        self.add_item(queries, infolabels, properties, contextmenu_items, context_replace, img, fanart,
                      resolved, total_items, playlist, item_type='music')

    def add_directory(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                      img='', fanart='', total_items=0, is_folder=True):
        """
        Convenience method to add a directory to the display list or a 
        playlist.
        
        See :meth:`add_item` for full infomation
        """
        self.add_item(queries, infolabels, properties, contextmenu_items, context_replace, img, fanart,
                      total_items=total_items, resolved=self.build_plugin_url(queries), 
                      is_folder=is_folder)

    def _decode_callback(self, matches):
        """Callback method used by :meth:`decode`."""
        id = matches.group(1)
        try:
            return unichr(int(id))
        except:
            return id

    def decode(self, data):
        """
        Regular expression to convert entities such as ``&#044`` to the correct
        characters. It is called by :meth:`unescape` and so it is not required
        to call it directly.
        
        This method was found `on the web <http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931>`_
        
        Args:
            data (str): String to be cleaned.
            
        Returns:
            Cleaned string.
        """
        return re.sub("&#(\d+)(;|(?=\s))", self._decode_callback, data).strip()

    def unescape(self, text):
        """
        Decodes HTML entities in a string.
        
        You can add more entities to the ``rep`` dictionary.
        
        Args:
            text (str): String to be cleaned.
            
        Returns:
            Cleaned string.
        """
        try:
            text = self.decode(text)
            rep = {'&lt;': '<',
                   '&gt;': '>',
                   '&quot': '"',
                   '&rsquo;': '\'',
                   '&acute;': '\'',
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
            # this has to be last:
            text = text.replace("&amp;", "&")
        
        # we don't want to fiddle with non-string types
        except TypeError:
            pass

        return text

    def unescape_dict(self, d):
        """
        Calls :meth:`unescape` on all values in a dictionary.
        
        Args:
            d (dict): A dictionary containing string values
            
        Returns:
            A dictionary with HTML entities removed from the values.
        """
        out = {}
        for key, value in d.items():
            out[key] = self.unescape(value)
        return out
    
    def save_data(self, filename, data):
        """
        Saves the data structure using pickle. If the addon data path does 
        not exist it will be automatically created. This save function has
        the same restrictions as the pickle module.
        
        Args:
            filename (string): name of the file you want to save data to. This 
            file will be saved in your addon's profile directory.
            
            data (data object/string): you want to save.
            
        Returns:
            True on success
            False on failure
        """
        profile_path = self.common.addon_profile_path
        try:
            os.makedirs(profile_path)
        except:
            pass
        save_path = os.path.join(profile_path, filename)
        try:
            pickle.dump(data, open(save_path, 'wb'))
            return True
        except pickle.PickleError:
            return False
        
    def load_data(self, filename):
        """
        Load the data that was saved with save_data() and returns the
        data structure.
        
        Args:
            filename (string): Name of the file you want to load data from. This
            file will be loaded from your addons profile directory.
            
        Returns:
            Data stucture on success
            False on failure
        """
        load_path = os.path.join(self.common.addon_profile_path, filename)
        if not os.path.isfile(load_path):
            return False
        try:
            data = pickle.load(open(load_path))
        except:
            return False
        return data

    def add_items(self, dict_list):
        """
        add_video/music/directory items from a list of dicts
        total_items = len(dict_list)
        required dict items - 'mode':, 'title':, 'cover_url':, 'backdrop_url':
        'contextmenu_items': defaults to []
        'context_replace': defaults to False
        'type': defaults to 3
                0 - video
                1 - music
                2 - picture
                3 - directory
        :param dict_list: [{}]
        :output: add_*item
        """
        most_content = [0, 0, 0]
        if not isinstance(dict_list, list): raise TypeError
        for item in dict_list:
            try: item.keys()
            except: raise TypeError
        self._view_content_type = ''
        for item in dict_list:
            item.setdefault('type', 3)
            item_type = item['type']
            total_items = len(dict_list)
            if not isinstance(item_type, int):
                try: item_type = int(item_type)
                except: item_type = 3
            item.setdefault('context', 3)
            context = item['context']
            if not isinstance(context, int):
                try: context = int(context)
                except: context = 3
            context_items = ContextMenu(context, item).menu()
            item.setdefault('contextmenu_items', [])
            items = item['contextmenu_items']
            if not isinstance(items, list):
                items = ast.literal_eval(items)
                if not isinstance(items, list):
                    items = []
            context_items.extend(items)
            item.setdefault('context_replace', False)
            context_replace = item['context_replace']
            if not isinstance(context_replace, bool):
                context_replace = self.common.to_bool(context_replace)
            if not isinstance(item, AddonDict):
                item = AddonDict(item_type).update(item)

            #
            if item.get('context', 3) != 3:
                content = item.get('content', None)
                if content:
                    if 'movie' in content:
                        most_content[0] += 1
                    elif ('tvshow' in content) or ('season' in content):
                        most_content[1] += 1
                    elif 'episode' in content:
                        most_content[2] += 1

            if self.common.usedirsources():
                if (item_type == 0) and (item.get('mode', 'main').lower() == 'play') and (not self.common.autoplay()):
                    item_type = 3
                    item['type'] = 3

            if item_type == 0:  # video_item
                self.add_video_item(item, item.labels(),
                                    contextmenu_items=context_items, context_replace=context_replace,
                                    fanart=self.common.art(item['backdrop_url']), img=self.common.image(item['cover_url']),
                                    total_items=total_items)
            elif item_type == 1:  # music_item
                pass
            elif item_type == 2:  # picture_item
                pass
            elif item_type == 3:  # directory_item
                self.add_directory(item, item.labels(),
                                   contextmenu_items=context_items, context_replace=context_replace,
                                   fanart=self.common.art(item['backdrop_url']), img=self.common.image(item['cover_url']),
                                   total_items=total_items)
        most = None
        oldhigh = 0
        for i, c in enumerate(most_content):
            if not most:
                if c != 0:
                    oldhigh = c
                    if i == 0: most = 'movies'
                    elif i == 1: most = 'tvshows'
                    elif i == 2: most = 'episodes'
            if most_content[i] > oldhigh:
                oldhigh = c
                if i == 0: most = 'movies'
                elif i == 1: most = 'tvshows'
                elif i == 2: most = 'episodes'
        if most:
            self._view_content_type = most
        else:
            self._view_content_type = ''

    def end_of_directory(self, sort_methods=None, default_sort=None):
        """
        :param sort_methods: int:
                                  0 - video
                                  1 - music <not fully implemented/never tested>
                                  2 - picture <not fully implemented/never tested>
                                  3 - directory/files
        """

        viewid = None
        content = self._view_content_type
        if not content:
            content = self.queries.get('content', '')

        xbmcplugin.setContent(self.handle, content)

        if content:
            if 'movie' in content:
                viewid = self.common.get_setting_db('movie_view')
            elif ('tvshow' in content) or ('season' in content):
                viewid = self.common.get_setting_db('tvshow_view')
            elif 'episode' in content:
                viewid = self.common.get_setting_db('episode_view')

        if not isinstance(default_sort, int):
            try: default_sort = int(default_sort)
            except: default_sort = None
        if default_sort is not None:
            try: xbmcplugin.addSortMethod(self.handle, default_sort)
            except: pass

        if sort_methods is not None:
            if not isinstance(sort_methods, int) and sort_methods:
                try: sort_methods = int(sort_methods)
                except: sort_methods = self.common.addon_type()
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_UNSORTED)
            if sort_methods == 0:
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_RATING)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_EPISODE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LASTPLAYED)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_PLAYCOUNT)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_GENRE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_PRODUCTIONCODE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_STUDIO)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_CHANNEL)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_BITRATE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_COUNTRY)
            elif sort_methods == 1:
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TRACKNUM)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DURATION)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_ARTIST)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_GENRE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_ALBUM)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_SONG_RATING)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_MPAA_RATING)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LISTENERS)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_CHANNEL)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_BITRATE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_COUNTRY)
            elif sort_methods == 2:
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DATE_TAKEN)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_COUNTRY)
            elif sort_methods == 3:
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DRIVE_TYPE)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_FULLPATH)
                xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_SIZE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_FILE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DATEADDED)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DATE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LABEL)
        else:
            xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)

        xbmcplugin.endOfDirectory(self.handle)
        if viewid and content:
            time.sleep(0.2)
            self.common.set_view(str(viewid))

    def search_input(self):
        title = self.language(30808, True) + ' ' + self.common.addon_name
        if self.common.search_history_size_limit() != 0:
            search_queries = self.get_search_history()
            if search_queries:
                if len(search_queries) > 0:
                    search_queries.insert(0, '[B]' + self.language(30815, True) + '[/B]')
                    index = xbmcgui.Dialog().select(title, search_queries)
                    if index > -1:
                        if index != 0:
                            return urllib.quote_plus(search_queries[index])
                    else:
                        return ''
        search = xbmcgui.Dialog().input(title)
        search = search.strip()
        if search:
            search = re.sub(r'\s+', ' ', search)
            self.add_search_history(search)
            search = urllib.quote_plus(search)
            return search
        return ''

    def play_input(self, sub_site):
        title = self.language(30817, True)
        if self.common.play_history_size_limit() != 0:
            play_queries = self.get_play_history(sub_site)
            if play_queries:
                if len(play_queries) > 0:
                    play_queries.insert(0, '[B]' + self.language(30816, True) + '[/B]')
                    play_queries.insert(1, '[B]' + self.language(30879, True) + '[/B]')
                    index = xbmcgui.Dialog().select(title, play_queries)
                    if index > -1:
                        if index == 1:
                            self.common.clear_play_history(sub_site)
                            return ''
                        elif index > 1:
                            return play_queries[index]
                    else:
                        return ''
        this_input = xbmcgui.Dialog().input(title)
        this_input = this_input.strip()
        if this_input:
            this_input = re.sub(r'\s+', ' ', this_input)
            self.add_play_history(sub_site, this_input)
            return this_input
        return ''

    def edit_input(self, to_edit=''):
        if not isinstance(to_edit, str):
            try: to_edit = str(to_edit)
            except: to_edit = ''
        edited = xbmcgui.Dialog().input(self.language(30811, True), to_edit)
        edited = edited.strip()
        if edited:
            search = re.sub(r'\s+', ' ', edited)
            return search
        return ''

    def page_input(self, last_page):
        title = self.common.language(30810, True)
        if not isinstance(last_page, int):
            try: last_page = int(last_page)
            except: last_page = 10000
        if last_page != 10000: title = self.language(30809, True) + ' ' + str(last_page)
        page = xbmcgui.Dialog().numeric(0, title)
        if page:
            if 1 <= int(page) <= last_page: return page
        return ''

    def get_page(self, url, ignore_cache=False):
        if not isinstance(url, str):
            try: url = str(url)
            except: raise TypeError
        cached_content = ''
        if self.common.uses_cache() and not ignore_cache:
            cached_content = self.common.check_cache_expired(url)
        if cached_content:
            return cached_content
        else:
            try:
                cookies = self.net.set_cookies(self.common.cookie_file)
                content = self.net.http_GET(url, {'Referer': url}).content
                cookies = self.net.save_cookies(self.common.cookie_file)
                if isinstance(content, unicode):
                    content.encode('utf-8')
                soup = BeautifulSoup(content, convertEntities=BeautifulSoup.HTML_ENTITIES)
                return_content = soup.renderContents()
                if self.common.uses_cache() and not ignore_cache:
                    self.common.add_to_cache(url, return_content)
                return return_content
            except urllib2.HTTPError, e:
                self.error(e)
                return ''
            except (urllib2.URLError, httplib.HTTPException, AttributeError, ValueError, Exception), e:
                self.error(e)
                return ''

    def extended_menu(self):
        if not self.queries.get('site', None):
            author_links = self.common.author_links
            menu_items = []
            menu_items.extend([self.menu_separator()])
            menu_items.extend([{'mode': '', 'title': self.language(30721, True), 'site': 'lock_toggle',
                                'cover_url': self.image('lock.png'), 'backdrop_url': self.art(), 'type': 3}])
            if author_links:
                menu_items.extend([{'mode': '', 'title': self.language(30100, True),
                                    'site': 'author', 'cover_url': self.image('author.png'),
                                    'backdrop_url': self.art(), 'type': 3}])
            return menu_items
        else:
            return []

    def favs_hist_menu(self, site):
        menu_items = []
        menu_items.extend([{'site': 'favorites', 'sub_site': site, 'title': self.language(30889, True),
                            'cover_url': self.image('favorites.png'), 'backdrop_url': self.art(), 'type': 3}])
        if self.common.history_size_limit() != 0:
            menu_items.extend([{'site': 'history', 'sub_site': site, 'title': self.language(30875, True),
                                'cover_url': self.image('history.png'), 'backdrop_url': self.art(), 'type': 3}])
        return menu_items

    def author_links_menu(self):
        author_links = self.common.author_links
        menu_items = []
        for index, link in enumerate(author_links):
            item_num = 30100 + index + 1
            menu_items.extend([{'mode': '', 'title': self.language(item_num, True), 'url': link,
                                'site': 'execute', 'cover_url': self.image('author_link_' + str(index + 1) + '.png'),
                                'backdrop_url': self.art(), 'type': 3}])
            if index == 10: break
        return menu_items

    def menu_separator(self):
        return {'mode': '', 'title': self.language(30999, True), 'site': 'separator', 'cover_url': self.image(),
                'backdrop_url': self.art(), 'type': 3}

    def add_history(self):
        params = self.queries
        execute = 'INSERT INTO ' + self.common.hist_db_table + \
                  ' (sub_site, content, url, __params_) VALUES (?, ?, ?, ?)'
        inserted = self.common.db.execute(execute, (params['sub_site'], params['content'], params['url'], str(params)))
        if inserted == 1:
            execute = 'SELECT COUNT(*) FROM ' + self.common.hist_db_table + ' WHERE sub_site=?'
            result = int(self.common.db.fetchall(execute, (params['sub_site'],))[0][0])
            if result > self.common.history_size_limit():
                execute = 'DELETE FROM ' + self.common.hist_db_table + ' WHERE ROWID = (SELECT MIN(ROWID) FROM ' + \
                          self.common.hist_db_table + ') AND sub_site=?'
                result = self.common.db.execute(execute, (params['sub_site'],))
                if result == 0:
                    execute = 'DELETE * FROM ' + self.common.hist_db_table + ' WHERE sub_site=?'
                    result = self.common.db.execute(execute, (params['sub_site'],))
                    if result == 0:
                        execute = 'DROP TABLE ' + self.common.hist_db_table
                        result = self.common.db.execute(execute)
                        self.common.create_tables()

    def add_search_history(self, search_query):
        params = self.queries
        site = params.get('sub_site', '')
        if not site:
            site = params.get('site', False)
            if not site:
                return False
        execute = 'INSERT INTO ' + self.common.search_db_table + ' (sub_site, query) VALUES (?, ?)'
        inserted = self.common.db.execute(execute, (site, str(search_query)))
        if inserted == 1:
            execute = 'SELECT COUNT(*) FROM ' + self.common.search_db_table + ' WHERE sub_site=?'
            result = int(self.common.db.fetchall(execute, (site,))[0][0])
            if result > self.common.search_history_size_limit():
                execute = 'DELETE FROM ' + self.common.search_db_table + ' WHERE ROWID = (SELECT MIN(ROWID) FROM ' + \
                          self.common.search_db_table + ') AND sub_site=?'
                result = self.common.db.execute(execute,(site,))
                if result == 0:
                    execute = 'DELETE * FROM ' + self.common.search_db_table + ' WHERE sub_site=?'
                    result = self.common.db.execute(execute,(site,))
                    if result == 0:
                        execute = 'DROP TABLE ' + self.common.search_db_table
                        result = self.common.db.execute(execute)
                        self.common.create_tables()

    def get_search_history(self):
        params = self.queries
        site = params.get('sub_site', '')
        if not site:
            site = params.get('site', False)
            if not site:
                return False
        execute = 'SELECT * FROM ' + self.common.search_db_table + ' WHERE sub_site=? ORDER BY ROWID DESC'
        selected = self.common.db.fetchall(execute, (site,))
        results = []
        if selected:
            for this_id, this_site, this_query in selected:
                results.extend([this_query])
            return results
        else:
            return False

    def add_play_history(self, sub_site, url):
        execute = 'INSERT INTO ' + self.common.play_db_table + ' (sub_site, url) VALUES (?, ?)'
        inserted = self.common.db.execute(execute, (sub_site, str(url)))
        if inserted == 1:
            execute = 'SELECT COUNT(*) FROM ' + self.common.play_db_table + ' WHERE sub_site=?'
            result = int(self.common.db.fetchall(execute, (sub_site,))[0][0])
            if result > self.common.play_history_size_limit():
                execute = 'DELETE FROM ' + self.common.play_db_table + ' WHERE ROWID = (SELECT MIN(ROWID) FROM ' + \
                          self.common.play_db_table + ') AND sub_site=?'
                result = self.common.db.execute(execute,(sub_site,))
                if result == 0:
                    execute = 'DELETE * FROM ' + self.common.play_db_table + ' WHERE sub_site=?'
                    result = self.common.db.execute(execute,(sub_site,))
                    if result == 0:
                        execute = 'DROP TABLE ' + self.common.play_db_table
                        result = self.common.db.execute(execute)
                        self.common.create_tables()

    def get_play_history(self, sub_site):
        execute = 'SELECT * FROM ' + self.common.play_db_table + ' WHERE sub_site=? ORDER BY id DESC'
        selected = self.common.db.fetchall(execute, (sub_site,))
        results = []
        if selected:
            for this_id, this_site, this_query in selected:
                results.extend([this_query])
            return results
        else:
            return False

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


import re
import ast
import xbmc
import xbmcgui
import xbmcplugin
from addon import Addon


class Playback:

    def __init__(self):
        import urlresolver
        self.addon = Addon()
        self.common = self.addon.common
        self.urlresolver = urlresolver
        self.urlresolver.plugnplay.plugin_dirs = []
        if self.common.resolvers:
            self.urlresolver.plugnplay.set_plugin_dirs(self.urlresolver.common.plugins_path, self.common.resolvers_path,
                                                       self.common.builtin_resolvers_path)
        else:
            self.urlresolver.plugnplay.set_plugin_dirs(self.urlresolver.common.plugins_path,
                                                       self.common.builtin_resolvers_path)
        self.urlresolver.plugnplay.load_plugins()

    def _dialog_sources(self, source_list):
        if not isinstance(source_list, list): return
        return self.urlresolver.choose_source(source_list)

    def _directory_sources(self, source_list, dict_list):
        from addondict import AddonDict
        item_list = []
        for index, item in enumerate(source_list):
            multipart = re.search('^playlist://[a-zA-Z0-9_]+?/([0-9]+?)/$', item.get_url())
            if multipart:
                _dict = AddonDict(0).update(dict_list[int(multipart.group(1))])
            else:
                _dict = AddonDict(0).update(dict_list[0])
            _dict['title'] = str(item.title) + ' | ' + str(_dict['title'])
            _dict['site'] = 'play_this'
            _dict['sub_site'] = ''
            _dict['mode'] = ''
            _dict['type'] = 0
            _dict['context'] = 3
            _dict['url'] = str(item.get_url())
            item_list.extend([_dict])

        if item_list:
            self.addon.add_items(item_list)
            self.addon.end_of_directory()

    def _create_source_list(self, dict_list):
        source_list = []
        part_list = []
        full_list = []
        playlist_list = []
        host = re.compile('(?:http|https)://(?:.+?\.)*?([0-9a-zA-Z_\-]+?)\.[0-9a-zA-Z]{2,}(?:/|:).*')
        old_host = ''
        separator = ' | '
        for iindex, item in enumerate(dict_list):
            playlist_host = 'playlist://%s/%s/'
            source_title = ''
            quality = separator + item.get('src_quality', 'SD')
            if item['multi-part']:
                if item['src_title']: source_title = item['src_title'] + separator
                source_host = host.search(item['url'])
                if source_host: source_host = source_host.group(1)
                else: source_host = 'UID'
                for index, part in enumerate(item['parts']):
                    part_title = source_title + source_host + separator + self.common.language(30651, True) + ' ' + str(index + 1) + quality
                    source = self.urlresolver.HostedMediaFile(url=part, title=part_title.upper())
                    if source:
                        part_list.extend([source])
                if old_host != source_host:
                    old_host = source_host
                    playlist_host = playlist_host % (old_host, iindex)
                    playlist_title = source_title + old_host + separator + self.common.language(30650, True) + quality
                    playlist_source = self.urlresolver.HostedMediaFile(url=playlist_host, title=playlist_title.upper())
                    if playlist_source:
                        playlist_list.extend([playlist_source])
            else:
                if item['src_title']: source_title = item['src_title'] + separator
                source_host = host.search(item['url'])
                if source_host: source_host = source_host.group(1)
                else: source_host = 'UID'
                source_title += source_host + quality
                source = self.urlresolver.HostedMediaFile(url=item['url'], title=source_title.upper())
                if source:
                    full_list.extend([source])
        full_list.extend(playlist_list)
        source_list.extend(full_list)
        source_list.extend(part_list)
        return [source_list, full_list]

    def _sort_sources(self, dict_list):
        usehd = self.common.usehd()
        autoplay = self.common.autoplay()
        hd = []
        hq = []
        sd = []
        lq = []
        new_dict_list = []
        for item in dict_list:
            source = True
            if item['multi-part']:
                item['url'] = 'playlist://' + item['parts'][0]
            if source:
                quality = item.get('src_quality', 'sd')
                if quality.lower() == 'hd': hd.extend([item])
                elif quality.lower() == 'hq': hq.extend([item])
                elif quality.lower() == 'sd': sd.extend([item])
                elif quality.lower() == 'lq': lq.extend([item])
        if (autoplay and usehd) or not autoplay:
            new_dict_list.extend(hd)
        new_dict_list.extend(hq)
        new_dict_list.extend(sd)
        new_dict_list.extend(lq)
        if autoplay and not usehd:
            new_dict_list.extend(hd)
        return new_dict_list

    def choose_sources(self, dict_list):
        if not isinstance(dict_list, list): raise TypeError
        for item in dict_list:
            try: item.keys()
            except: raise TypeError
        autoplay = self.common.autoplay()
        edit_url = self.common.editurl()
        dict_list = self._sort_sources(dict_list)
        if not dict_list:
            self.common.alert(self.common.language(30905, True), sound=False)
            return
        lists = self._create_source_list(dict_list)
        source_list = lists[0]
        full_list = lists[1]
        chosen = None
        img = dict_list[-1].get('cover_url', '')
        if (self.common.theme_path in img) or (self.common.media_path in img):
            img = ''
        thumb = dict_list[-1].get('thumb_url', None)
        if thumb:
            if (self.common.theme_path in thumb) or (self.common.media_path in thumb):
               img = thumb
        title = dict_list[-1].get('title', '')
        found = False
        if len(dict_list) == 1:
            stream_url = source_list[0].resolve()
            if stream_url:
                found = True
                self.play_this(stream_url, dict_list[0].get('title', ''), dict_list[0].get('cover_url', ''), self.common.usedirsources(), dict_list[0])
        elif autoplay and full_list:
            for index, chosen in enumerate(full_list):
                stream_url = chosen.resolve()
                if stream_url:
                    if not stream_url.startswith('playlist://'):
                        if edit_url: stream_url = self.addon.edit_input(stream_url)
                        found = True
                        playback_item = xbmcgui.ListItem(label=title, thumbnailImage=img, path=stream_url)
                        playback_item.setProperty('IsPlayable', 'true')
                        xbmcplugin.setResolvedUrl(self.common.handle, True, playback_item)
                        break
                    else:
                        list_index = re.search('^playlist://[a-zA-Z0-9_]+?/([0-9]+?)/$', stream_url)
                        if list_index:
                            found = True
                            self.play_list(dict_list[int(list_index.group(1))], title, img)
                            break
        elif source_list:
                if self.common.usedirsources():
                    found = True
                    self._directory_sources(source_list, dict_list)
                else:
                    chosen = self._dialog_sources(source_list)
                    if chosen:
                        idx = None
                        stream_url = chosen.resolve()
                        if stream_url:
                            if not stream_url.startswith('playlist://'):
                                if edit_url: stream_url = self.addon.edit_input(stream_url)
                                part_title = re.search('.+?(\s[Pp][Aa][Rr][Tt]\s[0-9]+)', chosen.title)
                                if part_title:
                                    title += part_title.group(1)
                                playback_item = xbmcgui.ListItem(label=title, thumbnailImage=img, path=stream_url)
                                playback_item.setProperty('IsPlayable', 'true')
                                found = True
                                xbmcplugin.setResolvedUrl(self.common.handle, True, playback_item)
                            else:
                                list_index = re.search('^playlist://[a-zA-Z0-9_]+?/([0-9]+?)/$', stream_url)
                                if list_index:
                                    found = True
                                    self.play_list(dict_list[int(list_index.group(1))], title, img)
        if not found:
            try:
                failmsg = str(stream_url.msg)
            except:
                failmsg = self.common.language(30905, True)
            else:
                self.common.alert(failmsg, self.common.language(30923, True))


    def play_list(self, source, title='', image=''):
        try: source.keys()
        except: raise TypeError

        if source['multi-part']:
            all_resolved = True
            playlist_item = self.addon.get_playlist(1, True)
            first_item = None
            try:
                source['parts'] = ast.literal_eval(source['parts'])
            except:
                pass
            for index, part in enumerate(source['parts']):
                this_title = title
                src_title = source['title'] + ' ' + self.common.language(30651, True) + ' ' + str(index + 1)
                if this_title:
                    this_title += ' ' + self.common.language(30651, True) + ' ' + str(index + 1)
                else:
                    this_title = src_title
                stream_url = None
                hmf = self.urlresolver.HostedMediaFile(url=part, title=src_title)
                if hmf:
                    stream_url = hmf.resolve()
                if stream_url:
                    playback_item = \
                        xbmcgui.ListItem(label=this_title, thumbnailImage=image,
                                         path=stream_url)
                    playback_item.setProperty('IsPlayable', 'true')
                    if not first_item: first_item = playback_item
                    playlist_item.add(stream_url, playback_item)
                else:
                    amsg = '%s %s %s' % (self.common.language(30991, True), str(index + 1), self.common.language(30922, True))
                    self.common.alert(amsg, self.common.language(30921, True))
                    all_resolved = False
                    break
            if all_resolved and first_item:
                xbmcplugin.setResolvedUrl(self.common.handle, True, first_item)

    def play_this(self, item, title='', image='', with_player=True, meta_dict=None):
        if not isinstance(item, str):
            try: item = str(item)
            except: return
        source = self.urlresolver.HostedMediaFile(url=item, title=title)
        stream_url = source.resolve()
        if not stream_url:
            try:
                failmsg = str(stream_url.msg)
            except:
                failmsg = self.common.language(30905, True)
            else:
                self.common.alert(failmsg, self.common.language(30923, True))
            finally:
                stream_url = item
        if stream_url:
            multipart = False
            if meta_dict:
                multipart = meta_dict.get('multi-part', False)
                if multipart:
                    if 'playlist://' not in item:
                        multipart = False
            if multipart:
                self.play_list(meta_dict, title, image)
            else:
                playback_item = xbmcgui.ListItem(label=title, thumbnailImage=image, path=stream_url)
                playback_item.setProperty('IsPlayable', 'true')
                if with_player:
                    core = self.common.player_core()
                    xbmc.Player(core).play(stream_url, playback_item)
                else:
                    xbmcplugin.setResolvedUrl(self.common.handle, True, playback_item)

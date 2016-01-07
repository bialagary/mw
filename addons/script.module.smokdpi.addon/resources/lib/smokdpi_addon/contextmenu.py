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


import common
from addondict import AddonDict


class ContextMenu:

    def __init__(self, context, params):
        if not isinstance(context, int):
            try: context = int(context)
            except: context = 3
        if not isinstance(params, dict) and not isinstance(params, AddonDict): return
        site = params.setdefault('site', None)
        if not site: return
        if not isinstance(site, str):
            try: site = str(site)
            except: return
        sub_site = params.setdefault('sub_site', '')
        if not isinstance(sub_site, str):
            try: sub_site = str(sub_site)
            except: sub_site = ''
        mode = params.setdefault('mode', 'main')
        if not isinstance(mode, str):
            try: mode = str(mode)
            except: mode = ''
        content = params.setdefault('content', '')
        if not isinstance(content, str):
            try: content = str(content)
            except: content = ''
        self.content = content
        self.site = site
        self.sub_site = sub_site
        self.context = context
        self.params = params
        self.mode = mode
        self.common = common

    def add_favorite(self):
        title = self.common.addon_name + ' - ' + self.common.language(30882, True) + ' ' + self.common.language(30893, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'favorites',
                                                                             'mode': 'add_favorite',
                                                                             '__params_': self.params}))]

    def delete_favorite(self):
        title = self.common.language(30883, True) + ' ' + self.common.language(30894, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'favorites',
                                                                             'mode': 'delete_favorite',
                                                                             '__params_': self.params}))]

    def clear_favorites(self):
        title = self.common.language(30895, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'favorites',
                                                                             'mode': 'clear_favorites',
                                                                             'sub_site': self.sub_site}))]

    def clear_history(self):
        title = self.common.language(30879, True)
        return [(title,
                 'XBMC.RunPlugin(%s)' %
                 self.common.build_plugin_url({'site': 'history', 'mode': 'clear_history', 'sub_site': self.sub_site}))]

    def clear_search(self):
        for_site = self.params.get('sub_site')
        if not for_site: for_site = self.site
        title = self.common.language(30876, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'clear_search',
                                                                             'sub_site': for_site}))]

    def refresh_container(self):
        title = self.common.language(30600, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'refresh'}))]

    def show_information(self):
        title = self.common.language(30601, True)
        return [(title, 'XBMC.Action(Info)')]

    def show_settings(self):
        title = self.common.language(30602, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'show_settings'}))]

    def play(self):
        title = self.common.language(30603, True)
        return [(title, 'XBMC.Action(Play)')]

    def set_view(self):
        title = self.common.language(30604, True)
        return [(title, 'XBMC.RunPlugin(%s)' % self.common.build_plugin_url({'site': 'set_view_mode',
                                                                             'content': self.content}))]

    def menu(self):
        the_menu = []
        if self.context == 3:
            if self.content.lower() == 'search':
                the_menu.extend(self.clear_search())
            if self.site.lower() == 'favorites':
                the_menu.extend(self.clear_favorites())
            if self.site.lower() == 'history':
                the_menu.extend(self.clear_history())
            # the_menu.extend(self.show_settings())
        else:
            # if self.mode.lower() == 'play':
            #     the_menu.extend(self.play())
            if self.context == 4:
                the_menu.extend(self.delete_favorite())
                the_menu.extend(self.clear_favorites())
            if self.context != 4:
                the_menu.extend(self.add_favorite())
                the_menu.extend(self.set_view())
            the_menu.extend(self.show_information())
            the_menu.extend(self.refresh_container())
            # the_menu.extend(self.show_settings())
        return the_menu

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


import os
import sys
import re
from addon import Addon


addon = Addon()
common = addon.common

common.create_tables()

sys.path.append(common.module_path)
sys.path.append(common.site_path)

params = addon.queries
param = params.get('site', 'main')
context = params.get('context', 3)

is_allowed_access = common.disclaim()


if is_allowed_access:
    if common.history_size_limit() != 0:
        if 2 >= int(context) >= 0:
            addon.add_history()
    if param == 'main':
        is_allowed_access = False
        if common.is_locked():
            is_allowed_access = common.toggle_lock()
        else: is_allowed_access = True

        if is_allowed_access:

            sites = []
            item_list = []
            site_list = []

            for _file in os.listdir(common.site_path):
                if os.path.isfile(os.path.join(common.site_path, _file)):
                    site = re.search('^([a-zA-Z0-9]+[a-zA-Z0-9_\-]+)\.py$', _file)
                    if site:
                        sites.extend([site.groups()[0]])
            if sites:
                if len(sites) == 1:
                    try:
                        i = __import__(sites[0], fromlist=[''])
                        i.Site(params)
                    except ImportError: common.error(common.language(30907, True) + ' ' + common.addon_name)
                elif len(sites) > 1:
                    for site in sites:
                        try:
                            i = __import__(site, fromlist=[''])
                            if i:
                                order = 999
                                try:
                                    if i.order:
                                        if not isinstance(i.order, int):
                                            try: order = int(i.order)
                                            except: order = 999
                                        else: order = i.order
                                except: pass
                                if not i.image: i.image = str(site) + '-icon.png'
                                if not i.art: i.art = str(site) + '-fanart.jpg'
                                item_list.append((order, {'mode': 'main', 'title': i.title, 'content': '',
                                                          'site': site, 'cover_url': common.image(i.image),
                                                          'backdrop_url': common.art(i.art), 'type': 3}))
                        except: pass
                    if item_list:
                        item_list = sorted(item_list, key=lambda item: item[0])
                        for item in item_list:
                            site_list.extend([item[1]])
                    if site_list:
                        site_list.extend(addon.extended_menu())
                        addon.add_items(site_list)
                        addon.end_of_directory()
                    else:
                        common.error(common.language(30907, True) + ' ' + common.addon_name)
    elif param == 'set_view_mode':
        common.set_view_mode_db(params['content'])
    elif param == 'refresh':
        common.container_refresh()
    elif param == 'show_information':
        common.show_information(params['type'])
    elif param == 'show_settings':
        common.show_settings()
    elif param == 'author':
        try:
            addon.add_items(addon.author_links_menu())
            addon.end_of_directory()
        except:
            common.noop()
    elif param == 'execute':
        common.execute(params['url'])
    elif param == 'lock_password':
        try: common.change_password()
        except: common.alert(common.language(30908, True))
    elif param == 'lock_toggle':
        try: common.toggle_lock()
        except: common.alert(common.language(30908, True))
    elif param == 'clear_cookies':
        try: common.clear_cookies()
        except: common.alert(common.language(30914, True))
    elif param == 'clear_cache':
        try: common.clear_cache()
        except: common.alert(common.language(30916, True))
    elif param == 'clear_search':
        try: common.clear_search(params['sub_site'])
        except: common.alert(common.language(30920, True))
    elif param == 'separator':
        pass
    elif param == 'play_this':
        from playback import Playback
        Playback().play_this(params.get('url', ''), params['title'], common.image(params.get('cover_url', '')), False, params)
    else:
        is_allowed_access = False
        if common.is_locked():
            is_allowed_access = common.toggle_lock()
        else: is_allowed_access = True
        if is_allowed_access:
            try:
                i = __import__(param, fromlist=[''])
                i.Site(params)
            except ImportError: common.error(common.language(30907, True) + ' ' + param)

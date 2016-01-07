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


    <string id="30882">Add</string>
    <string id="30883">Delete</string>
    <string id="30884">All</string>
    <string id="30885">Movies</string>
    <string id="30886">Shows</string>
    <string id="30887">Seasons</string>
    <string id="30888">Episodes</string>
    <string id="30889">Favorites</string>
    <string id="30890">already in favorites</string>
    <string id="30891">Added</string>
    <string id="30892">Removed</string>
    <string id="30893">to favorites</string>
    <string id="30894">from favorites</string>
    <string id="30895">Clear Favorites</string>
    <string id="30896">Are you sure you would like to delete all your favorites?</string>
    <string id="30897">Favorites have been cleared</string>
    <string id="30898">Yes</string>
    <string id="30899">No</string>
"""


import xbmc
import xbmcgui
from addon import Addon
from addondict import AddonDict


class Site:

    def __init__(self, params):
        site = self.__module__
        addon = Addon()
        common = addon.common
        mode = params['mode']
        common.update_favorites_db()

        if mode == 'main':
            __item_list_ = [{'site': site, 'mode': 'list_favorites', 'title': addon.language(30884, True), 'content': 'all',
                             'sub_site': params['sub_site'], 'cover_url': addon.image('all.png'), 'backdrop_url': addon.art(), 'type': 3},
                            {'site': site, 'mode': 'list_favorites', 'title': addon.language(30885, True), 'content': 'movies',
                             'sub_site': params['sub_site'], 'cover_url': addon.image('movies.png'), 'backdrop_url': addon.art(), 'type': 3},
                            {'site': site, 'mode': 'list_favorites', 'title': addon.language(30886, True), 'content': 'tvshows',
                             'sub_site': params['sub_site'], 'cover_url': addon.image('tvshows.png'), 'backdrop_url': addon.art(), 'type': 3},
                            {'site': site, 'mode': 'list_favorites', 'title': addon.language(30888, True), 'content': 'episodes',
                             'sub_site': params['sub_site'], 'cover_url': addon.image('scenes.png'), 'backdrop_url': addon.art(), 'type': 3}]

            addon.add_items(__item_list_)
            addon.end_of_directory()

        elif mode == 'add_favorite':
            params = AddonDict(common.addon_type()).str_update(params['__params_'])
            execute = 'INSERT INTO ' + common.fav_db_table + ' (sub_site, content, url, __params_) VALUES (?, ?, ?, ?)'
            inserted = common.db.execute(execute, (params['sub_site'], params['content'], params['url'], str(params)))
            if common.to_bool(inserted):
                if inserted == 1:
                    addon.alert(str(addon.language(30891, True) + ' ' + params['title'].decode('ascii', 'ignore') + ' ' + addon.language(30893, True)))
                if inserted == 2:
                    addon.alert(str(params['title'].decode('ascii', 'ignore') + ' ' + addon.language(30890, True)))

        elif mode == 'delete_favorite':
            params = AddonDict(common.addon_type()).str_update(params['__params_'])
            execute = 'DELETE FROM ' + common.fav_db_table + ' WHERE sub_site=? AND content=? AND url=?'
            deleted = common.db.execute(execute, (params['sub_site'], params['content'], params['url']))
            if common.to_bool(deleted):
                addon.alert(str(addon.language(30892, True) + ' ' + params['title'].decode('ascii', 'ignore') + ' ' + addon.language(30894, True)))
                xbmc.executebuiltin('Container.Refresh')

        elif mode == 'list_favorites':
            if params['content'] == 'all':
                sql_params = (params['sub_site'],)
                execute = 'SELECT * FROM ' + common.fav_db_table + ' WHERE sub_site=?'
            else:
                sql_params = (params['sub_site'], params['content'])
                execute = 'SELECT * FROM ' + common.fav_db_table + ' WHERE sub_site=? AND content=?'
            selected = common.db.fetchall(execute, sql_params)
            item_list = []
            if selected:
                for this_id, site, content, url, params in selected:
                    params = AddonDict(common.addon_type()).str_update(params)
                    params['context'] = 4
                    item_list.extend([params])
            if item_list:
                addon.add_items(item_list)
            addon.end_of_directory()

        elif mode == 'clear_favorites':
            """
            Prompt user for confirmation prior to clearing all favorites / removing favorites table
            """
            if not params['sub_site']:
                execute = 'DROP TABLE ' + common.fav_db_table
                sql_params = ''
            else:
                execute = 'DELETE FROM ' + common.fav_db_table + ' WHERE sub_site=?'
                sql_params = (params['sub_site'],)
            clear_favs = xbmcgui.Dialog().yesno(
                common.addon_name + ' - ' + addon.language(30895, True), ' ', addon.language(30896, True),
                nolabel=addon.language(30899, True), yeslabel=addon.language(30898, True))
            if common.to_bool(clear_favs):
                cleared = common.db.execute(execute, sql_params)
                if common.to_bool(cleared):
                    common.db.execute('VACUUM ' + common.fav_db_table)
                    addon.alert(str(addon.language(30897, True)))
                    xbmc.executebuiltin('Container.Refresh')

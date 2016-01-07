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


    <string id="30875">History</string>
    <string id="30876">Clear search history</string>
    <string id="30877">Are you sure you would like to delete your search history?</string>
    <string id="30878">Search history has been cleared</string>
    <string id="30879">Clear history</string>
    <string id="30880">Are you sure you would like to delete your history?</string>
    <string id="30881">History has been cleared</string>
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

        if mode == 'main':

            sql_params = (params['sub_site'],)
            execute = 'SELECT * FROM ' + common.hist_db_table + ' WHERE sub_site=? ORDER BY id DESC'
            selected = common.db.fetchall(execute, sql_params)
            item_list = []
            if selected:
                for this_id, site, content, url, params in selected:
                    try:
                        params = AddonDict(common.addon_type()).str_update(params)
                        item_list.extend([params])
                    except:
                        pass
            if item_list:
                addon.add_items(item_list)
            addon.end_of_directory()

        elif mode == 'clear_history':
            if not params['sub_site']:
                execute = 'DROP TABLE ' + common.hist_db_table
                sql_params = ''
            else:
                execute = 'DELETE FROM ' + common.hist_db_table + ' WHERE sub_site=?'
                sql_params = (params['sub_site'],)
            clear_hist = xbmcgui.Dialog().yesno(
                common.addon_name + ' - ' + addon.language(30879, True), ' ', addon.language(30880, True),
                nolabel=addon.language(30899, True), yeslabel=addon.language(30898, True))
            if common.to_bool(clear_hist):
                cleared = common.db.execute(execute, sql_params)
                if common.to_bool(cleared):
                    common.db.execute('VACUUM ' + common.hist_db_table)
                    addon.alert(str(addon.language(30881, True)))
                    xbmc.executebuiltin('Container.Refresh')
                else:
                    addon.alert(str(addon.language(30919, True)))
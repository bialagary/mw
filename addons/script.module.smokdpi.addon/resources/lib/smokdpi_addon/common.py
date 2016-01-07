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
from BeautifulSoup import BeautifulSoup
import urlparse
import datetime
import time
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
from database import SQLite
import __config__
from net import Net
import socket
import traceback


def log(msg, level=xbmc.LOGNOTICE):
    """
    Writes a string to the XBMC log file. The addon name is inserted into
    the beginning of the message automatically to help you find relevent
    messages in the log file.

    The available log levels are defined in the :mod:`xbmc` module and are
    currently as follows::

        xbmc.LOGDEBUG = 0
        xbmc.LOGERROR = 4
        xbmc.LOGFATAL = 6
        xbmc.LOGINFO = 1
        xbmc.LOGNONE = 7
        xbmc.LOGNOTICE = 2
        xbmc.LOGSEVERE = 5
        xbmc.LOGWARNING = 3

    Args:
        msg (str or unicode): The message to be written to the log file.

    Kwargs:
        level (int): The XBMC log level to write at.
    """
    # msg = unicodedata.normalize('NFKD', unicode(msg)).encode('ascii', 'ignore')
    xbmc.log('%s: %s' % (addon_name, msg), level)


def log_error(msg):
    """
    Convenience method to write to the XBMC log file at the
    ``xbmc.LOGERROR`` error level. Use when something has gone wrong in
    your addon code. This will show up in the log prefixed with 'ERROR:'
    whether you have debugging switched on or not.
    """
    log(msg, xbmc.LOGERROR)


def log_debug(msg):
    """
    Convenience method to write to the XBMC log file at the
    ``xbmc.LOGDEBUG`` error level. Use this when you want to log lots
    of detailed information that is only usefull for debugging. This will
    show up in the log only when debugging is enabled in the XBMC settings,
    and will be prefixed with 'DEBUG:'.
    """
    log(msg, xbmc.LOGDEBUG)


def log_notice(msg):
    """
    Convenience method to write to the XBMC log file at the
    ``xbmc.LOGNOTICE`` error level. Use for general log messages. This will
    show up in the log prefixed with 'NOTICE:' whether you have debugging
    switched on or not.
    """
    log(msg, xbmc.LOGNOTICE)


module_author = __config__.author
module_id = 'script.module.' + module_author + '.addon'
module_theme_id = 'theme.' + module_author + '.default'
resolver_id = 'script.module.' + module_author + '.resolvers'
addon_id = xbmcaddon.Addon().getAddonInfo('id')

thisaddon = xbmcaddon.Addon(addon_id)
thismodule = xbmcaddon.Addon(module_id)

addon_theme_id = thisaddon.getSetting('theme_id')
addon_name = thisaddon.getAddonInfo('name')
addon_author = thisaddon.getAddonInfo('author')
addon_version = thisaddon.getAddonInfo('version')
addon_disclaimer = thisaddon.getAddonInfo('disclaimer')

module_path = xbmc.translatePath(os.path.join(thismodule.getAddonInfo('path'),
                                              'resources', 'lib', module_author + '_addon'))
builtin_resolvers_path = xbmc.translatePath(os.path.join(module_path, 'resolvers'))
media_path = xbmc.translatePath(os.path.join(xbmcaddon.Addon(module_theme_id).getAddonInfo('path'),
                                             'resources', 'media'))
addon_path = xbmc.translatePath(thisaddon.getAddonInfo('path'))
site_path = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib', 'sites'))

addon_xml = xbmc.translatePath(os.path.join(addon_path, 'addon.xml'))

# Profile Paths
addon_profile_path = xbmc.translatePath(os.path.join(xbmc.translatePath('special://profile'), 'addon_data', addon_id))
module_profile_path = xbmc.translatePath(os.path.join(xbmc.translatePath('special://profile'), 'addon_data', module_id))
if not os.path.exists(addon_profile_path):
    try: xbmcvfs.mkdirs(addon_profile_path)
    except: os.mkdir(addon_profile_path)
if not os.path.exists(module_profile_path):
    try: xbmcvfs.mkdirs(module_profile_path)
    except: os.mkdir(module_profile_path)


# Net
cookie_file = xbmc.translatePath(os.path.join(xbmc.translatePath(addon_profile_path), 'cookies.txt'))


def _is_cookie_file(the_file):
    exists = os.path.exists(the_file)
    if not exists:
        return False
    else:
        try:
            tmp = xbmcvfs.File(the_file).read()
            if tmp.startswith('#LWP-Cookies-2.0'):
                return True
            return False
        except:
            with open(the_file, 'r') as f:
                tmp = f.readline()
                if tmp == '#LWP-Cookies-2.0\n':
                    return True
                return False


def _create_cookie(the_file):
    try:
        if xbmcvfs.exists(the_file):
            xbmcvfs.delete(the_file)
        _file = xbmcvfs.File(the_file, 'w')
        _file.write('#LWP-Cookies-2.0\n')
        _file.close()
        return the_file
    except:
        try:
            _file = open(the_file, 'w')
            _file.write('#LWP-Cookies-2.0\n')
            _file.close()
            return the_file
        except:
            return ''


if not _is_cookie_file(cookie_file):
    cookie_file = _create_cookie(cookie_file)


# Database
db_file = xbmc.translatePath(os.path.join(addon_profile_path, 'database.db'))
db = SQLite(db_file)
db_table = 'core_0_0_1'
fav_db_table = 'favorites_0_0_2'
hist_db_table = 'history_0_0_2'
search_db_table = 'search_0_0_2'
play_db_table = 'play_0_0_2'

cache_db_file = xbmc.translatePath(os.path.join(module_profile_path, 'cache.db'))
cache_db = SQLite(cache_db_file)
cache_db_table = 'cache_0_0_1'
sources_db_table = 'sources_0_0_2'

pw_db_file = xbmc.translatePath(os.path.join(addon_profile_path, 'password.db'))
pw_db = SQLite(pw_db_file)
pw_db_table = 'password_0_0_1'


def create_tables():
    list_of_statements = [['CREATE TABLE IF NOT EXISTS ' + db_table + ' (sub_site, setting_name UNIQUE, setting)', ''],
                          ['CREATE TABLE IF NOT EXISTS ' + fav_db_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                                          'sub_site, content, url, __params_, '
                                                                          'CONSTRAINT unq UNIQUE (sub_site, url))', ''],
                          ['CREATE TABLE IF NOT EXISTS ' + hist_db_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                                           'sub_site, content, url, __params_, '
                                                                           'CONSTRAINT unq UNIQUE (sub_site, url))', ''],
                          ['CREATE TABLE IF NOT EXISTS ' + search_db_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                                             'sub_site, query, '
                                                                             'CONSTRAINT unq UNIQUE (sub_site, query))', ''],
                          ['CREATE TABLE IF NOT EXISTS ' + play_db_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                                           'sub_site, url, '
                                                                           'CONSTRAINT unq UNIQUE (sub_site, url))', '']]
    if not db.execute_list(list_of_statements):
        log_error('Failed to create a table in database <\'' + str(db) + '\'>')
        raise Exception
    if not cache_db.execute('CREATE TABLE IF NOT EXISTS ' + cache_db_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                                             'url UNIQUE, timestamp, content)'):
        log_error('Failed to create table <\'' + cache_db_table + '\'> in database <\'' +
                 str(cache_db) + '\'>')
        raise Exception
    if not pw_db.execute('CREATE TABLE IF NOT EXISTS ' + pw_db_table + ' (sub_site UNIQUE, password)'):
        log_error('Failed to create table <\'' + pw_db_table + '\'> in database <\'' + str(pw_db) + '\'>')
        raise Exception


def get_setting(setting_id):
    if not isinstance(setting_id, str):
        try: setting_id = str(setting_id)
        except: return ''
    return thisaddon.getSetting(setting_id)


def set_setting(setting_id, setting_value):
    if not isinstance(setting_id, str):
        try: setting_id = str(setting_id)
        except: return ''
    return thisaddon.setSetting(setting_id, setting_value)


# Icon/Fanart Defaults - Theme
addon_icon = xbmc.translatePath(os.path.join(addon_path, 'icon.png'))
addon_fanart = xbmc.translatePath(os.path.join(addon_path, 'fanart.jpg'))
theme_id_path = ''

if not addon_theme_id or (addon_theme_id.lower() == 'none'):
    has_theme = False
else:
    _tmp = addon_id.rfind('.')
    addon_theme_id = 'theme.' + addon_id[_tmp+1:] + '.' + addon_theme_id.lower().replace(' ', '')
    has_theme = xbmc.getCondVisibility('System.HasAddon(%s)' % addon_theme_id)
    if has_theme:
        theme_id_path = xbmcaddon.Addon(addon_theme_id).getAddonInfo('path')
        theme_path = xbmc.translatePath(os.path.join(theme_id_path,
                                                     'resources', 'media'))
        if not os.path.exists(theme_path):
            has_theme = False

if has_theme:
    icon = xbmc.translatePath(os.path.join(theme_id_path, 'icon.png'))
    fanart = xbmc.translatePath(os.path.join(theme_id_path, 'fanart.jpg'))
else:
    _tmp = set_setting('theme_id', 'None')
    theme_path = xbmc.translatePath(os.path.join(addon_path, 'resources', 'media'))
    icon = addon_icon
    fanart = addon_fanart


# Setup resolver packs
resolvers_path = ''
try:
    resolvers = False
    resolvers_path = xbmc.translatePath(os.path.join(xbmcaddon.Addon(resolver_id).getAddonInfo('path'),
                                                     'resources', 'lib', module_author + '_resolvers'))
    if os.path.exists(resolvers_path):
        resolvers = True
except:
    resolvers = False


# Author links for menu
author_links = []
if __config__.author_links and isinstance(__config__.author_links, list): author_links = __config__.author_links


"""
common functions
"""


def parse_query(this_queries, defaults={'mode': 'main'}):
    """
    Parse a query string as used in a URL or passed to your addon by XBMC.

    Example:

    >>> addon.parse_query('name=test&type=basic')
    {'mode': 'main', 'name': 'test', 'type': 'basic'}

    Args:
        query (str): A query string.

    Kwargs:
        defaults (dict): A dictionary containing key/value pairs parsed
        from the query string. If a key is repeated in the query string
        its value will be a list containing all of that keys values.
    """
    this_queries = urlparse.parse_qs(this_queries)
    q = defaults
    for key, value in this_queries.items():
        if len(value) == 1:
            q[key] = value[0]
        else:
            q[key] = value
    return q


#
url = ''
handle = ''
queries = ''
argv = sys.argv
if argv:
    url = argv[0]
    handle = int(argv[1])
    queries = parse_query(argv[2][1:])
net = Net(cookie_file, cloudflare=True)


def build_plugin_url(this_queries):
    import urllib
    out_dict = {}
    for k, v in this_queries.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf-8')
        out_dict[k] = v
    return url + '?' + urllib.urlencode(out_dict)


def addon_type():
    # Addon Type from addon.xml 'Provides'
    # 0 = video/default, 1 = audio/music, 2 = image/pictures, 3, executable/programs
    _file = open(addon_xml)
    _xml = BeautifulSoup(_file.read())
    _file.close()

    _addon_type = _xml.find('provides').string.lower()
    if 'video' in _addon_type: _addon_type = 0
    elif 'audio' in _addon_type: _addon_type = 1
    elif 'image' in _addon_type: _addon_type = 2
    elif 'executable' in _addon_type: _addon_type = 3
    else: _addon_type = 0
    return _addon_type


def to_bool(value):
    """
    Test value against possible False string statements and bool(); returning Boolean True / False
    :param value: value to test against
    :return: Boolean: True / False
    """
    if isinstance(value, str) and bool(value): return not value.lower() in ('false', '0', '0.0', 'n', 'no', 'off')
    else: return bool(value)


def show_settings():
    """Shows the settings dialog for this addon."""
    thisaddon.openSettings()


def bool_setting(setting_id, inverse=False):
    """
    Get provided setting and return Boolean result
    :param setting_id:  str: add-on setting id from settings.xml
    :param inverse: bool: if True will return inverted result
    :return: bool:  True / False
    """
    if not isinstance(setting_id, str):
        try: setting_id = str(setting_id)
        except: return ''
    if not isinstance(inverse, bool): inverse = False
    setting = get_setting(setting_id)
    if not setting: setting = False
    if inverse:
        return not to_bool(setting)
    return to_bool(setting)


def language(string_id, from_module=False):
    if not isinstance(string_id, int):
        try: string_id = int(string_id)
        except: return ''
    if not isinstance(from_module, bool): from_module = False
    if not from_module:
        return thisaddon.getLocalizedString(string_id).encode('utf-8', 'ignore')
    if from_module:
        return thismodule.getLocalizedString(string_id).encode('utf-8', 'ignore')


def image(use_image='', failover_image=''):
    failover_site = queries.get('sub_site', '')
    if not failover_site: failover_site = queries.get('site', '')
    if not failover_image:
        if failover_site:
            failover_image = failover_site + '-icon.png'
            if not use_image.startswith('http'):
                tmp_image = failover_site + '-' + use_image
                tmp_image = xbmc.translatePath(os.path.join(theme_path, tmp_image))
                if os.path.isfile(tmp_image):
                    failover_image = tmp_image
        else: failover_image = icon
    if not isinstance(failover_image, str):
        try: failover_image = str(failover_image)
        except: failover_image = icon
    if not isinstance(use_image, str):
        try: use_image = str(use_image)
        except: use_image = failover_image
    if use_image:
        if use_image == icon: return icon
        elif use_image.startswith('http'): return net.url_with_headers(use_image)
        elif not use_image.startswith('http'):
            theme_img = xbmc.translatePath(os.path.join(theme_path, use_image))
            if os.path.isfile(theme_img): return theme_img
            use_image = xbmc.translatePath(os.path.join(media_path, use_image))
            if os.path.isfile(use_image): return use_image
    if failover_image.startswith('http'): return net.url_with_headers(failover_image)
    if failover_image != icon:
        theme_failover_image = xbmc.translatePath(os.path.join(theme_path, failover_image))
        if os.path.isfile(theme_failover_image): return theme_failover_image
        failover_image = xbmc.translatePath(os.path.join(media_path, failover_image))
        if not os.path.isfile(failover_image): failover_image = icon
    return failover_image


def art(use_image=''):
    theme_site = queries.get('sub_site', '')
    if not theme_site: theme_site = queries.get('site', '')
    if theme_site:
        theme_art = theme_site + '-fanart.jpg'
        theme_art = xbmc.translatePath(os.path.join(theme_path, theme_art))
        if not os.path.isfile(theme_art): theme_art = fanart
    else: theme_art = fanart
    if not isinstance(use_image, str):
        try: use_image = str(use_image)
        except: pass
    if use_image:
        if use_image == fanart: return fanart
        elif use_image == theme_art: return theme_art
        elif use_image.startswith('http'): return net.url_with_headers(use_image)
    return theme_art


def get_setting_db(setting_name):
    d_execute = 'SELECT * FROM ' + db_table + ' WHERE setting_name=?'
    selected = db.fetchall(d_execute, (setting_name, ))
    if selected:
        return selected[0][2]
    else:
        return ''


def set_setting_db(setting_name, setting_value):
    old_setting_value = get_setting_db(setting_name)
    d_execute = 'INSERT INTO ' + db_table + ' (sub_site, setting_name, setting) VALUES (?, ?, ?)'
    sqlparams = (addon_name, setting_name, setting_value)
    if old_setting_value:
        if setting_value == old_setting_value:
            return True
        else:
            d_execute = 'UPDATE ' + db_table + ' SET setting=? WHERE setting_name=? AND sub_site=?'
            sqlparams = (setting_value, setting_name, addon_name)
    successful = db.execute(d_execute, sqlparams)
    if successful == 1:
        return True
    else:
        return False


def alert(message, title='', use_image='', time=5000, sound=False):
    if not isinstance(message, str): raise TypeError
    if not title or not isinstance(title, str): title = addon_name
    if not use_image or not isinstance(use_image, str): use_image = icon
    if not time or not isinstance(time, int): time = 5000
    if 1000 >= time <= 10000: time = 5000
    try:
        xbmcgui.Dialog().notification(title, message, use_image, time, sound)
    except:
        xbmc.executebuiltin('Notification("%s","%s",%d,"%s")' % (title, message, time, use_image))


def error(message):
    if not isinstance(message, str):
        try: message = str(message)
        except: message = language(30801, True)
    title = language(30800, True)
    if sys.exc_info()[0]:
        exception = re.search('exceptions\.(.+?)\'>', str(sys.exc_info()[0]))
        if exception: title = exception.group(1)
    if not title: title = language(30800, True)
    lasterror = str(traceback.format_exc())
    log_error(lasterror)
    lasterror = set_setting_db('lasterror', lasterror)
    alert(message, addon_name + ' ' + title + ':', image('error.png'), sound=True)
    exit(1)


def container_refresh():
    xbmc.executebuiltin('Container.Refresh')


def update_favorites_db():
    d_execute = "SELECT name FROM sqlite_master WHERE type='table' AND name='favorites_0_0_1'"
    selected = db.fetchall(d_execute)
    if selected:
        d_execute = 'SELECT * FROM favorites_0_0_1'
        selected = db.fetchall(d_execute)
        if selected:
            for item in selected:
                d_execute = 'INSERT INTO ' + fav_db_table + ' (sub_site, content, url, __params_) VALUES (?, ?, ?, ?)'
                inserted = db.execute(d_execute, (item[0], item[1], item[2], str(item[3])))
            d_execute = 'ALTER TABLE favorites_0_0_1 RENAME TO _favorites_old'
            db.execute(d_execute)


def disclaim():
    if not addon_disclaimer: return 1
    d_execute = 'SELECT * FROM ' + db_table + ' WHERE setting_name=?'
    selected = db.fetchall(d_execute, ('disclaimer', ))
    d_execute = 'INSERT INTO ' + db_table + ' (sub_site, setting_name, setting) VALUES (?, ?, ?)'
    sqlparams = (addon_name, 'disclaimer', addon_version)
    if selected:
        if selected[0][2] == addon_version: return 1
        else:
            d_execute = 'UPDATE ' + db_table + ' SET setting=? WHERE setting_name=? AND sub_site=?'
            sqlparams = (addon_version, 'disclaimer', addon_name)
            selected = False
    if not selected:
        check = xbmcgui.Dialog().yesno(addon_name + ' ' + language(30994, True), addon_disclaimer,
                                       nolabel=language(30993, True), yeslabel=language(30992, True))
        if check:
            updated = db.execute(d_execute, sqlparams)
        return check


def action(action_id):
    xbmc.executebuiltin('Action(%s)' % action_id)


def noop():
    action('noop')


def execute(execute_this):
    if not isinstance(execute_this, str):
        try: execute_this = execute_this.encode('UTF-8')
        except:
            try: execute_this = str(execute_this)
            except: return ''
    try: xbmc.executebuiltin('System.Exec(%s)' % execute_this)
    except: noop()


def change_password():
    pw_execute = 'SELECT * FROM ' + pw_db_table + ' WHERE sub_site=?'
    oldpassword = pw_db.fetchall(pw_execute, (addon_name, ))
    if oldpassword == []:
        newpassword = xbmcgui.Dialog().input(language(30813, True), type=xbmcgui.INPUT_PASSWORD)
        if newpassword:
            pw_execute = 'INSERT INTO ' + pw_db_table + ' (sub_site, password) VALUES (?, ?)'
            sqlparams = (addon_name, newpassword)
            updated = pw_db.execute(pw_execute, sqlparams)
            return True
        else: return False
    elif oldpassword:
        oldpassword = oldpassword[0][1]
        temppassword = xbmcgui.Dialog().input(language(30812, True), option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if not temppassword: return False
        import md5
        checkpassword = md5.new(temppassword).hexdigest()
        if checkpassword == oldpassword:
            newpassword = xbmcgui.Dialog().input(language(30813, True), type=xbmcgui.INPUT_PASSWORD)
            if newpassword:
                pw_execute = 'UPDATE ' + pw_db_table + ' SET password=? WHERE sub_site=?'
                sqlparams = (newpassword, addon_name)
                updated = pw_db.execute(pw_execute, sqlparams)
                return True
            else: return False
        else:
            alert(language(30910, True))
            return False
    return False


def check_password(checkpassword):
    pw_execute = 'SELECT * FROM ' + pw_db_table + ' WHERE sub_site=?'
    oldpassword = pw_db.fetchall(pw_execute, (addon_name, ))
    if oldpassword == []: return True
    elif oldpassword:
        oldpassword = oldpassword[0][1]
        if checkpassword == oldpassword: return True
        else: return False
    return False


def toggle_lock():
    pw_execute = 'SELECT * FROM ' + db_table + ' WHERE setting_name=?'
    selected = db.fetchall(pw_execute, ('locked', ))
    if selected:
        pw_execute = 'UPDATE ' + db_table + ' SET setting=? WHERE setting_name=? AND sub_site=?'
        if to_bool(selected[0][2]):
            import md5
            checkpassword = xbmcgui.Dialog().input(language(30814, True), option=xbmcgui.ALPHANUM_HIDE_INPUT)
            if not checkpassword: return False
            checkpassword = md5.new(checkpassword).hexdigest()
            can_toggle = check_password(checkpassword)
            if can_toggle:
                sqlparams = ('false', 'locked', addon_name)
                updated = db.execute(pw_execute, sqlparams)
                alert(language(30723, True))
                return True
            else:
                alert(language(30910, True))
                return False
        else:
            sqlparams = ('true', 'locked', addon_name)
            if has_password():
                updated = db.execute(pw_execute, sqlparams)
                alert(language(30724, True))
                return True
            else:
                if change_password():
                    updated = db.execute(pw_execute, sqlparams)
                    alert(language(30724, True))
                    return True
        return False
    else:
        pw_execute = 'INSERT INTO ' + db_table + ' (sub_site, setting_name, setting) VALUES (?, ?, ?)'
        sqlparams = (addon_name, 'locked', 'true')
        if has_password():
            updated = db.execute(pw_execute, sqlparams)
            alert(language(30724, True))
            return True
        else:
            if change_password():
                updated = db.execute(pw_execute, sqlparams)
                alert(language(30724, True))
                return True
        return False


def is_locked():
    pw_execute = 'SELECT * FROM ' + db_table + ' WHERE setting_name=?'
    selected = db.fetchall(pw_execute, ('locked', ))
    if selected == []: return False
    else: return to_bool(selected[0][2])


def has_password():
    pw_execute = 'SELECT * FROM ' + pw_db_table + ' WHERE sub_site=?'
    oldpassword = pw_db.fetchall(pw_execute, (addon_name, ))
    if oldpassword == []: return False
    else: return True


def clear_cookies():
    if cookie_file:
        cleared = _create_cookie(cookie_file)
        if cleared:
            alert(language(30915, True))
        else:
            error(language(30914, True))


def player_core():
    # id: player / values: AUTO|DVDPLAYER|MPLAYER|PAPLAYER / result: core
    player = get_setting('player')
    core = xbmc.PLAYER_CORE_AUTO
    if player == 'DVDPLAYER': core = xbmc.PLAYER_CORE_DVDPLAYER
    elif player == 'MPLAYER': core = xbmc.PLAYER_CORE_MPLAYER
    elif player == 'PAPLAYER': core = xbmc.PLAYER_CORE_PAPLAYER
    return core


def socket_timeout():
    timeout = get_setting('sockettimeout')
    if not timeout: return 60
    if not isinstance(timeout, int):
        try: timeout = int(timeout)
        except: return 60
    return timeout


def cache_expiry():
    expiry = get_setting('cacheexpiry')
    if not expiry: return 7
    if not isinstance(expiry, int):
        try: expiry = int(expiry)
        except: return 7
    return expiry


def cache_size_limit():
    cachesizelimit = get_setting('cachesizelimit')
    if not cachesizelimit: return 5
    if not isinstance(cachesizelimit, int):
        try: cachesizelimit = int(cachesizelimit)
        except: return 5
    return cachesizelimit


def uses_cache():
    expires = cache_expiry()
    if (expires == 0) or not expires: return False
    sizelimit = cache_size_limit()
    if (sizelimit == 0) or not sizelimit: return False
    return True


def clear_cache():
    cache_execute = 'DROP TABLE ' + cache_db_table
    sql_params = ''
    cleared_cache = xbmcgui.Dialog().yesno(
        addon_name + ' - ' + language(30729, True), ' ', language(30918, True),
        nolabel=language(30899, True), yeslabel=language(30898, True))
    if to_bool(cleared_cache):
        cleared = cache_db.execute(cache_execute, sql_params)
        if to_bool(cleared):
            cache_db.execute('VACUUM ' + cache_db_table)
            alert(language(30917, True))
        else:
            alert(language(30916, True))


def trim_cache_file():
    # Check cache file size against limit
    if os.path.exists(cache_db_file):
        _fsize = os.path.getsize(cache_db_file)
        _fsize /= float(1<<20)
        _fsize = float(format(_fsize, '.2f'))
        if _fsize >= cache_size_limit():
            try:
                _cache_execute = 'SELECT COUNT(*) FROM ' + cache_db_table
                _cache_result = cache_db.fetchall(_cache_execute)[0][0]
                _cache_result = str(int(_cache_result) / 2)
                _cache_execute = 'DELETE FROM ' + cache_db_table + ' WHERE id IN (SELECT id FROM ' + cache_db_table + \
                                 ' ORDER BY id ASC LIMIT ' + _cache_result + ')'
                _cache_result = cache_db.execute(_cache_execute)
                if _cache_result == 1:
                    _cache_execute = 'VACUUM ' + cache_db_table
                    _cache_result = cache_db.execute(_cache_execute)
                else:
                    raise Exception
            except:
                try:
                    _cache_execute = 'DROP TABLE ' + cache_db_table
                    _cache_result = cache_db.execute(_cache_execute)
                    if _cache_result == 1:
                        _cache_execute = 'VACUUM ' + cache_db_table
                        _cache_result = cache_db.execute(_cache_execute)
                    raise Exception
                except:
                    os.remove(cache_db_file)


def diff_in_minutes(datetime_ref):
    fmt = '%Y-%m-%d %H:%M:%S'
    try:
        datetime_ref = datetime.datetime.strptime(datetime_ref, fmt)
    except TypeError:
        datetime_ref = datetime.datetime(*(time.strptime(datetime_ref, fmt)[0:6]))
    datetime_now = datetime.datetime.now()
    datetime_ref = time.mktime(datetime_ref.timetuple())
    datetime_now = time.mktime(datetime_now.timetuple())
    return int(datetime_now - datetime_ref) / 60


def check_cache_expired(cache_url):
    expiry = cache_expiry()
    cache_content = ''
    cache_execute = 'SELECT * FROM ' + cache_db_table + ' WHERE url=?'
    selected = cache_db.fetchall(cache_execute, (cache_url, ))
    if selected:
        for this_id, this_url, this_stamp, this_content in selected:
            if diff_in_minutes(this_stamp) < expiry:
                cache_content = this_content
    return cache_content


def add_to_cache(cache_url, cache_content):
    cache_execute = 'SELECT * FROM ' + cache_db_table + ' WHERE url=?'
    selected = cache_db.fetchall(cache_execute, (cache_url, ))
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if selected:
        cache_execute = 'UPDATE ' + cache_db_table + ' SET timestamp=?, content=? WHERE url=?'
        inserted = cache_db.execute(cache_execute, (timestamp, cache_content, cache_url))
    else:
        cache_execute = 'INSERT INTO ' + cache_db_table + ' (url, timestamp, content) VALUES ( ?, ?, ?)'
        inserted = cache_db.execute(cache_execute, (cache_url, timestamp, cache_content))
    trim_cache_file()


def set_view_mode_db(content):
    skin_path = xbmc.translatePath('special://skin/')
    file_path = xbmc.translatePath(os.path.join(skin_path, 'addon.xml'))
    exists = os.path.isfile(file_path)
    if exists:
        _file = open(file_path)
        xml = BeautifulSoup(_file.read())
        _file.close()
        tag = xml.findAll('res', {'folder': True})
        if tag:
            file_path = xbmc.translatePath(os.path.join(skin_path, tag[0].get('folder'), 'MyVideoNav.xml'))
            exists = os.path.isfile(file_path)
            if exists:
                _file = open(file_path)
                xml = BeautifulSoup(_file.read())
                _file.close()
                tag = xml.find('views')
                if tag:
                    views = tag.string.split(',')
                    viewid = None
                    for view in views:
                        viewlabel = xbmc.getInfoLabel('Control.GetLabel(%s)' % view)
                        if viewlabel != '':
                            viewid = view
                            break
                    if viewid and content:
                        if 'movie' in content:
                            set_setting_db('movie_view', viewid)
                        elif ('tvshow' in content) or ('season' in content):
                            set_setting_db('tvshow_view', viewid)
                        elif 'episode' in content:
                            set_setting_db('episode_view', viewid)
                        viewlabel = xbmc.getInfoLabel('Container.Viewmode')
                        alert(language(30604, True) + ' | ' + content.capitalize().replace('Tvs', 'TVS') + ' | ' + viewlabel, addon_name)


def set_view(view_id):
    xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view_id))


def clear_search(sub_site):
    if not sub_site:
        search_execute = 'DROP TABLE ' + search_db_table
        sql_params = ''
    else:
        search_execute = 'DELETE FROM ' + search_db_table + ' WHERE sub_site=?'
        sql_params = (sub_site,)
    cleared_search = xbmcgui.Dialog().yesno(
        addon_name + ' - ' + language(30876, True), ' ', language(30877, True),
        nolabel=language(30899, True), yeslabel=language(30898, True))
    if to_bool(cleared_search):
        cleared = db.execute(search_execute, sql_params)
        if to_bool(cleared):
            db.execute('VACUUM ' + search_db_table)
            alert(language(30878, True))
        else:
            alert(language(30920, True))


def clear_play_history(sub_site):
    if not sub_site:
        play_execute = 'DROP TABLE ' + play_db_table
        sql_params = ''
    else:
        play_execute = 'DELETE FROM ' + play_db_table + ' WHERE sub_site=?'
        sql_params = (sub_site,)
    cleared = db.execute(play_execute, sql_params)
    if to_bool(cleared):
        db.execute('VACUUM ' + play_db_table)


def autoplay():
    return bool_setting('autoplay')


def editurl():
    return bool_setting('editurl')


def usehd():
    return bool_setting('usehd')


def preresolve():
    return bool_setting('preresolve')


def usedirsources():
    tmp = get_setting('sourcelisttype')
    if isinstance(tmp, str):
        if tmp.lower() == 'directory':
            return True
    return False


def return_limit(settingid):
    limit = get_setting(settingid)
    if not limit: return 0
    if not isinstance(limit, int):
        try: limit = int(limit)
        except: return 0
    return limit


def history_size_limit():
    return return_limit('historysizelimit')


def search_history_size_limit():
    return return_limit('searchsizelimit')


def play_history_size_limit():
    return return_limit('playsizelimit')


socket.setdefaulttimeout(socket_timeout())

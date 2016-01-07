# -*- coding: utf-8 -*-

'''
    Ororo TV XBMC Addon
    Copyright (C) 2014 lambda

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
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers
from resources.lib.libraries import client


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
offData             = os.path.join(dataPath,'offset.cfg')
subData             = os.path.join(dataPath,'subscriptions2.cfg')
favData             = os.path.join(dataPath,'favourites2.cfg')
user                = getSetting("user")
password            = getSetting("password")



class main:
    def __init__(self):
        global action, content_type
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        page = urllib.unquote_plus(params["page"])
        except:     page = 1
        try:        content_type = urllib.unquote_plus(params["content_type"])
        except:     content_type = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None

        if action == None:                          root().get()
        elif action == 'root_movies':               root().get("movies")
        elif action == 'root_shows':                root().get("shows")
        elif action == 'root_search':               root().search()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb, year)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb, year)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'view_seasons':              contextMenu().view('seasons')
        elif action == 'view_episodes':             contextMenu().view('episodes')
        elif action == 'metadata_tvshows':          contextMenu().metadata('tvshow', name, url, imdb, '', '')
        elif action == 'metadata_tvshows2':         contextMenu().metadata2('tvshow', imdb, '', '')
        elif action == 'metadata_movies2':          contextMenu().metadata2('movie', imdb, '', '')
        elif action == 'metadata_seasons':          contextMenu().metadata2('season', imdb, season, '')
        elif action == 'metadata_episodes':         contextMenu().metadata2('episode', imdb, season, episode)
        elif action == 'playcount_tvshows':         contextMenu().playcount('tvshow', imdb, '', '')
        elif action == 'playcount_seasons':         contextMenu().playcount('season', imdb, season, '')
        elif action == 'playcount_episodes':        contextMenu().playcount('episode', imdb, season, episode)
        elif action == 'library_add':               contextMenu().library_add(name, url, image, imdb, year)
        elif action == 'library_from_search':       contextMenu().library_from_search(name, url, image, imdb, year)
        elif action == 'library_delete':            contextMenu().library_delete(name, url)
        elif action == 'library_update':            contextMenu().library_update()
        elif action == 'library_service':           contextMenu().library_update(silent=True)
        elif action == 'download':                  contextMenu().download(name, url)
        elif action == 'shows_favourites':          favourites().shows()
        elif action == 'shows_subscriptions':       subscriptions().shows()
        elif action == 'shows':                     shows().genre(url)
        elif action == 'movies':                    movies().genre(url, page)
        elif action == 'movies_title':              movies().title(page)
        elif action == 'movies_added':              movies().added(page)
        elif action == 'movies_release':            movies().release(page)
        elif action == 'movies_rating':             movies().rating(page)
        elif action == 'movies_search':             movies().search(page, query)
        elif action == 'genres_movies':             genres().get("movies")
        elif action == 'shows_title':               shows().title()
        elif action == 'shows_release':             shows().release()
        elif action == 'shows_rating':              shows().rating()
        elif action == 'shows_search':              shows().search(query)
        elif action == 'genres_shows':              genres().get("shows")
        elif action == 'seasons':                   seasons().get(url, image, year, imdb, genre, plot, show)
        elif action == 'episodes':                  episodes().get(name, url, image, year, imdb, genre, plot, show)
        elif action == 'play':                      resolver().run(url, name, content_type)
        elif action == 'clear_cache':               index().clearCache()

        if action is None:
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('seasons'):
            xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
            index().container_view('seasons', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})    
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.PseudoTVRunning = index().getProperty('PseudoTVRunning')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, name, url, imdb='0'):
        self.video_info(name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or self.PseudoTVRunning == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                file = self.name + '.strm'
                file = file.translate(None, '\/:*?"<>|')
                if content_type == "movies":
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "genre", "year", "rating", "director", "trailer", "tagline", "plot", "plotoutline", "originaltitle", "lastplayed", "playcount", "writer", "studio", "mpaa", "country", "imdbnumber", "runtime", "votes", "fanart", "thumbnail", "file", "sorttitle", "resume", "dateadded"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['movies']
                    self.meta = [i for i in meta if i['file'].endswith(file)][0]
                    meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(self.meta['genre']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'country': str(self.meta['country']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'duration': self.meta['runtime'], 'trailer': self.meta['trailer'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'studio': str(self.meta['studio']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'tagline': self.meta['tagline'], 'plotoutline': self.meta['plotoutline'], 'plot': self.meta['plot']}
                    poster = self.meta['thumbnail']
                    
                else:
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "plot", "votes", "rating", "writer", "firstaired", "playcount", "runtime", "director", "productioncode", "season", "episode", "originaltitle", "showtitle", "lastplayed", "fanart", "thumbnail", "file", "resume", "tvshowid", "dateadded", "uniqueid"]}, "id": 1}' % (self.season, self.episode))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['episodes']
                    self.meta = [i for i in meta if i['file'].endswith(file)][0]
                    meta = {'title': self.meta['title'], 'tvshowtitle': self.meta['showtitle'], 'season': self.meta['season'], 'episode': self.meta['episode'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'duration': self.meta['runtime'], 'premiered': self.meta['firstaired'], 'plot': self.meta['plot']}
                    poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, name, imdb):
        if content_type == "movies":
            self.name = name
            self.content = 'movie'
            self.title = self.name.rsplit(' (', 1)[0].strip()
            self.year = '%04d' % int(self.name.rsplit(' (', 1)[-1].split(')')[0])
            if imdb == '0': imdb = metaget.get_meta('movie', self.title, year=str(self.year))['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.subtitle = subtitles().get(self.name, self.imdb, '', '')
        else:
            self.name = name
            self.content = 'episode'
            self.show = self.name.rsplit(' ', 1)[0]
            if imdb == '0': imdb = metaget.get_meta('tvshow', self.show)['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.season = '%01d' % int(name.rsplit(' ', 1)[-1].split('S')[-1].split('E')[0])
            self.episode = '%01d' % int(name.rsplit(' ', 1)[-1].split('E')[-1])
            self.subtitle = subtitles().get(self.name, self.imdb, self.season, self.episode)

    def container_refresh(self):
        try:
            params = {}
            query = self.folderPath[self.folderPath.find('?') + 1:].split('&')
            for i in query: params[i.split('=')[0]] = i.split('=')[1]
            if not params["action"].endswith('_search'): index().container_refresh()
        except:
            pass

    def offset_add(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"' % (self.name, self.imdb, self.currentTime))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (self.name, self.imdb) in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            read = [i for i in read.splitlines(True) if '"%s"|"%s"|"' % (self.name, self.imdb) in i][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(read)[0]
        except:
            return

    def change_watched(self):
        if content_type == "movies":
            try:
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
            except:
                metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)
        else:
            try:
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
            except:
                metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30350).encode("utf-8"), offset_time), '', self.name, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if self.PseudoTVRunning == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30319).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        if self.PseudoTVRunning == 'True': return
        self.change_watched()
        self.offset_delete()
        self.container_refresh()

    def onPlayBackStopped(self):
        if self.PseudoTVRunning == 'True': return
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()
        self.offset_delete()
        self.offset_add()
        self.container_refresh()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30317).encode("utf-8"), name)
            return

class index:
    def clearCache(self):
        try:
            StorageServer.StorageServer(addonFullId,1).delete("%")
            StorageServer.StorageServer(addonFullId,24).delete("%")
            StorageServer.StorageServer(addonFullId,720).delete("%")
            self.okDialog("The commoncache has been cleared.", "")
        except:
            self.okDialog("The commoncache could not be cleared. Please try again.", "")
        
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(subData):
            file = xbmcvfs.File(subData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                if action == "clear_cache":
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
                else:
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList, content_type):
        if pageList == None: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=%s&url=%s' % (sys.argv[0], content_type, sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def movieList(self, movieList, X, list, page=1):
        if movieList == None: return
        page = int(page)
        numResults = 15
        if not page == 1: start = int((numResults * page) - numResults)
        else: start = 0
        end = int(start + numResults)

        #getmeta = true
        getmeta = getSetting("meta")
        #if action == 'movies_search': getmeta = ''
        
        import math
        total = len(movieList)
        numPages = int(math.ceil(total / float(numResults)))
        nextPage = page + 1
        for i in range(start, end):
            try:
                name, url, image, year, imdb, genre, plot = movieList[i]['name'], movieList[i]['url'] + '/video', movieList[i]['image'], movieList[i]['year'], movieList[i]['imdb'], movieList[i]['genre'], movieList[i]['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name.rsplit(' (', 1)[0].strip()

                sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)
                u = '%s?action=play&name=%s&url=%s&content_type=movies&imdb=%s&year=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getmeta == 'true':
                    #if imdb == '0': imdb = metaget.get_meta('movie', title, year=str(year))['imdb_id']
                    #meta = metaget.get_meta('movie', title, imdb_id=imdb)
                    meta = metaget.get_meta('movie', title, year=str(year))
                    imdb = meta['imdb_id']
                    #meta.update({'playcount': 0, 'overlay': 0})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                    #if banner == '': banner = poster
                    #if banner == '': banner = image
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart
                    

                meta.update({'art(poster)': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30434).encode("utf-8"), 'Action(Info)'))

                if getmeta == 'true' and list != "_search": cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies2&imdb=%s)' % (sys.argv[0], metaimdb)))
                #cm.append((language(30435).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=numResults,isFolder=False)
            except:
                pass
                
        if page != numPages and numPages > 1:
            name, page, image = language(30361).encode("utf-8"), page, addonNext
            page = int(page + 1)

            if list == "":
                sysurl = urllib.quote_plus(X)
                u = '%s?action=movies%s&page=%d&url=%s' % (sys.argv[0], list, page, sysurl)
            elif list == "_search":
                query = urllib.quote_plus(X)
                u = '%s?action=movies%s&page=%d&query=%s' % (sys.argv[0], list, page, query)
            else: u = '%s?action=movies%s&page=%d' % (sys.argv[0], list, page)

            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def showList(self, showList):
        if showList == None: return

        getmeta = getSetting("meta")
        #if action == 'shows_search': getmeta = ''

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()
        file = xbmcvfs.File(subData)
        subRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, url, image, year, imdb, genre, plot = i['name'], i['url'], i['image'], i['year'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name

                sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)
                u = '%s?action=seasons&url=%s&image=%s&year=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot, sysname)

                if getmeta == 'true':
                    #if imdb == '0': imdb = metaget.get_meta('tvshow', title)['imdb_id']
                    #meta = metaget.get_meta('tvshow', title, imdb_id=imdb)
                    meta = metaget.get_meta('tvshow', title)
                    imdb = meta['imdb_id']
                    meta.update({'playcount': 0, 'overlay': 0})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    poster, banner = meta['cover_url'], meta['banner_url']
                    if banner == '': banner = poster
                    if banner == '': banner = image
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': title, 'year' : year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    poster, banner = image, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if action == 'shows_favourites':
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&name=%s&url=%s&imdb=%s)' % (sys.argv[0], sysname, sysurl, metaimdb)))
                    #if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '2': cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'shows_subscriptions':
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&name=%s&url=%s&imdb=%s)' % (sys.argv[0], sysname, sysurl, metaimdb)))
                    #if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                elif action.startswith('shows_search'):
                    cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows2&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                if action == 'shows_search':
                    if ('"%s"' % url in favRead and '"%s"' % url in subRead): suffix = '|F|S| '
                    elif '"%s"' % url in favRead: suffix = '|F| '
                    elif '"%s"' % url in subRead: suffix = '|S| '
                    else: suffix = ''
                    name = suffix + name

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def seasonList(self, seasonList):
        if seasonList == None: return

        try:
            year, imdb, genre, plot, show = seasonList[0]['year'], seasonList[0]['imdb'], seasonList[0]['genre'], seasonList[0]['plot'], seasonList[0]['show']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                seasons = []
                for i in seasonList: seasons.append(i['season'])
                season_meta = metaget.get_seasons(show, imdb, seasons)
                meta = metaget.get_meta('tvshow', show, imdb_id=imdb)
                banner = meta['banner_url']
            else:
                meta = {'tvshowtitle': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                banner = ''
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(seasonList)
        for i in range(0, int(total)):
            try:
                name, url, image = seasonList[i]['name'], seasonList[i]['url'], seasonList[i]['image']
                sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show)
                u = '%s?action=episodes&name=%s&url=%s&image=%s&year=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot, sysshow)

                if getSetting("meta") == 'true':
                    meta.update({'playcount': 0, 'overlay': 0})
                    #meta.update({'playcount': season_meta[i]['playcount'], 'overlay': season_meta[i]['overlay']})
                    poster = season_meta[i]['cover_url']
                    playcountMenu = language(30407).encode("utf-8")
                    if season_meta[i]['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason = urllib.quote_plus(re.sub('[^0-9]', '', str(season_meta[i]['imdb_id']))), urllib.quote_plus(str(season_meta[i]['season']))
                    if poster == '': poster = image
                    if banner == '': banner = poster
                    if banner == '': banner = image
                else:
                    poster, banner = image, image

                meta.update({'label': name, 'title': name, 'art(season.banner)': banner, 'art(season.poster': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                #if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                cm.append((language(30430).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        if episodeList == None: return

        getmeta = getSetting("meta")
        if action == 'episodes_calendar': getmeta = ''

        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, year, imdb, genre, plot, title, show, season, episode = i['name'], i['url'], i['image'], i['date'], i['year'], i['imdb'], i['genre'], i['plot'], i['title'], i['show'], i['season'], i['episode']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, systitle, sysimdb, sysyear, sysseason, sysepisode, sysshow, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(url)
                u = '%s?action=play&name=%s&url=%s&content_type=shows&imdb=%s&year=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getmeta == 'true':
                    if imdb == '0': imdb = metaget.get_meta('tvshow', show)['imdb_id']
                    imdb = re.sub('[^0-9]', '', imdb)
                    meta = metaget.get_episode_meta(title, imdb, season, episode)
                    meta.update({'tvshowtitle': show})
                    if meta['title'] == '': meta.update({'title': title})
                    if meta['episode'] == '': meta.update({'episode': episode})
                    if meta['premiered'] == '': meta.update({'premiered': date})
                    if meta['plot'] == '': meta.update({'plot': plot})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason, metaepisode = urllib.quote_plus(re.sub('[^0-9]', '', str(meta['imdb_id']))), urllib.quote_plus(str(meta['season'])), urllib.quote_plus(str(meta['episode']))
                    label = str(meta['season']) + 'x' + '%02d' % int(meta['episode']) + ' . ' + meta['title']
                    if action == 'episodes_subscriptions': label = show + ' - ' + label
                    poster = meta['cover_url']
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                    label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                    if action == 'episodes_subscriptions': label = show + ' - ' + label
                    poster = image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                cm.append((language(30431).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def item_play_from_here(self, url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            i = str(i)
            label = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % i)
            if label == '': break

            params = {}
            path = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % i)
            path = urllib.quote_plus(path).replace('+%26+', '+&+')
            query = path.split('%3F', 1)[-1].split('%26')
            for i in query: params[urllib.unquote_plus(i).split('=')[0]] = urllib.unquote_plus(i).split('=')[1]
            sysname = urllib.quote_plus(params["name"])
            u = '%s?action=play&name=%s&url=%s&content_type=%s&imdb=%s&year=%s' % (sys.argv[0], sysname, params["url"], params["content_type"], params["imdb"], params["year"])

            meta = {'title': xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'tvshowtitle': xbmc.getInfoLabel('ListItemNoWrap(%s).tvshowtitle' % i), 'season': xbmc.getInfoLabel('ListItemNoWrap(%s).season' % i), 'episode': xbmc.getInfoLabel('ListItemNoWrap(%s).episode' % i), 'writer': xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director': xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating': xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration': xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'premiered': xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'plot': xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i)}
            poster, fanart = xbmc.getInfoLabel('ListItemNoWrap(%s).icon' % i), xbmc.getInfoLabel('ListItemNoWrap(%s).Property(Fanart_Image)' % i)

            item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            item.setProperty("IsPlayable", "true")
            item.setProperty("Video", "true")
            item.setProperty("Fanart_Image", fanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (skin, content) in i]
            write.append('"%s"|"%s"|"%s"' % (skin, content, str(view)))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(viewData, 'w')
            file.write(str(write))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb, year):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb, year):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if '"%s"' % url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i == 0 : return
            write[i], write[i-1] = write[i-1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i+1 == len(write): return
            write[i], write[i+1] = write[i+1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

    def metadata(self, content, name, url, imdb, season, episode):
        try:
            list = []
            if content == 'movie' or content == 'tvshow':
                if content == 'movie':
                    search = metaget.search_movies(name)
                elif content == 'tvshow':
                    search = []
                    result = metahandlers.TheTVDB().get_matching_shows(name)
                    for i in result: search.append({'tvdb_id': i[0], 'title': i[1], 'imdb_id': i[2]})
                for i in search:
                    label = i['title']
                    if 'year' in i: label += ' (%s)' % i['year']
                    list.append(label)
                select = index().selectDialog(list, language(30364).encode("utf-8"))
                if select > -1:
                    if content == 'movie':
                        new_imdb = metaget.get_meta('movie', search[select]['title'] ,year=search[select]['year'])['imdb_id']
                    elif content == 'tvshow':
                        new_imdb = search[select]['imdb_id']
                    new_imdb = re.sub('[^0-9]', '', new_imdb)
                    sources = []
                    try: sources.append(favData)
                    except: pass
                    try: sources.append(favData2)
                    except: pass
                    try: sources.append(subData)
                    except: pass
                    if sources == []: raise Exception()
                    for source in sources:
                        try:
                            file = xbmcvfs.File(source)
                            read = file.read()
                            file.close()
                            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
                            line2 = line.replace('"0"', '"%s"' % new_imdb).replace('"%s"' % imdb, '"%s"' % new_imdb)
                            write = read.replace(line, line2)
                            file = xbmcvfs.File(source, 'w')
                            file.write(str(write))
                            file.close()
                        except:
                            pass
                    metaget.update_meta(content, '', imdb, year='')
                    index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def metadata2(self, content, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library_add(self, name, url, image, imdb, year, update=True, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            self.library(name, url, imdb, year, silent=True)

            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30312).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library_from_search(self, name, url, image, imdb, year, update=True, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            if '"%s"' % url in read:
                index().infoDialog(language(30316).encode("utf-8"), name)
                return

            self.library(name, url, imdb, year, silent=True)

            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30312).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library_delete(self, name, url, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()

            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30313).encode("utf-8"), name)
        except:
            return

    def library_update(self, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, year, imdb, url, image in match:
                if xbmc.abortRequested == True: sys.exit()
                self.library(name, url, imdb, year, silent=True)
            if getSetting("updatelibrary") == 'true':
                xbmc.executebuiltin('UpdateLibrary(video)')
            if silent == False:
                index().infoDialog(language(30314).encode("utf-8"))
        except:
            return

    def library(self, name, url, imdb, year, check=False, silent=False):
        try:
            library = xbmc.translatePath(getSetting("tv_library"))
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            show = name
            seasonList = seasons().get(url, '', year, imdb, '', '', show, idx=False)
        except:
            return

        try:
            for i in seasonList:
                season, seasonUrl, show_alt, idx_data = i['name'], i['url'], i['show'], i['idx_data']
                enc_show = show_alt.translate(None, '\/:*?"<>|')
                folder = os.path.join(library, enc_show)
                xbmcvfs.mkdir(folder)
                enc_season = season.translate(None, '\/:*?"<>|')
                seasonDir = os.path.join(folder, enc_season)
                xbmcvfs.mkdir(seasonDir)
                episodeList = episodes().get(season, seasonUrl, '', year, imdb, '', '', show_alt, idx_data, idx=False)
                for i in episodeList:
                    name, url, imdb = i['name'], i['url'], i['imdb']
                    sysname, sysurl, sysimdb, sysyear = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(imdb), urllib.quote_plus(year)
                    content = '%s?action=play&name=%s&url=%s&content_type=shows&imdb=%s&year=%s' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear)
                    enc_name = name.translate(None, '\/:*?"<>|')
                    stream = os.path.join(seasonDir, enc_name + '.strm')
                    file = xbmcvfs.File(stream, 'w')
                    file.write(str(content))
                    file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), show)
        except:
            return

    def download(self, name, url):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().run(url, name, download=True)
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

class subscriptions:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(subData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

class favourites:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            if getSetting("fav_sort") == '1':
                try: status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
                except: status = ''
            else:
                status = ''
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': '', 'status': status})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))
        elif getSetting("fav_sort") == '1':
            filter = []
            self.list = sorted(self.list, key=itemgetter('name'))
            filter += [i for i in self.list if not i['status'] == 'Ended']
            filter += [i for i in self.list if i['status'] == 'Ended']
            self.list = filter

        index().showList(self.list)

class root:
    def __init__(self):
        if user == '' or password == '': self.openSettings(addonId)
    def get(self, content_type=None):
        rootList = []
        if content_type == "movies":
            rootList.append({'name': 30501, 'image': 'Title.png', 'action': 'movies_title'})
            rootList.append({'name': 30500, 'image': 'Added.png', 'action': 'movies_added'})
            rootList.append({'name': 30502, 'image': 'Release.png', 'action': 'movies_release'})
            rootList.append({'name': 30503, 'image': 'Rating.png', 'action': 'movies_rating'})
            rootList.append({'name': 30504, 'image': 'Genres.png', 'action': 'genres_movies'})
            rootList.append({'name': 30507, 'image': 'Search.png', 'action': 'movies_search'})
        elif content_type == "shows":
            rootList.append({'name': 30501, 'image': 'Title.png', 'action': 'shows_title'})
            rootList.append({'name': 30502, 'image': 'Release.png', 'action': 'shows_release'})
            rootList.append({'name': 30503, 'image': 'Rating.png', 'action': 'shows_rating'})
            rootList.append({'name': 30504, 'image': 'Genres.png', 'action': 'genres_shows'})
            rootList.append({'name': 30505, 'image': 'Favourites.png', 'action': 'shows_favourites'})
            rootList.append({'name': 30506, 'image': 'Subscriptions.png', 'action': 'shows_subscriptions'})
            rootList.append({'name': 30507, 'image': 'Search.png', 'action': 'shows_search'})
        else:
            rootList.append({'name': 30508, 'image': 'Movies.png', 'action': 'root_movies'})
            rootList.append({'name': 30509, 'image': 'Shows.png', 'action': 'root_shows'})
            rootList.append({'name': 30515, 'image': 'Subscriptions.png', 'action': 'clear_cache'})
        index().rootList(rootList)
        index().downloadList()
        
    def openSettings(self, id=addonId):
        try:
            xbmc.executebuiltin('Dialog.Close(busydialog)')
            xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)
            #xbmc.executebuiltin('SetFocus(%i)' % (2 + 200))
            #xbmc.executebuiltin('SetFocus(%i)' % (3 + 100))
            xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/,replace)")
        except:
            return

class link:
    def __init__(self):
        self.base_link = 'http://ororo.tv'
        self.movies_link = 'http://ororo.tv/en/movies'
        self.sign_link = 'http://ororo.tv/en/users/sign_in'
        self.cookie = None
        self.lang_cookie = 'locale=en; nl=true'
        #self.user = user
        #self.password = password
        self.post = {'user[email]': user, 'user[password]': password, 'user[remember_me]': 1}
        self.post = urllib.urlencode(self.post)

class genres:
    def __init__(self):
        self.list = []

    def get(self, content_type):
        if content_type == "movies": self.base_link = link().movies_link
        else: self.base_link = link().base_link
        #self.list = self.ororo_list()
        self.list = cache3(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().pageList(self.list, content_type)

    def ororo_list(self):
        try:
            cookie = link().cookie
            url = self.base_link

            if not (user == '' or password == ''):
                if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
                if not '"guest":false' in str(result):
                    index().infoDialog(language(30516).encode("utf-8"))
                    return
            else:
                index().infoDialog(language(30517).encode("utf-8"))
                return

            genres = common.parseDOM(result, "select", attrs = { "id": "genre-select" })[0]
            genres = re.compile('(<option.+?</option>)').findall(genres)
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "option", ret="value")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonGenres.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list
        
class movies:
    def __init__(self):
        self.list = []
        content_type = "movies"

    def title(self, page):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().movieList(self.list, None, "_title", page)

    def release(self, page):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('year'))
        self.list = self.list[::-1]
        index().movieList(self.list, None, "_release", page)
    
    def added(self, page):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('sort'))
        self.list = self.list[::-1]
        index().movieList(self.list, None, "_added", page)        

    def rating(self, page):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('rating'))
        self.list = self.list[::-1]
        index().movieList(self.list, None, "_rating", page)

    def genre(self, url, page):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = [i for i in self.list if url.lower() in i['genre'].lower()]
        index().movieList(self.list, url, "", page)

    def search(self, page, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = urllib.unquote_plus(query).strip()
        if not (self.query is None or self.query == ''):
            self.X = self.query
            self.query = self.query.split(' ')
            self.list = self.ororo_list()
            self.list = [i for i in self.list if all(x.lower() in i['name'].lower() for x in self.query)]
            index().movieList(self.list, self.X, "_search", page)

    def ororo_list(self):
        try:
            cookie = link().cookie
            url = link().movies_link

            if not (user == '' or password == ''):
                if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
                if not '"guest":false' in str(result):
                    index().infoDialog(language(30516).encode("utf-8"))
                    return
            else:
                index().infoDialog(language(30517).encode("utf-8"))
                return

            movies = common.parseDOM(result, "div", attrs = { "class": "shows movies" })[0]
            movies = movies.replace("'index show'", "'index show'><a")
            movies = common.parseDOM(movies, "div", attrs = { "class": "index show" })
        except:
            return

        for movie in movies:
            try:
                name = common.parseDOM(movie, "a", attrs = { "class": "name" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "value" })
                year = [i for i in year if i.isdigit and len(i)==4][0]
                year = year.encode('utf-8')

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                
                paid = common.parseDOM(movie, "a", ret="class")
                paid = paid[0].encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="data-original")[0]
                except:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                image = '%s%s' % (link().base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                sort = common.parseDOM(movie, "a", ret="data-newest")[0]
                sort = common.replaceHTMLCodes(sort)
                sort = sort.encode('utf-8')
                
                rating = common.parseDOM(movie, "span", attrs = { "class": "value" })[1]
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                

                try:
                    genre = common.parseDOM(movie, "a", ret="data-info")[0]
                    genre = genre.split(' ')
                    genre = [i for i in genre if any(x == i for x in ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'])]
                    genre = [i.title() for i in genre]
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = common.parseDOM(movie, "p")[-1]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                if "paid" not in paid: self.list.append({'name': '%s (%s)' % (name, year), 'url': url, 'image': image, 'year': year, 'imdb': '0', 'genre': genre, 'plot': plot, 'sort': sort, 'rating': rating})
            except:
                pass

        return self.list

class shows:
    def __init__(self):
        self.list = []
        content_type == "shows"

        
    def title(self):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def release(self):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = sorted(self.list, key=itemgetter('sort'))
        self.list = self.list[::-1]
        index().showList(self.list)

    def rating(self):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        index().showList(self.list)

    def genre(self, url):
        #self.list = self.ororo_list()
        self.list = cache(self.ororo_list)
        self.list = [i for i in self.list if url.lower() in i['genre'].lower()]
        index().showList(self.list)

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = self.query.split(' ')
            self.list = self.ororo_list()
            self.list = [i for i in self.list if all(x.lower() in i['name'].lower() for x in self.query)]
            index().showList(self.list)

    def ororo_list(self):
        try:
            cookie = link().cookie
            url = link().base_link

            if not (user == '' or password == ''):
                if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
                if not '"guest":false' in str(result):
                    index().infoDialog(language(30516).encode("utf-8"))
                    return
            else:
                index().infoDialog(language(30517).encode("utf-8"))
                return

            shows = common.parseDOM(result, "div", attrs = { "class": "shows" })[0]
            shows = shows.replace("'index show'", "'index show'><a")
            shows = common.parseDOM(shows, "div", attrs = { "class": "index show" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "a", attrs = { "class": "name" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "value" })
                year = [i for i in year if i.isdigit and len(i)==4][0]
                year = year.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="data-original")[0]
                except:
                    image = common.parseDOM(show, "img", ret="src")[0]
                image = '%s%s' % (link().base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                sort = common.parseDOM(show, "a", ret="data-newest")[0]
                sort = common.replaceHTMLCodes(sort)
                sort = sort.encode('utf-8')

                try:
                    genre = common.parseDOM(show, "a", ret="data-info")[0]
                    genre = genre.split(' ')
                    genre = [i for i in genre if any(x == i for x in ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Education', 'Family', 'Fantasy', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Reality-TV', 'Romance', 'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western'])]
                    genre = [i.title() for i in genre]
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = common.parseDOM(show, "p")[-1]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': '0', 'genre': genre, 'plot': plot, 'sort': sort})
            except:
                pass

        return self.list

class seasons:
    def __init__(self):
        self.list = []

    def get(self, url, image, year, imdb, genre, plot, show, idx=True):
        if idx == True:
            #self.list = self.ororo_list(url, image, year, imdb, genre, plot, show)
            self.list = cache2(self.ororo_list, url, image, year, imdb, genre, plot, show)
            index().seasonList(self.list)
        else:
            self.list = self.ororo_list(url, image, year, imdb, genre, plot, show)
            return self.list

    def ororo_list(self, url, image, year, imdb, genre, plot, show):
        try: 
            cookie = link().cookie

            if not (user == '' or password == ''):
                if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
                if not '"guest":false' in str(result):
                    index().infoDialog(language(30516).encode("utf-8"))
                    return
            else:
                index().infoDialog(language(30517).encode("utf-8"))
                return

            seasons = common.parseDOM(result, "ul", attrs = { "class": "ui tabular menu season-tabs" })[0]
            seasons = re.sub('<li\s.+?>','<li>', seasons)
            seasons = common.parseDOM(seasons, "li")
        except:
            return

        for season in seasons:
            try:
                num = common.parseDOM(season, "a")[0]
                num = re.sub('[^0-9]', '', num)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show, 'season': num, 'sort': '%10d' % int(num), 'idx_data': result})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

class episodes:
    def __init__(self):
        self.list = []

    def get(self, name, url, image, year, imdb, genre, plot, show, idx_data='', idx=True):
        if idx == True:
            #self.list = self.ororo_list(name, url, image, year, imdb, genre, plot, show, idx_data)
            self.list = cache(self.ororo_list, name, url, image, year, imdb, genre, plot, show, idx_data)
            index().episodeList(self.list)
        else:
            self.list = self.ororo_list(name, url, image, year, imdb, genre, plot, show, idx_data)
            return self.list

    def ororo_list(self, name, url, image, year, imdb, genre, plot, show, idx_data):
        try:
            if not idx_data == '': result = idx_data
            else:
                cookie = link().cookie

                if not (user == '' or password == ''):
                    if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                    result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
                    if not '"guest":false' in str(result):
                        index().infoDialog(language(30516).encode("utf-8"))
                        return
                else:
                    index().infoDialog(language(30517).encode("utf-8"))
                    return

            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            episodes = common.parseDOM(result, "div", attrs = { "class": "tab-content episodes-tab" })[0]
            episodes = common.parseDOM(episodes, "div", attrs = { "id": season })[0]
            episodes = common.parseDOM(episodes, "li")
        except:
            return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "a")[0]
                try: title = title.split(' ', 1)[1].strip()
                except: pass
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "a", attrs = { "class": "episode" }, ret=" href")[0]
                num = re.sub('[^0-9]', '', num.split("-")[-1])
                num = num.encode('utf-8')

                name = show + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="data-href")[0]
                url = '%s%s' % (link().base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: desc = common.parseDOM(episode, "div", attrs = { "class": "plot" })[0]
                except: desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': year, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

class resolver:
    def run(self, url, name, download=False):
        try:
            url = self.ororo(url)

            if url is None: raise Exception()

            if download == True: return url
            player().run(name, url)
            return url
        except:
            if content_type == "movies":
                index().infoDialog(language(30320).encode("utf-8"))
            else: 
                index().infoDialog(language(30318).encode("utf-8"))
            return

    def ororo(self, url):
        try:
            cookie = link().cookie
            referer = url
            
            if not (user == '' or password == ''):
                if cookie == None: cookie = client.source(link().sign_link, post=link().post, cookie=link().lang_cookie, output='cookie')
                result = client.source(url, cookie='%s; %s' % (cookie, link().lang_cookie))
            else:
                index().infoDialog(language(30517).encode("utf-8"))
                return
                

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url == None: return
            if cookie == None: cookie = ''

            url = '%s|User-Agent=%s&Cookie=%s&video=true' % (url, urllib.quote_plus(client.agent()), urllib.quote_plus(cookie))
            
            return url
        except:
            return


main()
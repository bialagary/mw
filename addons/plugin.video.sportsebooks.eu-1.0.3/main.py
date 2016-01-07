import urllib, urllib2, httplib
import sys, re, os, cgi
import xbmc, xbmcplugin, xbmcaddon, xbmcgui, gui
import simplejson as json

__scriptname__  = sys.modules[ '__main__' ].__scriptname__
__scriptID__  = sys.modules[ '__main__' ].__scriptID__
__url__ = sys.modules[ '__main__' ].__url__
__addon__ = sys.modules[ '__main__' ].__addon__
t = sys.modules[ '__main__' ].__language__

checkUrl = __url__ + '/api/checkPluginVersionXBMC'
playerUrl = __url__ + '/api/setPlayer'
jsonUrl = __url__ + '/api/getChannelList?'
scheduleUrl = __url__ + '/resources/guide'

HOST = 'XBMC'
VERSION = 100

login = __addon__.getSetting('username')
password = __addon__.getSetting('userpassword')
multi = __addon__.getSetting('video_quality')
display = __addon__.getSetting('list_display')

os.path.join( __addon__.getAddonInfo('path'), 'resources' )

#confluence: thumb: 500, biglist: 51, normal 50
#transparency: thumb: 53, biglist: 52, normal: 590

SKINS = {
    'confluence': { 'opt1': 51, 'opt2': 50 },
    'transparency': { 'opt1': 52, 'opt2': 590 }
}

class Settings:
    def __init__(self):
        pass
    
    def showSettings(self):
        __addon__.openSettings(sys.argv[0])
    
    def setViewMode(self, view):
        if view != 'orig':
            for k, v in SKINS.items():
                if k in xbmc.getSkinDir():
                    if view == 'general':
                        xbmc.executebuiltin('Container.SetViewMode(' + str(v['opt2']) + ')')
                    elif view == 'other':
                        xbmc.executebuiltin('Container.SetViewMode(' + str(v['opt1']) + ')')
    
    def getJsonUrl(self):
        return jsonUrl

class ShowList:
    def __init__(self):
        pass
    
    def decode(self, string):
        json_ustr = json.dumps(string, ensure_ascii=False)
        return json_ustr.encode('utf-8')
    
    def JsonToSortedTab(self, json):
        strTab = []
        outTab = []
        for v,k in json.iteritems():
            strTab.append(int(v))
            strTab.append(k)
            outTab.append(strTab)
            strTab = []
        outTab.sort(key=lambda x: x[0])
        return outTab
    
    def getJsonFromAPI(self, url):
        result_json = { '0': 'Null' }
        try:
            headers = { 'User-Agent': HOST, 'ContentType': 'application/x-www-form-urlencoded' }
            post = { 'username': login, 'userpassword': password }
            data = urllib.urlencode(post)
            reqUrl = urllib2.Request(url, data, headers)
            raw_json = urllib2.urlopen(reqUrl)
            content_json = raw_json.read()

            if str(content_json) == 'status=-5':
                msg = Messages()
                msg.Error(t(57018).encode('utf-8'), t(57055).encode('utf-8'), t(57037).encode('utf-8'), t(57038).encode('utf-8'))
                return
            elif str(content_json) == 'status=-6':
                msg = Messages()
                msg.Error(t(57018).encode('utf-8'), t(57056).encode('utf-8'))
                return
            elif str(content_json) == 'status=-100':
                msg = Messages()
                msg.Error(t(57018).encode('utf-8'), t(57056).encode('utf-8'))
                return
            else:
                result_json = json.loads(content_json)

        except urllib2.URLError, urlerr:
            msg = Messages()
            result_json = { '0': 'Error' }
            print urlerr
            msg.Error(t(57001).encode('utf-8'), t(57002).encode('utf-8'), t(57003).encode('utf-8'))
        except NameError, namerr:
            msg = Messages()
            result_json = { '0': 'Error' }
            print namerr
            msg.Error(t(57009).encode('utf-8'), t(57010).encode('utf-8'))
        except ValueError, valerr:
            msg = Messages()
            result_json = { '0': 'Error' }
            print valerr
            msg.Error(t(57001).encode('utf-8'), t(57011).encode('utf-8'), t(57012).encode('utf-8'), t(57013).encode('utf-8'))
        except httplib.BadStatusLine, statuserr:
            msg = Messages()
            result_json = { '0': 'Error' }
            print statuserr
            msg.Error(t(57001).encode('utf-8'), t(57002).encode('utf-8'), t(57003).encode('utf-8'))
        return result_json
    
    def loadChannels(self, url):
        parser = UrlParser()
        params = parser.getParams()
        mode = parser.getIntParam(params, 'mode')
        customResponse = self.getJsonFromAPI(url)

        if customResponse:
            channelsArray = self.JsonToSortedTab(customResponse)
            if len(channelsArray) > 0:
                try:
                    if channelsArray[0][1] == 'Null':
                        msg = Messages()
                        msg.Warning(t(57001).encode('utf-8'), t(57004).encode('utf-8'))
                    elif channelsArray[0][1] != 'Error' and channelsArray[0][1] != 'Null':
                        for i in range(len(channelsArray)):
                            k = channelsArray[i][1]
                            name = self.decode(k['channel_name']).replace("\"", '')
                            title = self.decode(k['channel_title']).replace("\"", '')
                            desc = self.decode(k['channel_description']).replace("\"", '')
                            tags = self.decode(k['channel_tags']).replace("\"", '')
                            image = k['channel_logo_url']
                            online = k['channel_online']
                            rank = k['rank']
                            bitrate = k['multibitrate']
                            user = self.decode(k['user_name']).replace("\"", '')
                            self.addChannelToXBMC(str(mode), online, name, title, image, desc, tags, user)
                        s = Settings()
                        s.setViewMode('other')
                        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                        if mode == 1:
                            xbmcplugin.addSortMethod(handle = int(sys.argv[1]), sortMethod = xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                except KeyError, keyerr:
                    msg = Messages()
                    print keyerr
                    msg.Error(t(57001).encode('utf-8'), t(57025).encode('utf-8'))
            else:
                msg = Messages()
                msg.Error(t(57001).encode('utf-8'), t(57004).encode('utf-8'))
    
    def addChannelToXBMC(self, mode, action, name, title, img, desc, tags, user):
        status = t(57033).encode('utf-8')
        if title == '':
            title = name
            label = name
        else:
            label = title
        if desc == None or desc == '' or desc == 'null':
            desc = t(57016).encode('utf-8')
        if tags == None or tags == 'null':
            tags = t(57017).encode('utf-8')
        if int(action) == 0:
            if display == 'color':
                status = '[COLOR red]' + t(57030).encode('utf-8') + '[/COLOR]'
            elif display == 'gray':
                status = t(57030).encode('utf-8')
        elif int(action) == 1:
            if display == 'color':
                status = '[COLOR green]' + t(57029).encode('utf-8') + '[/COLOR]'
            elif display == 'gray':
                status = t(57029).encode('utf-8')
        if display == 'color':
            label = ' [B]%s[/B]  %s [I]%s[/I]    [B]%s[/B] ' % (title, t(57032).encode('utf-8'), user, status)
        elif display == 'gray':
            label = ' %s %s %s %s %s    %s ' % (title, t(57031).encode('utf-8'), name, t(57032).encode('utf-8'), user, status)
        liz = xbmcgui.ListItem(label, iconImage = 'DefaultFolder.png', thumbnailImage = img)
        liz.setProperty('IsPlayable', 'false')
        liz.setInfo(type = 'Video', infoLabels={ 'Title': title, 'Plot': desc, 'Studio': __scriptname__, 'Tagline': tags, 'Status': status, 'Aired': user })
        u = '%s?mode=%d&action=%d&channel=%s&title=%s' % (sys.argv[0], int(mode), int(action), name, urllib.quote_plus(title))
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

class UrlParser:
    def __init__(self):
        pass
    
    def getParam(self, params, name):
        try:
            result = params[name]
            result = urllib.unquote_plus(result)
            return result
        except:
            return None
    
    def getIntParam (self, params, name):
        try:
            param = self.getParam(params, name)
            return int(param)
        except:
            return None
    
    def getBoolParam (self, params, name):
        try:
            param = self.getParam(params,name)
            return 'True' == param
        except:
            return None
    
    def getParams(self, paramstring = sys.argv[2]):
        param=[]
        if len(paramstring) >= 2:
            params = paramstring
            cleanedparams = params.replace('?', '')
            if (params[len(params)-1] == '/'):
                params = params[0:len(params)-2]
            pairsofparams = cleanedparams.split('&')
            param = {}
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if (len(splitparams)) == 2:
                    param[splitparams[0]] = splitparams[1]
        return param

class VideoPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        self.is_active = True
        print '#Starting control VideoPlayer events#'
    
    def setPremium(self, premium):
        self.premium = premium
    
    def getPremium(self):
        return self.premium
    
    def onPlayBackPaused(self):
        print '#Im paused#'
        self.is_active = False
    
    def onPlayBackResumed(self):
        print '#Im Resumed #'
    
    def onPlayBackStarted(self):
        print '#Playback Started#'
        try:
            print '#Im playing :: ' + self.getPlayingFile()
        except:
            print '#I failed get what Im playing#'
    
    def onPlayBackEnded(self):
        msg = Messages()
        print '#Playback Ended#'
        self.is_active = False
        if self.getPremium() == 0:
            msg.Warning(t(57018).encode('utf-8'), t(57019).encode('utf-8'), t(57020).encode('utf-8'))
        else:
            msg.Warning(t(57018).encode('utf-8'), t(57027).encode('utf-8'))
    
    def onPlayBackStopped(self):
        print '## Playback Stopped ##'
        self.is_active = False
    
    def sleep(self, s):
        xbmc.sleep(s)

class InitPlayer:
    def __init__(self):
        pass
    
    def checkVersion(self):
        status = None
        try:
            parser = UrlParser()
            headers = { 'User-Agent' : HOST }
            post = { 'v': VERSION }
            data = urllib.urlencode(post)
            request = urllib2.Request(checkUrl, data, headers)
            response = urllib2.urlopen(request)
            responseRead = response.read()
            params = parser.getParams(responseRead)
            status = parser.getIntParam(params, 'status')
        except urllib2.URLError, urlerr:
            print 'Error when checking if the plugin version is up to date!'
            print urlerr
        print 'Version status: %s' % (status)
        return { 'status': status }
    
    def setPlayer(self, channel):
        status = None
        rtmp = None
        imgLink = None
        titile = ''
        premium = 0
        try:
            parser = UrlParser()
            headers = { 'User-Agent' : HOST }
            if login != '' and password != '':
                post = { 'channel': channel, 'platform': 'XBMC', 'username': login, 'userpassword': password }
            else:
                post = { 'channel': channel, 'platform': 'XBMC' }
            data = urllib.urlencode(post)
            request = urllib2.Request(playerUrl, data, headers)
            response = urllib2.urlopen(request)
            responseRead = response.read()
            params = parser.getParams(responseRead)
            
            status = parser.getParam(params, 'status')
            premium = parser.getIntParam(params, 'premium')
            imgLink = parser.getParam(params, 'image')
            rtmpLink = parser.getParam(params, 'rtmp')
            playPath = parser.getParam(params, 'playpath')
            bitrate = parser.getIntParam(params, 'bitrate')
            token = parser.getParam(params, 'token')
            title = parser.getParam(params, 'title')
    
            if title == '':
                 title = parser.getParam(params, 'name')
            
            if status == '1':
                rtmp = rtmpLink + '/' + str(playPath) + str(token)
                #rtmp += ' playpath=' + str(playPath)
                rtmp += " live=true"
            else:
                rtmp = False

            print "### " + rtmp + " ###"

        except urllib2.URLError, urlerr:
            print urlerr
            msg = Messages()
            msg.Error(t(57014).encode('utf-8'), t(57015).encode('utf-8'), t(57003).encode('utf-8'))
        print 'Output rtmp link: %s' % (rtmp)
        return { 'status': status, 'rtmp': rtmp, 'imgLink': imgLink, 'title': title, 'premium': premium }
                
    def LoadVideoLink(self, channel):
        res = True
        title = ''
        videoLink = self.setPlayer(channel)
        if videoLink['status'] == '1':
            if videoLink['rtmp'].startswith('rtmp'):
                liz = xbmcgui.ListItem(videoLink['title'], iconImage = videoLink['imgLink'], thumbnailImage = videoLink['imgLink'])
                liz.setInfo(type='Video', infoLabels={ 'Title': videoLink['title'] })
                try:
                    player = VideoPlayer()
                    player.setPremium(int(videoLink['premium']))
                    if videoLink['premium'] == 0:
                        msg = Messages()
                        msg.Warning(t(57034).encode('utf-8'), t(57036).encode('utf-8'), t(57037).encode('utf-8'), t(57038).encode('utf-8'))
                    player.play(videoLink['rtmp'], liz)
                    while player.is_active:
                        player.sleep(100)
                except:
                    msg = Messages()
                    msg.Error(t(57018).encode('utf-8'), t(57021).encode('utf-8'), t(57028).encode('utf-8'))
            else:
                msg = Messages()
                msg.Error(t(57018).encode('utf-8'), t(57022).encode('utf-8'))
        elif videoLink['status'] == '-1':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57043).encode('utf-8'))
        elif videoLink['status'] == '-2':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57044).encode('utf-8')) 
        elif videoLink['status'] == '-3':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57045).encode('utf-8'))
        elif videoLink['status'] == '-4':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57046).encode('utf-8'), t(57047).encode('utf-8'))
        elif videoLink['status'] == '-5':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57055).encode('utf-8'), t(57037).encode('utf-8'), t(57038).encode('utf-8'))
        elif videoLink['status'] == '-6':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57056).encode('utf-8'))
        elif videoLink['status'] == '-100':
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57056).encode('utf-8'))
        else:
            msg = Messages()
            msg.Warning(t(57018).encode('utf-8'), t(57042).encode('utf-8'))
        return res

class Messages:
    def __init__(self):
        pass
    
    def Error(self, t1, t2, t3 = '', t4 = ''):
        err = gui.Windows()
        err.Error(t1, t2, t3, t4)
    
    def Warning(self, t1, t2, t3 = '', t4 = ''):
        warn = gui.Windows()
        warn.Warning(t1, t2, t3, t4)

class Handler:
    def __init__(self):
        pass
    
    def run(self, mode):
        parser = UrlParser()
        params = parser.getParams()
        mode = parser.getIntParam(params, 'mode')
        channel = parser.getParam(params, 'channel')
        title = parser.getParam(params, 'title')
        action = parser.getIntParam(params, 'action')
        if mode > 0 and action == None:
            url = ''
            if mode == 1:
                url = jsonUrl + '&option=online-alphabetical'
            elif mode == 2:
                url = jsonUrl + '&option=online-now-viewed'
            elif mode == 3:
                url = jsonUrl + '&option=online-most-viewed'
            elif mode == 4:
                url = jsonUrl + '&option=offline-ranking'
            elif mode == 5:
                url = jsonUrl + '&option=all-ranking'
            showlist = ShowList()
            showlist.loadChannels(url)
        elif mode > 0 and action == 1:
            if channel != '':
                run = InitPlayer()
                run.LoadVideoLink(channel)
        elif mode > 0 and action == 0:
            msg = Messages()
            msg.Warning(t(57005).encode('utf-8'), t(57006).encode('utf-8'), t(57007).encode('utf-8'), t(57008).encode('utf-8'))

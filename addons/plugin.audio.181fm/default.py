import urllib,urllib2,re,cookielib,string,HTMLParser
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.addon import Addon
import datetime
import time
import os

ADDON=xbmcaddon.Addon(id='plugin.audio.181fm')
pars = HTMLParser.HTMLParser()
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.181fm/resources/art', ''))
ADDON=xbmcaddon.Addon(id='plugin.audio.181fm')

_DOWNLOAD_T = 213
_DOWNLOAD_A = 214

def OPENURL(url):
        print "openurl = " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=pars.unescape(link)
        link=urllib.unquote(link)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        return link


def MAIN():
        if xbmc.Player().isPlayingAudio():
                addSearchDir('[COLOR red]Download Current Track Playing[/COLOR]',  _DOWNLOAD_T ,art+"hubmusic.png")
                addSearchDir('[COLOR red]Search Current Artist Playing[/COLOR]', _DOWNLOAD_A,art+"hubmusic2.png")

        link=OPENURL('http://www.181.fm/channellistmini.php')
        match = re.compile('700"><br>(.+?)</font></td>(.+?)</table>').findall(link)
        for name,url in match:
            name=name.replace('/','&')
            addDir(name,url,1,art+name+".png")
    

def LIST(mname,murl):
        if xbmc.Player().isPlayingAudio():
                addSearchDir('[COLOR red]Download Current Track Playing[/COLOR]',  _DOWNLOAD_T ,art+"hubmusic.png")
                addSearchDir('[COLOR red]Search Current Artist Playing[/COLOR]', _DOWNLOAD_A,art+"hubmusic2.png")
        thumb=art+"%s.png"%(mname)
        print "kk "+thumb
        match = re.compile('<a STYLE="text-decoration:none" href="(.+?)" class="left_link">(.+?)</a></font></td>').findall(murl)
        for url,name in match:
            addPlay(name,url,2,thumb)


def LINK(name,url):
        link=OPENURL(url)
        source = re.compile('<REF HREF="(.+?)"/>').findall(link)
        for stream_url in source:
                match = re.compile('relay').findall(stream_url)
                print match
                if len(match)>0:
                        stream=stream_url
                else:
                        stream=stream_url
        pl = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        pl.clear()    
        pl.add(stream)
        xbmc.Player().play(pl)
        xbmc.executebuiltin("Container.Refresh")
        

def addPlay(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage='', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',art+"fanart.jpg")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addSearchDir(name, mode,iconimage):
    #thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0] + "?mode=" + str(mode)        
    liz       = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image',art+"fanart.jpg")
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)


def addDir(name, url, mode, thumbImage):

        u  = sys.argv[0]

        u += "?url="  + urllib.quote_plus(url)
        u += "&mode=" + str(mode)
        u += "&name=" + urllib.quote_plus(name)

        liz = xbmcgui.ListItem(name, iconImage='', thumbnailImage=thumbImage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',art+"fanart.jpg")

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=True)

class HUB( xbmcgui.WindowXMLDialog ): # The call MUST be below the xbmcplugin.endOfDirectory(int(sys.argv[1])) or the dialog box will be visible over the pop-up.
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()

             
def pop():# Added Close_time for window auto-close length.....
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    elif xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    
    popup.doModal()
    del popup
                
def checkdate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update


def check_popup():

    threshold  = 120

    now   = datetime.datetime.today()
    prev  = checkdate(ADDON.getSetting('pop_time'))
    delta = now - prev
    nDays = delta.days

    doUpdate = (nDays > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('pop_time', str(now).split('.')[0])
    pop()


def DownloaderClass(url,dest):
        dp = xbmcgui.DialogProgress()
        dp.create("XBMCHUB...Maintenance","Downloading & Copying File",'')
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
            print 'Downloaded '+str(percent)+'%'
            dp.update(percent)
        except:
            percent = 100
            dp.update(percent)
        if (dp.iscanceled()): 
            print "DOWNLOAD CANCELLED" # need to get this part working
            return False
        dp.close()
        del dp

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "Name: "+str(name)

if mode == _DOWNLOAD_T or mode == _DOWNLOAD_A:
        url = 'DUMMY'

if mode==None or url==None or len(url)<1:
        MAIN()
       
elif mode==1:
        LIST(name,url)
        
elif mode==2:
        LINK(name,url)

elif mode == _DOWNLOAD_T or mode == _DOWNLOAD_A:
        muspath = xbmc.translatePath(os.path.join('special://home/addons', ''))
        xbmcmusic=os.path.join(muspath, 'plugin.audio.xbmchubmusic')
        if os.path.exists(xbmcmusic)==False:
                dialog = xbmcgui.Dialog()
                ret=dialog.yesno("XBMCHUB TEAM", "This will Install XBMCHUB Music.","Will take effect after restart.","Would you like to install?",)
                if ret==1:
                        url = 'http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/plugin.audio.xbmchubmusic-2.6.zip'
                        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                        lib=os.path.join(path, 'plugin.audio.xbmchubmusic-2.6.zip')
                        DownloaderClass(url,lib)
                        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
                        time.sleep(2)
                        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
               
        else:
                if xbmc.Player().isPlayingAudio():
                        info   = xbmc.Player().getMusicInfoTag()
                        artist = info.getTitle().split(' - ')[0]
                        track  = info.getTitle()
                        track  = track.split(' (')[0]
                        print track
                        artist=artist.replace('f/','ft ')

                        cmd = '%s?mode=%s&name=%s&artist=%s' % ('plugin://plugin.audio.xbmchubmusic/', str(mode), track, artist)
                        xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
check_popup()

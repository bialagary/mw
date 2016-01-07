import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon

#Old Skool - By ANONYMOUS.......

addon_id = 'plugin.audio.oldskool'
plugin = xbmcaddon.Addon(id=addon_id)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
baseurl = 'http://artmeetsscience.co.uk/tapes/'
Mypicture = 'http://www.thissongslaps.com/wp-content/uploads/2015/03/anonymous.jpg'


def INDEX():
        req = urllib2.Request(baseurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        try:
            req = urllib2.Request('http://pastebin.com/raw.php?i=BBvznDS4')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            message=response.read()
            response.close()
        except:
            message='[B][COLOR white]OLD SKOOL BY ANONYMOUS[/COLOR][/B]'
			
        addDir(message,' ',1,Mypicture,Mypicture)
        match=re.compile('<a href="(.+?)">(.+?)</a>.+?\n').findall(link)
        for url,name in match:
                nono = ['Name','\r\r    Sign Up\r    Lo..&gt;']
                if name not in nono:
                        name = name.replace('..&gt;','')
                        name = name.replace('&amp;','&')
                        url = baseurl+url
                        url = url.replace('&amp;','&')
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,1,icon,Mypicture)
                
                        
def LINKS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">(.+?)</a>.+?\n').findall(link)
        for url1,name in match:
                nono = ['Name', '\r\r    Sign Up\r    Lo..&gt;']
                ok = '.mp3'
                if name  not in nono:
                        name = name.replace('..&gt;','')
                        name = name.replace('&amp;','&')
                        url1 = url+url1
                        url1 = url1.replace('&amp;','&')
                        if ok in url1:
                                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url1,2,icon,fanart)
                        if ok not in url1:
                                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url1,1,icon,fanart)
                        

def PLAY(name,url):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'audio')
        li = xbmcgui.ListItem('[COLOR green]PLAY[/COLOR] [COLOR yellow]%s[/COLOR]' %name, iconImage=icon, thumbnailImage=icon)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)



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



def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
              
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
print "URL: "+str(url)
print "Name: "+str(name)
########################################
if mode==None or url==None or len(url)<1:
        print ""
        INDEX()
        
elif mode==1:
        print ""+url
        LINKS(url)
        
elif mode==2:
        print ""+url
        PLAY(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

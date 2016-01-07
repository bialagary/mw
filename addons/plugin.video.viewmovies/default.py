import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,random,urlparse,mknet
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.viewmovies'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
metaset = selfAddon.getSetting('enable_meta')
net = mknet.Net()

def CATEGORIES():
        addDir2('Cinema Movies','http://www.viewmovies.tv/category/cinema-movies/?filtre=date',1,icon,'',fanart)
        addDir2('Indian Movies','http://www.viewmovies.is/category/movies/indian-movies/',1,icon,'',fanart)
        addDir2('Christmas Movies','http://www.viewmovies.is/category/movies/christmas/?filtre=date/',1,icon,'',fanart)
        addDir2('Recently Added Movies','http://www.viewmovies.is/category/movies/?filtre=date',1,icon,'',fanart)
        addDir2('Full HD Movies','http://www.viewmovies.is/category/full-hd-movies/',1,icon,'',fanart)
        addDir2('Most Viewed Movies','http://www.viewmovies.is/category/movies/?filtre=views',1,icon,'',fanart)
        addDir2('Categories','url',2,icon,'',fanart)
        addDir2('Years','url',4,icon,'',fanart)
        addDir2('Search','url',3,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')

def GETMOVIES(url,name):
        link = open_url(url)
        match=re.compile('href="(.+?)" title="(.+?)">').findall(link)[1:]
        items = len(match)
        for url,name in match:
                name2 = cleanHex(name)
                addDir(name2,url,100,'',len(match))
        try:
                match=re.compile('<a href="(.+?)">Next').findall(link)
                url= match[0]
                addDir('Next Page>>',url,1,artpath+'nextpage.png',items,isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')
        
def GENRES(url):
        addDir2('Action','http://www.viewmovies.is/category/movies/action/',1,icon,'',fanart)
        addDir2('Adventure','http://www.viewmovies.is/category/movies/adventure/',1,icon,'',fanart)
        addDir2('Animation','http://www.viewmovies.is/category/movies/animation/',1,icon,'',fanart)
        addDir2('Biography','http://www.viewmovies.is/category/movies/biography/',1,icon,'',fanart)
        addDir2('Christmas','http://www.viewmovies.is/category/movies/christmas/',1,icon,'',fanart)
        addDir2('Comedy','http://www.viewmovies.is/category/movies/comedy/',1,icon,'',fanart)
        addDir2('Crime','http://www.viewmovies.is/category/movies/crime/',1,icon,'',fanart)
        addDir2('Comedy','http://www.viewmovies.is/category/movies/comedy/',1,icon,'',fanart)
        addDir2('Docuumentary','http://www.viewmovies.is/category/movies/documentary/',1,icon,'',fanart)
        addDir2('Drama','http://www.viewmovies.is/category/movies/drama/',1,icon,'',fanart)
        addDir2('Family','http://www.viewmovies.is/category/movies/family/',1,icon,'',fanart)
        addDir2('Fantasy','http://www.viewmovies.is/category/movies/fantasy/',1,icon,'',fanart)
        addDir2('History','http://www.viewmovies.is/category/movies/history/',1,icon,'',fanart)
        addDir2('Horror','http://www.viewmovies.is/category/movies/horror/',1,icon,'',fanart)
        addDir2('Musical','http://www.viewmovies.is/category/movies/musical/',1,icon,'',fanart)
        addDir2('Mystery','http://www.viewmovies.is/category/movies//mystery/',1,icon,'',fanart)
        addDir2('Romance','http://www.viewmovies.is/category/movies/romance/',1,icon,'',fanart)
        addDir2('Sci-Fi','http://www.viewmovies.is/category/movies/sci-fi/',1,icon,'',fanart)
        addDir2('Sport','http://www.viewmovies.is/category/movies/sport/',1,icon,'',fanart)
        addDir2('Thriller','http://www.viewmovies.is/category/movies/thriller/',1,icon,'',fanart)
        addDir2('War','http://www.viewmovies.is/category/movies/war/',1,icon,'',fanart)

def YEARS():
        addDir2('2015','http://www.viewmovies.is/category/year/2015/',1,icon,'',fanart)
        addDir2('2014','http://www.viewmovies.is/category/year/2014/',1,icon,'',fanart)
        addDir2('2013','http://www.viewmovies.is/category/year/2013/',1,icon,'',fanart)
        addDir2('2012','http://www.viewmovies.is/category/year/2012/',1,icon,'',fanart)
        addDir2('2011','http://www.viewmovies.is/category/year/2011/',1,icon,'',fanart)
        addDir2('2010','http://www.viewmovies.is/category/year/2010/',1,icon,'',fanart)
        addDir2('2009','http://www.viewmovies.is/category/year/2009/',1,icon,'',fanart)
        addDir2('2005-2008','http://www.viewmovies.is/category/year/2005-2007/',1,icon,'',fanart)
        addDir2('2000-2004','http://www.viewmovies.is/category/year/2000-2004/',1,icon,'',fanart)
        addDir2('1990-1999','http://www.viewmovies.is/category/year/1990-1999/',1,icon,'',fanart)
        addDir2('1900-1989','http://www.viewmovies.is/category/movies/before-1990/',1,icon,'',fanart)
        

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search View Movies')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.viewmovies.is/?s='+ search_entered
        link = open_url(url)
        GETMOVIES(url,name)


def PLAYLINK(name,url,iconimage):
        link = open_url(url)
        try:
                url = re.compile('src="http://videomega.tv/view.php\?ref=(.+?)"').findall(link)[0]
                url = 'http://videomega.tv/view.php?ref='+url
        except:
                url = re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)"').findall(link)[0]
                url = 'http://videomega.tv/validatehash.php?hashkey='+url      
        url = urlresolver.resolve(url)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)

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

def addDir2(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true':
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            mg = metahandlers.MetaData()
            meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels= meta )
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
            

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
                
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GENRES(url)
elif mode==3: SEARCH()
elif mode==4: YEARS()
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


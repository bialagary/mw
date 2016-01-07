import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,urlresolver

addon_id = 'plugin.video.SoapCatchup'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/', ''))
base = 'http://uksoapshare.blogspot.co.uk/'

def CATEGORIES():
        link = open_url(base)
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url,name in match:
                name=name.replace("'","")
                iconimage = art + name + '.jpg'
                if not 'Now' in name:
                        if not 'Down' in name:
                                if not 'Martin' in name:
                                        if not 'Other' in name:
                                                if not 'Royal' in name:
                                                        if not 'Specials' in name:
                                                                addDir(name,url,1,iconimage,fanart)
        addDir('Neighbours','http://hdsoapcity.blogspot.co.uk/search/label/Neighbours#.VlhSDFjhDct',3,art+'Neighbours.jpg',fanart)
        addDir('Home and Away','http://hdsoapcity.blogspot.co.uk/search/label/Home%20and%20Away#.VlhTsljhDcs',3,art+'Home and Away.jpg',fanart)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]),sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def EPISODES2(name,url,iconimage):
        iconimage = art + name + '.jpg'
        link = open_url(url)
        match=re.compile("<a href='(.+?)'>(.+?)</a>").findall(link)[1:]
        for url,name in match:
                if 'HD' in name:
                    if not 'apci'in name:    
                        name = name.replace('Watch Online','').replace('HD','')
                        addLink(name,url,2,iconimage,fanart)
        try:
            np=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]  
            addDir('Older Episodes',np,1,iconimage,fanart)
        except: pass


        
def EPISODES(name,url,iconimage):
        iconimage = art + name + '.jpg'
        link = open_url(url)
        link=link.replace('"_blank"','_blank')
        match=re.compile('<a href="(.+?)" target=_blank>(.+?)</a><br />').findall(link)
        match = match[::-1]
        for url,name in match:
                name = name.replace('_',' ').replace('.mp4','').replace('.',' ').replace('x264-SS','').replace('HDTV','').replace('D A','Downton Abbey').replace('D W','Doctor Who')
                if 'huge' in url:
                        addLink(name,url,2,iconimage,fanart)

def PLAYEP(name,url,iconimage):
        if urlresolver.HostedMediaFile(url).valid_url():
                stream_url = urlresolver.HostedMediaFile(url).resolve()
        else:
                link = open_url(url)
                url=re.compile('src="(.+?)"></iframe>').findall(link)[0]
                url=url.split('?autoplay')[0]
                link = open_url(url)
                streamurl = re.compile('mp4","url":"(.+?)"').findall(link)[-1]
                stream_url=streamurl.replace('\\/','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
    
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

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    link=cleanHex(link)
    response.close()
    return link

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON2.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON2.getSetting(viewType) )

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
elif mode==1: EPISODES(name,url,iconimage)
elif mode==2: PLAYEP(name,url,iconimage)
elif mode==3: EPISODES2(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


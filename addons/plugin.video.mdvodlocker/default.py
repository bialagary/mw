import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers

#VODLOCKER - By Mucky Duck (03/2015)
addon_id='plugin.video.mdvodlocker'
addon = Addon(addon_id, sys.argv)
selfAddon = xbmcaddon.Addon(id=addon_id)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
datapath = addon.get_profile()
local = xbmcaddon.Addon(id=addon_id)
baseurl2 = 'http://www.vodlockerx.com'
metaset = selfAddon.getSetting('enable_meta')
#metaget = metahandlers.MetaData(preparezip=False)
net = Net()


#######################################################VODLOCKERMOVMOVIES####################################################


def VODLOCKER():
        addDir2('[B][COLOR cyan]New[/COLOR][/B]',baseurl2+'/movies',42,'http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/New%20Releases.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]IMDB Rating[/COLOR][/B]',baseurl2+'/movies/imdb_rating',42,art+'IMDB-Black.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Genres[/COLOR][/B]',baseurl2+'/movies',44,'http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/Movies%20by%20Genre.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]A/Z[/COLOR][/B]',baseurl2+'/movies/abc',42,'http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/A-Z.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Search[/COLOR][/B]','url',46,'http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/DeLorean.png',art+'abstract.jpg','')




def VLMINDEXM(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="link" href="(.+?)" title="(.+?)">').findall(link)
        items = len(match)
        for url,name in match:
                addDir(name,url,43,'',items)
        try:
                match=re.compile('<li><a href="(.+?)">.+?</a></li>').findall(link)
                url= match[-1]
                addDir('[B][COLOR maroon]Next Page >>>[/COLOR][/B]',url,42,'',items)
        except: pass

        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def getMeta( name, year):
    mg = metahandlers.MetaData()
    meta = mg.get_meta('movie', name=name, year=year)
    return meta


def VLMHOSTS(url,name,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<span>.+?</span></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</h5>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<ul class="filter" style="width:200px;float:right;margin-top: 0px;">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li class="current right" style="float:right"><a href="(.+?)" target="_blank">').findall(net.http_GET(url).content)
        for url in match:
                nono = 'idownloadplay.com'
                if nono not in url:
                        addDir(name,url,100,'',len(match))
                        print url




def VLMGENRES(url):
        addDir2('[B][COLOR cyan]Action[/COLOR][/B]',baseurl2+'/movie-tags/action',42,art+'Action-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Adventure[/COLOR][/B]',baseurl2+'/movie-tags/adventure',42,art+'Adventure-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Animation[/COLOR][/B]',baseurl2+'/movie-tags/animation',42,art+'Animated-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Biography[/COLOR][/B]',baseurl2+'/movie-tags/biography',42,art+'Biography-movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Comedy[/COLOR][/B]',baseurl2+'/movie-tags/comedy',42,art+'Comedy-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Crime[/COLOR][/B]',baseurl2+'/movie-tags/crime',42,art+'Crime-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Documentary[/COLOR][/B]',baseurl2+'/movie-tags/documentary',42,art+'Documentaries.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Drama[/COLOR][/B]',baseurl2+'/movie-tags/drama',42,art+'Drama-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Family[/COLOR][/B]',baseurl2+'/movie-tags/family',42,art+'Family-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Fantasy[/COLOR][/B]',baseurl2+'//movie-tags/fantasy',42,art+'Fantasy-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]History[/COLOR][/B]',baseurl2+'/movie-tags/history',42,art+'Historic-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Horror[/COLOR][/B]',baseurl2+'/movie-tags/horror',42,art+'Horror-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Music[/COLOR][/B]',baseurl2+'/movie-tags/music',42,art+'Music-icon.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Musical[/COLOR][/B]',baseurl2+'/movie-tags/musical',42,art+'Musical-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Mystery[/COLOR][/B]',baseurl2+'/movie-tags/mystery',42,art+'Mystery-Movies.ico',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Romance[/COLOR][/B]',baseurl2+'/movie-tags/romance',42,art+'Romantic-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Sci-Fi[/COLOR][/B]',baseurl2+'/movie-tags/sci-fi',42,art+'Sci-Fi-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Short[/COLOR][/B]',baseurl2+'/movie-tags/short',42,art+'Short-Film-movies.Png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Sport[/COLOR][/B]',baseurl2+'/movie-tags/sport',42,art+'Sports-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Thriller[/COLOR][/B]',baseurl2+'/movie-tags/thriller',42,art+'Thriller-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]War[/COLOR][/B]',baseurl2+'/movie-tags/war',42,art+'War-Movies.png',art+'abstract.jpg','')
        addDir2('[B][COLOR cyan]Western[/COLOR][/B]',baseurl2+'/movie-tags/western',42,art+'Western-Movies.png',art+'abstract.jpg','')




def VLTOPM(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.+?)" title="(.+?)" alt=".+?" class="smposter" align="left" /></a>\n<a href="(.+?)">.+?</a><br>\n<span class="highlight">(.+?)</span> <span class="rating">(.+?)</span><br>\n<span class="highlight">.+?</span>(.+?)<br>').findall(link)
        for thumbnail,name,url,rating,score,release in match:
                addDir('%s (%s %s -%s)' %(name,rating,score,release),url,23,thumbnail,'')




def VODLOCKERSEARCH():
        keyb = xbmc.Keyboard('', 'Search Vodlocker')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                #encode=urllib.quote(search)
                #print encode
                url = baseurl2+'/index.php?menu=search&query='+search
                print url
                match=re.compile('<a class="link" href="(.+?)" title="(.+?)">').findall(net.http_GET(url).content) 
                for url,name in match:
                        ok = '/movie'
                        if ok in url:
                                name = name.encode('ascii', 'ignore')
                                addDir(name,url,43,'',len(match))




def RESOLVE(name,url,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        print streamlink
        url = streamlink
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(streamlink,liz,False)




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
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def addDir(name,url,mode,iconimage,itemcount):
        if metaset=='true':
                metaget = metahandlers.MetaData()
                meta = metaget.get_meta('movie', name, '')
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
                liz.setInfo( type="Video", infoLabels= meta )
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                if mode==100:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok
        else:
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty('fanart_image', fanart)
                if mode==100:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok




def addDir2(name,url,mode,iconimage,fanart,description):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addDir3(name,url,mode,iconimage,itemcount):
        if metaset=='true':
                splitName=name.partition('(')
                simplename=""
                simpleyear=""
                if len(splitName)>0:
                        simplename=splitName[0]
                        simpleyear=splitName[2].partition(')')
                if len(simpleyear)>0:
                        simpleyear=simpleyear[0]
                meta = metaget.get_meta('tvshow', simplename ,simpleyear)
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
                liz.setInfo( type="Video", infoLabels= meta )
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                if mode==100:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok
        else:
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty('fanart_image', fanart)
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)




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
########################################
if mode==None or url==None or len(url)<1:
        print ""
        VODLOCKER()

elif mode==42:
        print ""+url
        VLMINDEXM(url,name)

elif mode==43:
        print ""+url
        VLMHOSTS(url,name,iconimage)

elif mode==44:
        print ""+url
        VLMGENRES(url)

elif mode==45:
        print ""+url
        VLTOPM(url)

elif mode==46:
        VODLOCKERSEARCH()
#########################
elif mode==100:
        print ""+url
        RESOLVE(name,url,iconimage)
#########################
xbmcplugin.endOfDirectory(int(sys.argv[1]))

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,urlresolver,random
from resources.libs.common_addon import Addon
from metahandler import metahandlers
exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("OSAgICAgICAgPSAnNWYuMmEuNTMnCmUgICAgICAgPSAzNC4yZig3Zj05KQoyNiAgICAgICAgICAgPSAyZig5LCA3YS43MSkKMjEgICAgICAgICAgPSAxZi5kKDVlLjU3LjFlKCcxMTovLzFkLzE1LycgKyA5ICwgJzIxLjc4JykpCjQzICAgICAgICAgICAgPSAxZi5kKDVlLjU3LjFlKCcxMTovLzFkLzE1LycgKyA5LCAnNDMuNTknKSkKMmMgICAgICA9IDFmLmQoNWUuNTcuMWUoJzExOi8vMWQvMTUvJyArIDksICcyMi41OScpKQo0NSAgICAgICAgID0gJzI6Ly8zNy4wLjcvMS8xMC42Jwo0NCAgICAgICAgPSBlLmYoJzZmJykKMzIgICAgICAgPSBlLmYoJzNkJykKMTYgICAgICAgPSAyNi40OS43YignMTYnLCAnJykKNDcgICAgICAgICA9IGUuZignMjQnKQo1YyA9JzJlOi8vMzcuMTQuNWEvMTkvNzIvMjI/ODA9Jwo1ZCA9JyYyOT03ZCYzZT0xOCY3Yz02MiY2MT1hJjc3PTJhJjEzPTUwJwo3NCA9ICcyZTovLzM3LjE0LjVhLzE5LzcyLzFhPzNlPTE4JjJiPScKNjQgPSAnJjEzPTUwJjYxPWInCjMxID0gWycyOi8vMC43LzEvMjcuNicsCgknMjovLzAuNy8xLzI1LjYnLAoJJzI6Ly8wLjcvMS83ZSU3Ni8xMC42JywKCScyOi8vMC43LzEvNDIvMTAuNicsCgknMjovLzAuNy8xLzc1LzEwLjYnLAoJJzI6Ly8wLjcvMS80Yi42JywKCScyOi8vMC43LzEvNDEuNicsCgknMjovLzAuNy8xLzZhLzEwLjYnLAoJJzI6Ly8wLjcvMS83My42JywKCScyOi8vMC43LzEvMzUuNicsCgknMjovLzAuNy8xLzIzLjYnLAoJJzI6Ly8wLjcvMS9jLzMlNjglNjUlNS42JywKCScyOi8vMC43LzEvNC8zJTY2JTUuNicsCgknMjovLzAuNy8xLzQvMyU2NyU1LjYnLAoJJzI6Ly8wLjcvMS80LzMlNmIlNmUlNS42JywKCScyOi8vMC43LzEvNC8zJTFiJTYwJTIwJiUxYiU1NiUxMiU4LjYnLAoJJzI6Ly8wLjcvMS80LzMlNTElNWIlNS42JywKCScyOi8vMC43LzEvNC8zJTcwJTUuNicsCgknMjovLzAuNy8xLzQvMyUzOCU1LjYnLAoJJzI6Ly8wLjcvMS80LzMlNTIlMjAmJTU1JTUuNicsCgknMjovLzAuNy8xLzQvMyUzMyU1NCU1LjYnLAoJJzI6Ly8wLjcvMS80Lzc5JTNmJTM2JTEyJTguNicsCgknMjovLzAuNy8xLzQvMyA2ZCA0ZiA2OSAyZC42JywKCScyOi8vMC43LzEvYy8zJTM5JTNhJTUuNicsCgknMjovLzAuNy8xLzQvMyU0OCU0ZSU1LjYnLAoJJzI6Ly8wLjcvMS9jLzMlM2IlMjAmJTQ2JTEyJTguNicsCgknMjovLzAuNy8xLzQvNmMuNicsCgknMjovLzAuNy8xLzQvMyUzYyU0MCU1LjYnLAoJJzI6Ly8wLjcvMS80LzRkLjYnLAoJJzI6Ly8wLjcvMS80LzRhLjYnLAoJJzI6Ly8wLjcvMS80LzU4LjYnLAoJJzI6Ly8wLjcvMS80LzMlMWMlMTclMzAlNS42JywKCScyOi8vMC43LzEvNC8zJTFjJTE3JTUuNicsCgknMjovLzAuNy8xLzQvNjMuNicsCgknMjovLzAuNy8xLzQvMyUyOCU1LjYnLAoJJzI6Ly8wLjcvMS80LzMlNGMlOC42JwoJXQ==")))(lambda a,b:b[int("0x"+a.group(1),16)],"metalkettle|UKTurk2|http|Classic|movies|20Movies|txt|co|20Collection|addon_id|AIzaSyA7v1QOHz8Q4my5J8uGSpr0zRrntRjnMmk|AIzaSyBAdxZCHbeJwnQ7dDZQJNfcaF46MdqJ24E|nonmetaMovies|translatePath|selfAddon|getSetting|Index|special|20Movie|maxResults|googleapis|addons|iconimage|20Disney|snippet|youtube|playlistItems|20Star|20Walt|home|join|xbmc|20|fanart|search|TurkishFilms|enable_meta|EnglishList|addon|SportsList|20Football|regionCode|video|playlistId|searchicon|Collection|https|Addon|20Animated|searchlist|adultpass|20Martial|xbmcaddon|TurkishTV|20Classic|www|20Western|20Charlie|20Chaplin|20Laurel|20Norman|password|part|20Craven|20Wisdom|Concerts|cartoons|icon|adultopt|baseurl|20Hardy|metaset|20Jerry|queries|CarryOn|Standup|20Bonus|WillHay|20Lewis|Presley|50|20James|20Mafia|ukturk|20Arts|20Gang|20Trek|path|Ealing|png|com|20Bond|ytapi1|ytapi2|os|plugin|20Wars|key|en_US|Pixar|ytpl2|2050s|2080s|2090s|20Pre|Movie|radio|20Box|Abbot|Elvis|20Set|adult|20War|argv|v3|CCTV|ytpl|docs|20shows|type|jpg|Wes|sys|get|hl|US|tv|id|q".split("|")))

def Search():
        keyb = xbmc.Keyboard('', 'Search UK Turk')
        keyb.doModal()
        if (keyb.isConfirmed()):
                searchterm=keyb.getText()
                searchterm=searchterm.upper()
        else:quit()
        for item in searchlist:
                link=open_url(item)
                match=re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"',re.DOTALL).findall(link)
                if len(match)>0:
                        for name,url,thumb in match:
                                if 'ImageH' in thumb:thumb=searchicon
                                normname=name
                                name=name.upper()
                                if searchterm in name and not 'COLOR' in name:
                                        if 'txt' in url:
                                                addDir(normname,url,3,thumb,fanart)
                                        if 'youtube.com/playlist?list=' in url:
                                                addDir(normname,url,3,thumb,fanart)
                                        if 'youtube.com/results?search_query=' in url:
                                                addDir(normname,url,3,thumb,fanart)      
                                        else:addLink(normname,url,3,thumb,fanart)                                
                match2=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
                if len(match2)>0:
                        for name,url,thumb in match2:
                                if 'ImageH' in thumb:thumb=searchicon
                                normname=name
                                name=name.upper()
                                if searchterm in name and not 'COLOR' in name:
                                        if 'txt' in url:
                                                addDir(normname,url,3,thumb,fanart)
                                        if 'youtube.com/playlist?list=' in url:
                                                addDir(normname,url,3,thumb,fanart)
                                        if 'youtube.com/results?search_query=' in url:
                                                addDir(normname,url,3,thumb,fanart)      
                                        else:addLink(normname,url,3,thumb,fanart)
                           
def Index():
        link=open_url(baseurl)	
	match=re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"',re.DOTALL).findall(link)
	for name,url,iconimage in match:
                if not 'XXX' in name:
                        addDir(name,url,1,iconimage,fanart)
                if 'XXX' in name:
                        if adultopt == 'true':
                                if adultpass == '':
                                    dialog = xbmcgui.Dialog()
                                    ret = dialog.yesno('Adult Content', 'You have opted to show adult content','','Please set a password to prevent accidental access','Cancel','Lets Go')
                                    if ret == 1:
                                        keyb = xbmc.Keyboard('', 'Set Password')
                                        keyb.doModal()
                                        if (keyb.isConfirmed()):
                                            
                                            passw = keyb.getText()
                                             
                                            selfAddon.setSetting('password',passw)
                                             
                                        addDir(name,url,1,iconimage,fanart)
                        if adultopt == 'true':
                                if adultpass <> '':
                                        addDir(name,url,1,iconimage,fanart)
        addDir('Search','url',4,'http://icons.iconarchive.com/icons/uriy1966/steel-system/512/Search-icon.png',fanart)
        addLink('UK Turk Twitter Feed','url',2,'http://www.metalkettle.co/UKTurk/thumbs/twitter.jpg',fanart)
      
def GetChans(name,url,iconimage):
        if 'Index' in url:
                GetIndex(url)      
        if 'XXX' in url:
                if adultpass <> '':
                        dialog = xbmcgui.Dialog()
                        ret = dialog.yesno('Adult Content', 'Please enter the password you set','to continue','','Cancel','Show me the money')
                        if ret == 1:
                           try:     
                              keyb = xbmc.Keyboard('', 'Set Password')
                              keyb.doModal()
                              if (keyb.isConfirmed()):
                                    passw = keyb.getText()
                              if passw == adultpass:
                                channels = GetContent(url)
                                for name,url,icon in channels:
                                        addLink(name,url,3,iconimage,fanart)
                           except:pass                 
        if 'movies' in url:
                channels = GetContent(url)
                cnt = len(channels)
                for name,url,icon in channels:
                        addLinkMeta(name,url,3,iconimage,cnt,isFolder=False)
                if 'Index' in url:
                        xbmc.executebuiltin('Container.SetViewMode(50)')              
        elif 'XXX' not in url:
                burl = url
                link=open_url(url)
                match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(link)
                for item in match:
                        links=re.compile('<link>(.+?)</link>').findall(item)
                        if len(links)==1:
                                channels=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>',re.DOTALL).findall(item)
                                for name,url,icon in channels:
                                        if 'youtube.com/results?search_query=' in url:
                                                addDir(name,url,3,icon,fanart)
                                        elif 'youtube.com/playlist?list=' in url:
                                                addDir(name,url,3,icon,fanart)
                                        else:
                                                if 'txt' in url:
                                                        addDir(name,url,3,icon,fanart)
                                                else:
                                                        if 'ImageH' in icon:
                                                                addLink(name,url,3,iconimage,fanart)
                                                        else:addLink(name,url,3,icon,fanart)
                        else:
                                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                addLink(name,burl,5,iconimage,fanart)

def GETMULTI(name,url,iconimage):
        streamurl=[]
        streamname=[]
        streamicon=[]
        link=open_url(url)
        link=re.sub(r'\(.*\)', '', link)
        name=re.sub(r'\(.*\)', '', name)
        urls=re.compile('<item>.+?<title>'+name+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
        links=re.compile('<link>(.+?)</link>').findall(urls)
        i=1
        for sturl in links:
                streamurl.append( sturl )
                streamname.append( 'Link '+str(i) )
                dialog = xbmcgui.Dialog()
                i=i+1
        select = dialog.select(name,streamname)
        if select == -1:
                quit()
        else:
                url = streamurl[select]
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
                liz.setPath(url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
      
def GetIndex(url):
        link=open_url(url)	
	match=re.compile('name="(.+?)".+?url="(.+?)".+?img="(.+?)"',re.DOTALL).findall(link)
	for name,url,icon in match:
                if 'youtube.com/playlist?list=' in url:
                        addDir(name,url,3,icon,fanart)
                elif 'youtube.com/results?search_query=' in url:
                        addDir(name,url,3,icon,fanart)
                else:
                        addDir(name,url,1,icon,fanart)

def GetContent(url):
        link=open_url(url)	
	list=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?humbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
	return list         
             
def PLAYLINK(url,name,iconimage):
        
            try:
                    if 'search' in iconimage:iconimage=icon
            except:pass
            if 'txt' in url:
                    GetChans(name,url,iconimage)
            else:
                    if 'youtube.com/results?search_query=' in url:
                        searchterm = url.split('search_query=')[1]
                        ytapi = ytapi1 + searchterm + ytapi2
                        req = urllib2.Request(ytapi)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        link = link.replace('\r','').replace('\n','').replace('  ','')
                        match=re.compile('"videoId": "(.+?)".+?"title": "(.+?)"',re.DOTALL).findall(link)
                        for ytid,name in match:
                                url = 'https://www.youtube.com/watch?v='+ytid
                                addLink(name,url,3,iconimage,fanart)
                    elif 'youtube.com/playlist?list=' in url:
                        searchterm = url.split('playlist?list=')[1]
                        ytapi = ytpl + searchterm + ytpl2
                        req = urllib2.Request(ytapi)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        link = link.replace('\r','').replace('\n','').replace('  ','')
                        match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
                        for name,ytid in match:
                                url = 'https://www.youtube.com/watch?v='+ytid
                                addLink(name,url,3,iconimage,fanart)
                    else:
                        if urlresolver.HostedMediaFile(url).valid_url():
                                streamurl = urlresolver.HostedMediaFile(url).resolve()
                        else: streamurl=url
                        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                        liz.setInfo( type="Video", infoLabels={ "Title": name} )
                        liz.setPath(streamurl)
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                      
#################################################################################           
def TWITTER():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
        req = urllib2.Request(twit)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = link.replace('/n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            try:
                            status = status.decode('ascii', 'ignore')
            except:
                            status = status.decode('utf-8','ignore')
            dte = dte[:-15]
            status = status.replace('&amp;','')
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR blue][B]@uk_turk[/B][/COLOR]', text)

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
                                     
def open_url(url):
        url += '?%d=%d' % (random.randint(1, 10000), random.randint(1, 10000))
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link = link.replace('\r','').replace('\t','').replace('&nbsp;','').replace('\'','')
        response.close()
        return link

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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        if not mode==2:
                liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
                liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addLinkMeta(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true':
          if not 'COLOR' in name:
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
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
            liz.setInfo( type="Video", infoLabels= meta )
            liz.setProperty("IsPlayable","true")
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
            liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
        
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
 
 
if mode==None or url==None or len(url)<1: Index()
elif mode==1:GetChans(name,url,iconimage)
elif mode==2:TWITTER()
elif mode==3:PLAYLINK(url,name,iconimage)
elif mode==4:Search()
elif mode==5:GETMULTI(name,url,icon)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

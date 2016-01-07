import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import random
import HTMLParser

ADDON = xbmcaddon.Addon(id='plugin.audio.worldradio')


PLAYLIST_PREFIXES = ('m3u', 'pls', 'asx', 'xml')

def CATEGORIES():

    response=OPEN_URL('http://www.listenlive.eu')
   
    match=re.compile('<img width="8".+?<a href="(.+?)">(.+?)</a>').findall(response)

    for url , name  in match :
        name= HTMLParser.HTMLParser().unescape(name)
        icon = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.worldradio/flags', name+'.GIF'))
        
        if not 'external services'  in name.lower():   
            addDir(name,url,1,icon,'')
     
                 
    setView('movies', 'default') 

def GET_RADIO(name,url,iconimage):
    xunity='http://www.listenlive.eu/%s' % url
    response=OPEN_URL(xunity).replace('\n','')
    try:
        response=response.split('<td class="header"><b>Format/Comments</b></td></tr>')[1]
    except:pass    
    match=re.compile('<b>(.+?)</b>.+?<a href="(.+?)"').findall(response)

    for name , url  in match :
        if not 'http:' or not 'Stream types' in name:
            
            addDir(name,url,200,iconimage,'')
                 
    setView('movies', 'default') 

def resolve_playlist(stream_url):
    print'CHECKING :'+stream_url
    servers = []
    if stream_url.lower().endswith('m3u'):
        response = OPEN_URL(stream_url)
        servers = [
            l for l in response.splitlines()
            if l.strip() and not l.strip().startswith('#')
        ]
    elif stream_url.lower().endswith('pls'):
        response = OPEN_URL(stream_url)
        servers = [
            'http://'+l.split('http://')[1].split('\n')[0]
            for l in response.splitlines() if 'http' in l
        ]
    elif stream_url.lower().endswith('asx'):
        response = OPEN_URL(stream_url)
        servers = [
            l.split('href="')[1].split('"')[0]
            for l in response.splitlines() if 'href' in l
        ]
    if servers:
          
        return random.choice(servers)    
    return stream_url       
               
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
    if '.m3u' in url or '.pls' in url or '.asx' in url:
        url=resolve_playlist(url)
        
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':name, 'Artist':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
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


                      


def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True     
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('music', {'Title':name, 'Artist':name})
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
                

        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
    print ""
    CATEGORIES()
   
elif mode==1:
    GET_RADIO(name,url,iconimage)

    
elif mode==200:
    PLAY_STREAM(name,url,iconimage)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

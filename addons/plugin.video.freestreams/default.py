import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.freestreams')
datapath = xbmc . translatePath ( ADDON . getAddonInfo ( 'profile' ) )
pak = os. path . join ( datapath , "pak" )



def CATEGORIES():
            
    aa=open(pak).read()
    link=aa.split('<items>')
    for p in link:
        try:
            name=re.compile('<programTitle>(.+?)</programTitle>').findall(p)[0]
            URL=re.compile('<programURL>(.+?)</programURL>').findall(p)[0]
            iconimage=re.compile('<programImage>(.+?)</programImage>').findall(p)[0]
            if not 'Movies' in p:
                addDir(name,URL,200,iconimage)
        except:pass
        
    
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default') 
       
       
                                                                      
def GetContent(url):
    aa=open(pak).read()
    link=aa.split('<items>')
    for p in link:
        try:
            name=re.compile('<programTitle>(.+?)</programTitle>').findall(p)[0]
            URL=re.compile('<programURL>(.+?)</programURL>').findall(p)[0]
            iconimage=re.compile('<programImage>(.+?)</programImage>').findall(p)[0]
            if '<programCategory>'+url in p:
                addDir(name,URL,200,iconimage)
        except:pass
               
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def auth():
 import base64
 import time
 TIME = time.time()
 second= str(TIME).split('.')[0]
 first =int(second)+69296929
 token=base64.b64encode('%s@2nd2@%s' % (str(first),second))    
 DATA_URL='https://app.dynns.com/keys/activate.php?token='+token
 request = urllib2.Request(DATA_URL)
 base64string = 'ZGlsZGlsZGlsOlBAa2lzdEBu'
 request.add_header("Authorization", "Basic %s" % base64string)   
 return urllib2.urlopen(request).read()
    

    
    
def PLAY_STREAM(name,url,iconimage):
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url+auth())
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

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        menu = []
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        GetContent(url)
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

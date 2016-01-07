import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json
import base64

ADDON = xbmcaddon.Addon(id='plugin.video.tvplayer')

if ADDON.getSetting('token')=='':

     DATA_URL='http://xty.me/xunitytalk/addons/plugin.video.tvplayer/config.txt'
     request = urllib2.Request(DATA_URL)
     link = urllib2.urlopen(request).read()
     token=re.compile('token="(.+?)"').findall(link)[0]
     expiry=re.compile('expiry="(.+?)"').findall(link)[0]
     referer=re.compile('referer="(.+?)"').findall(link)[0]
     ADDON.setSetting('token',token)
     ADDON.setSetting('expiry',expiry)
     ADDON.setSetting('referer',referer)
 

def CATEGORIES():
   

    response=OPEN_URL('http://lapi.cdn.uk.tvplayer.com/json/tvp/now.json')
    
    link=json.loads(response)

    data=link['data']
    

    for field in data:
        name   = field['channel']['name'].encode("utf-8")+' - [COLOR white]'+field['now']['title'].encode("utf-8")+'[/COLOR]'
        desc   = field['now']['desc'].encode("utf-8")
        status = field['channel']['status']
        try: NEXT   = desc + '\n\n[COLOR white]NEXT:\n'+field['next']['title'].encode("utf-8") +'[/COLOR]'
        except:NEXT=''
        id=field['channel']['id']
        
        if status=='online':
            icon='http://static.simplestream.com/tvplayer/logos/150/Inverted/%s.png' % id    
            addDir(name,id,200,icon,NEXT)
    if ADDON.getSetting('sort')== 'true':    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             
    setView('movies', 'default') 
       
               
 
 
def OPEN_URL(url):
    if ADDON.getSetting('proxy')== 'true':
            import base64
            
            try:
                print 'RESOLVING JUSTIN'
                print 'http://www.joeproxy.co.uk/index.php?q='+base64.b64encode(url)
                req = urllib2.Request('http://www.joeproxy.co.uk/index.php?q='+base64.b64encode(url))
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)                  
            except:
                print 'RESOLVING OPENPROXY'
                url=url.split('http')[1]
                req = urllib2.Request('http://www.openproxy.co.uk/browse.php?u='+base64.b64encode(url)+'=&b=13&f=norefer')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                req.add_header('Referer', 'http://www.openproxy.co.uk/')
                response = urllib2.urlopen(req)                
    else:                                      
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def OPEN_URL_STREAM_URL(url):
    import time
    timestamp =int(time.time()) + 4 * 60 * 60
    header={'Token':ADDON.getSetting('token'),'Token-Expiry': ADDON.getSetting('expiry'),'Referer':ADDON.getSetting('referer'),'User-Agent': 'iPhone/iOS 8.4 (iPhone; U; CPU iPhone OS 8_4 like Mac OS X;)'}
    req = urllib2.Request(url,headers=header)
    
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    cookie=response.info()['Set-Cookie']               
    return link ,cookie

    
def PLAY_STREAM(name,url,iconimage):
    url='http://live.tvplayer.com/stream-ios-encrypted.php?id=%s' % url
    
    response,cookie=OPEN_URL_STREAM_URL(url)    
    
    link=json.loads(response)

    
     
    stream=link['tvplayer']['response']['stream']

    

    server='http://'+re.compile('http://(.+?)/').findall (stream)[0]

    m3u8=OPEN_URL(stream)+'\n'
  
    URL=[]    
    if not 'chunklist' in  m3u8 :
        #M3U8_PATH=xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'yo.m3u8'))
        if not 'http' in m3u8:
            bw=re.compile('BANDWIDTH=(.+?(,|\n))').findall(m3u8)
            for quality,fuckall in bw:
                grrrrr=quality.replace(',','').replace('\n','')
                URL.append(eval(grrrrr))
                       
            hello= max(URL)         
            m3u8=m3u8.split(str(hello))[1]            
            match=re.compile('\n(.+?)\n').findall (m3u8)[0]
            g=server+match
        else:
            bw=re.compile('BANDWIDTH=(.+?(,|\n))').findall(m3u8)
            for quality,fuckall in bw:
                grrrrr=quality.replace(',','').replace('\n','')
                URL.append(eval(grrrrr))

                       
            hello= hello= max(URL)
            m3u8=m3u8.split(str(hello))[1]               
            match=re.compile('http://(.+?)\n').findall (m3u8)
            amount =len(match)-1
            g='http://'+match[amount]
            
        M3U8_PATH=g
    else:
            
            M3U8_PATH=stream
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(M3U8_PATH+'|Cookie='+cookie)
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
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
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
       

elif mode==200:

        PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

#MD3-Audio - By Mucky Duck (12/05/2015)

addon_id = 'plugin.audio.MD3-Audio'
plugin = xbmcaddon.Addon(id=addon_id)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
baseurl = 'http://www.itemvn.com'
single = 'http://www.itemvn.com/song/?s='
web = 'http:'
net = Net()

def CATEGORIES():
#        addDir('[B][COLOR yellow]Artists A/Z[/COLOR][/B]',baseurl,10,icon,fanart,'')
        addDir('[B][COLOR yellow]Bestsellers[/COLOR][/B]',baseurl+'/bestsellers',11,icon,fanart,'')
        addDir('[B][COLOR yellow]Billboard Top 10[/COLOR][/B]',baseurl+'/hot100',8,icon,fanart,'')
        addDir('[B][COLOR yellow]Browse Songs[/COLOR][/B]',baseurl+'/browse_songs',9,icon,fanart,'')
        addDir('[B][COLOR yellow]Genre[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR yellow]Hot Artists[/COLOR][/B]',baseurl+'/topartists',12,icon,fanart,'')
        addDir('[B][COLOR yellow]Just Added[/COLOR][/B]',baseurl+'/justadded',1,icon,fanart,'')
        addDir('[B][COLOR yellow]Suggestions[/COLOR][/B]',baseurl+'/artist/?s=95D51AC15B',13,icon,fanart,'')
        
        
        
        
def ALBUM(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<title>(.+?)</title>\r\n\t\t\t\t\t\t<META NAME="description" CONTENT=".+?">').findall(link)
        match2=re.compile('<a href=\'(.+?)\'><img src=".+?" id=".+?" class="artist_image_large" data-src="(.+?)" alt="(.+?)" />').findall(link)
        match3=re.compile("<a href='(.+?)'.+?>Next</a>").findall(link)
        for name in match1:
                name = name.replace('100','10')
                name = name.replace('- Itemvn','')
                addDir('[B][COLOR green]%s[/COLOR][/B]' %name,'url',None,icon,fanart,'')
        for url,thumb,name in match2:
                name = name.replace('&amp;','&')
                name = name.replace('Album Photo','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,6,web+thumb,fanart,'')
        for url in match3:
                addDir('[B][COLOR green]Next Page>>[/COLOR][/B]' ,baseurl+url,1,icon,fanart,'')

def XMLTRACK(url,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<object width="650" height="300">\r\n                                                            <param name="movie" value="(.+?)"></param>').findall(link)
        for url in match:
                url = url.replace('MPlayer.swf?configURL=','')
                url = url.replace('&autoPlay=false','')
                addDir('[COLOR yellow]%s[/COLOR]' %name,baseurl+url,7,iconimage,fanart,'')

def TRACK(url,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<title>(.+?)</title>\r\n    <length>.+?</length>\r\n    <fileName>(.+?)</fileName>').findall(link)
        for name,url in match:
                name = name.replace('&amp;','&')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,single+url,2,iconimage,fanart,'')


def FLINK(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<audio id="ap" src="(.+?)" style="width:100%" controls="controls" autoplay="autoplay" loop="loop" preload="auto">Your browser does not support the audio element.</audio>').findall(link)
        for url in match:
                PLAY(name,url)

def BILL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<title>(.+?)</title>\r\n\t\t\t\t\t\t<META NAME="description" CONTENT=".+?">').findall(link)
        match1=re.compile('<a class="albumcover" href=\'(.+?)\' onmouseover=".+?" onmouseout=".+?">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t                            <img src="(.+?)" id=".+?" class=".+?" alt="(.+?)" />').findall(link)
        match2=re.compile("<a href='(.+?)'.+?>Next</a>").findall(link)
        for name in match:
                name = name.replace('100','10')
                name = name.replace('- Itemvn','')
                addDir('[B][COLOR green]%s[/COLOR][/B]' %name,'url',None,icon,fanart,'')
        for url,thumb,name in match1:
                name = name.replace('&amp;','&')
                name = name.replace('Album Photo','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,2,web+thumb,fanart,'')
        for url in match2:
                addDir('[B][COLOR green]Next Page>>[/COLOR][/B]' ,baseurl+url,8,icon,fanart,'')


def SEARCHS(url):
        keyb = xbmc.Keyboard('', 'Search DnB-Sets')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                print encode
                url = baseurl+'/listsong/?keyword='+encode
                print url
                match=re.compile('<a id=".+?" class="artist_underline" href="(.+?)">(.+?)</a>').findall(net.http_GET(url).content) 
                for name,url in match:
                        name = name.replace('<font color=fff788><u>','')
                        name = name.replace('</u></font>','')
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,2,icon,fanart,'')


def GENRE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<td><a href="(.+?)" id=".+?" class="menu_genre_item"><div>(.+?)</div></a></td>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                url = url.replace(' ','%20')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')


def BROWSE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<title>(.+?)</title>\r\n\t\t\t\t\t\t<META NAME="description" CONTENT=".+?">').findall(link)
        match1=re.compile('<a id=".+?" class="artist_underline" href="(.+?)">(.+?)</a>').findall(link)
        match2=re.compile("<a href='(.+?)'.+?>Next</a>").findall(link)
        for name in match:
                name = name.replace('100','10')
                name = name.replace('- Itemvn','')
                addDir('[B][COLOR green]%s[/COLOR][/B]' %name,'url',None,icon,fanart,'')
        for url,name in match1:
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,2,icon,fanart,'')       
        for url in match2:
                addDir('[B][COLOR green]Next Page>>[/COLOR][/B]' ,baseurl+url,9,icon,fanart,'')


def ARTISTAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" id=".+?" class="search_letter">(.+?)</a>').findall(link)
        for url,name in match:
                name = name.replace('#','0/9')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')

def BESTSELLER(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<title>(.+?)</title>\r\n\t\t\t\t\t\t<META NAME="description" CONTENT=".+?">').findall(link)
        match1=re.compile('<a href=\'(.+?)\'><img src="(.+?)" id=".+?" class="album_image_large" alt="(.+?)" />').findall(link)
        for name in match:
                name = name.replace('Billboard 200 - ','')
                name = name.replace('- Itemvn','')
                addDir('[B][COLOR green]%s[/COLOR][/B]' %name,'url',None,icon,fanart,'')
        for url,thumb,name in match1:
                name = name.replace('&amp;','&')
                name = name.replace('Album Photo','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,6,web+thumb,fanart,'')

def HOTARTIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<title>(.+?)</title>\r\n\t\t\t\t\t\t<META NAME="description" CONTENT=".+?">').findall(link)
        match1=re.compile('<a href=\'(.+?)\'><img src="(.+?)" id=".+?" class="album_image_large" alt="(.+?)" />').findall(link)
        for name in match:
                name = name.replace('Billboard 200 - ','')
                name = name.replace('- Itemvn','')
                addDir('[B][COLOR green]%s[/COLOR][/B]' %name,'url',None,icon,fanart,'')
        for url,thumb,name in match1:
                name = name.replace('&amp;','&')
                name = name.replace('Album Photo','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,1,web+thumb,fanart,'')

def SUGGEST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href=\'(.+?)\'><img src=".+?" id=".+?" class="artist_image_medium" data-src="(.+?)" alt="(.+?)" />').findall(link)
        for url,thumb,name in match:
                name = name.replace('&amp;','&')
                name = name.replace('Album Photo','')
                name = name.replace('Photo','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,1,web+thumb,fanart,'')
                

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


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
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
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

########################################
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==1:
        print ""+url
        ALBUM(url)

elif mode==2:
        print ""+url
        FLINK(url)

elif mode==3:
        print ""+url
        PLAY(name,url)

elif mode==4:
        print ""+url
        SEARCHS(url)

elif mode==5:
        print ""+url
        GENRE(url)

elif mode==6:
        print ""+url
        XMLTRACK(url,iconimage)

elif mode==7:
        print ""+url
        TRACK(url,iconimage)

elif mode==8:
        print ""+url
        BILL(url)

elif mode==9:
        print ""+url
        BROWSE(url)

elif mode==10:
        print ""+url
        ARTISTAZ(url)

elif mode==11:
        print ""+url
        BESTSELLER(url)

elif mode==12:
        print ""+url
        HOTARTIST(url)

elif mode==13:
        print ""+url
        SUGGEST(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

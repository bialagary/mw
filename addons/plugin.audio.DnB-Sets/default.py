import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

#DnB-Sets - By Mucky Duck (10/05/2015)

addon_id = 'plugin.audio.DnB-Sets'
plugin = xbmcaddon.Addon(id=addon_id)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
baseurl = 'http://www.dnb-sets.de/'
baseurl1 = 'http://www.dnb-sets.de'
net = Net()

def CATEGORIES():
        addDir('[B][COLOR yellow]ALL[/COLOR][/B]',baseurl,1,icon,fanart,'')
        addDir('[B][COLOR yellow]Last Commented[/COLOR][/B]',baseurl+'?list=lastcommented',1,icon,fanart,'')
        addDir('[B][COLOR yellow]Live Search[/COLOR][/B]',baseurl,4,icon,fanart,'')
        addDir('[B][COLOR yellow]Most Commented(7 Days)[/COLOR][/B]',baseurl+'?list=mostcommented',1,icon,fanart,'')
        addDir('[B][COLOR yellow]Top 99 Searches[/COLOR][/B]',baseurl+'most-wanted.php',4,icon,fanart,'')
        addDir('[B][COLOR yellow]Top Rated(7 Days)[/COLOR][/B]',baseurl+'?list=toprated',1,icon,fanart,'')
        addDir('[B][COLOR yellow]Search[/COLOR][/B]',baseurl,3,icon,fanart,'')
        


def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<div id="ueberschrift"><b>(.+?)</b>.(.+?)<b>(.+?)</b>(.+?)<b>(.+?)</b>(.+?)</div>').findall(link)
        match=re.compile('<a href=".+?" style="color:#000000">(.+?)</a>.+?<td class="l_2">.+?<td class="r_2" nowrap="nowrap"><a href="(.+?)".+?</a>').findall(link)
        match2=re.compile('<a href="(.+?)">Next page .+?</a>').findall(link)
        for n1,n2,n3,n4,n5,n6 in match1:
                addDir('[B][COLOR green]%s %s%s %s %s %s[/COLOR][/B]' %(n1,n2,n3,n4,n5,n6),'',None,icon,fanart,'')
        for name,url in match:
                url = url.replace(' ','%20')
                name = name.replace('<font color=fff788><u>','')
                name = name.replace('</u></font>','')
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')
        for url in match2:
                addDir('[B][COLOR green]Next Page>>[/COLOR][/B]' ,baseurl+url,1,icon,fanart,'')

def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Search DnB-Sets')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                print encode
                url = baseurl+'?suche='+encode
                print url
                match=re.compile('<a href=".+?" style="color:#000000">(.+?)</a>.+?<td class="l_2">.+?<td class="r_2" nowrap="nowrap"><a href="(.+?)".+?</a>').findall(net.http_GET(url).content) 
                for name,url in match:
                        name = name.replace('<font color=fff788><u>','')
                        name = name.replace('</u></font>','')
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')


def TOPS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<tr class="mod_d">\r\n    <td  class="m_mod_l"  nowrap><a href="(.+?)">(.+?)</a></td>\r\n    <td  class="m_mod_r" >(.+?)</td>\r\n  </tr>').findall(link)
        match=re.compile('<td style="width:20px; text-align:center;">(.+?)</td><td  class="detail">.+?</td><td  class="adresse"><a href="(.+?)">(.+?)</a></td>.+?<td  class="detail">(.+?)</td></tr>').findall(link)               
        for pos,url,name,hit in match:
                url = url.replace(' ','%20')
                addDir('[B][COLOR yellow]%s: %s (matches:%s)[/COLOR][/B]' %(pos,name,hit),baseurl1+url,1,icon,fanart,'')
        for url,name,hit in match1:
                url = url.replace(' ','%20')
                addDir('[B][COLOR yellow]%s (matches:%s)[/COLOR][/B]' %(name,hit),baseurl1+url,1,icon,fanart,'')


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
        INDEX(url)

elif mode==2:
        print ""+url
        PLAY(name,url)

elif mode==3:
        print ""+url
        SEARCH(url)

elif mode==4:
        print ""+url
        TOPS(url)

elif mode==5:
        print ""+url
        TOPS(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

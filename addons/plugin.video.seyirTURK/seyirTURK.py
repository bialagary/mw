import sys
import urllib,urllib2
import re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import json, base64
import urlresolver
import hashlib
import os.path
from xml.dom import minidom

xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
settings = xbmcaddon.Addon(id='plugin.video.seyirTURK')
userdata = xbmc.translatePath('special://userdata')
def Basla():
        
        privacy = settings.getSetting( "adult" )
        if privacy == "false":
                mrl = root() + 'main/vip.php?filter=var'
        if privacy == "true":
                mrl = root() + 'main/vip.php?dummy=dummy'
        
        resp = root() + "check/check.php?mail=" + settings.getSetting( "mail" ) + "&parola=" + settings.getSetting( "sifre" )
        membership = get_url(resp)
        if ("okmember" in membership and settings.getSetting( "favori" ) == "true" ):
                erl = "&tip=favori&url=" + root() + "data/"+ hashlib.md5(settings.getSetting( "mail" )).hexdigest()+".xml"
        elif settings.getSetting( "favori" ) != "true" :
                erl =""
        else:
                erl="";
                showMessage("Favorilerim ozelligini kullanabilmek icin lutfen http://seyirturk.com a uye olunuz.")
        listele(mrl+erl)        
        if ("okmember" in membership and settings.getSetting( 'favori' ) == "false" ):
                addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ 'Favorilerim' +'[/B][/COLOR]'+'[COLOR blue]* [/COLOR]',mrl + "&tip=favori&url="+root()+"data/"+ hashlib.md5(settings.getSetting( "mail" )).hexdigest()+".xml",2,"resim")
        elif ("okmember" in membership and  settings.getSetting( 'favori' ) == "true"):
                if settings.getSetting( 'Adult')!='true':
                        portal_url = root() + 'main/vip.php?dummy=dummy'
                else :
                        portal_url = root() + 'main/vip.php?filter=evet'
                addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ 'Portallar' +'[/B][/COLOR]'+'[COLOR blue]* [/COLOR]',mrl,2,"resim")



                
def listele(url):
        
        searchstring=""
        if "&keyword" in url:
                keyboard = xbmc.Keyboard( '', "Film Arama", False )
                keyboard.doModal()
                if ( keyboard.isConfirmed() ):
                        searchstring = keyboard.getText()
                url = url+searchstring
        if url == "seyirturk.xml":
                seyirturk_file = os.path.join(userdata, 'seyirturk.xml')                
                if os.path.isfile(seyirturk_file) :
                        g = open(seyirturk_file).read()
                else:
                        showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR red][B]yerel listeniz yok![/B][/COLOR]")
        else :
                request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 seyirTURK_KODI (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
                f = urllib2.urlopen(request)
                g = get_url(url)
        print url
        print g
        if "Baslik" in g:
                js = json.load(f)
                for rs in js:

                        baslik=rs['Baslik'].encode('utf-8')
                        resim=rs['Resim'].encode('utf-8')
                        playlist=rs['Playlist'].encode('utf-8')
                        stream=rs['Stream'].encode('utf-8')
                        aciklama=rs['Aciklama'].encode('utf-8')
                        koruma=rs['Koruma']
                        if playlist <> '': 
                                url= playlist
                                if koruma == "False":
                                        
                                        addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ baslik +'[/B][/COLOR]',url+searchstring,2,resim)
                                        #addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ baslik +'[/B][/COLOR]',url,2,resim)
                                else:
                                        addDir('[COLOR red][B][COLOR blue]+18 > [/COLOR]'+ baslik +'[/B][/COLOR]',url,2,resim)

                        else:
                                url=stream
                                addDir('[COLOR white][B][COLOR red]> [/COLOR]'+baslik+'[/B][/COLOR]',url,3,resim)
                if "Portallar" in g:
                        addDir('[COLOR orange][B][COLOR blue]* [/COLOR] Yerel Oynatma Listem[/B][/COLOR]',settings.getSetting( "yerelxml" ) ,2,root()+'resimler/xml.png')
                                        
        elif "title" in g:
                xmldoc = minidom.parseString(g)
                js = xmldoc.getElementsByTagName('channel')
                
                for rs in js:
                        baslik = rs.getElementsByTagName("title")[0].firstChild.data.encode('utf-8')
                        resim=rs.getElementsByTagName("logo_30x30")[0].firstChild.data.encode('utf-8')
                        playlist_url = rs.getElementsByTagName("playlist_url")
                        stream_url = rs.getElementsByTagName("stream_url")                        
                        if len(playlist_url) > 0:
                                playlist=playlist_url[0].firstChild.data.encode('utf-8')
                                url = playlist
                                stream =None
                        elif len(stream_url)>0:
                                stream=stream_url[0].firstChild.data.encode('utf-8')
                                url = stream
                                playlist =None
                        else:
                                playlist = None
                                stream =None
                        aciklama=rs.getElementsByTagName("description")[0].firstChild.data.encode('utf-8')
                        aciklama = re.sub(r'<.*?>', '', aciklama)
                        if playlist <> None: 
                                addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ baslik +'[/B][/COLOR]',url,2,resim)
                        else:
                                addDir('[COLOR white][B][COLOR red]> [/COLOR]'+baslik+'[/B][/COLOR]',url,3,resim)
                                


        else:
                showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR blue][B]Link Bulunamadi[/B][/COLOR]")

def oynat(url,baslik):       
        playList.clear()
        url = str(url).encode('utf-8', 'ignore')
        if "vk.com" in url:
                url= VKoynat(url)
        elif "mail.ru" in url:
                url = Mailru(url)
        elif "youtube" in url:
                url= YoutubeOynat(url)
        elif "dailymotion" in url:
                url= dailyoynat(url)
        elif "epornik" in url:
                url= epornik(url)
        elif "veterok" in url:
                url= veterok(url)
        elif "vid.ag" in url:
                url= vidagoynat(url)
        elif "imdb" in url:
                url= imdb(url)
        elif "player.vimeo.com" in url:
                url= vimeo(url)
        elif "embed.myvideo.az" in url:
                url= myvideo(url)
        elif "watchcinema.ru" in url:
                url= watchcinema(url)
        elif "stagevu" in url:
                url= stagevu(url)
        elif "rutube" in url:
                url= rutube(url)
        elif "cloudy" in url:
                url= filekey1(url)
        elif "videoraj" in url:
                url= filekey1(url)
        elif "novamov" in url:
                url= filekey(url)
        elif "divxstage" in url:
                url= filekey(url)
        elif "embed.movshare" in url:
                url= kzd(url)
        elif "embed.nowvideo" in url:
                url= kzd(url)
        elif "plus.google.com" in url:
                url= google(url)
        elif "docs.google.com" in url:
                url= google(url)
        elif 'rtmp:'  in url:
                url= url
        elif 'rtsp:'  in url:
                url= url                                
        elif  'mms:' in url:
                url= url
        elif '.m3u8' in url:
                url= url
        elif url.endswith('.mp4'):
                url= url                    
        else:
                url1=urlresolver.resolve(url)
                if url1:
                        url = url1

        if url:
                if ("vk.com" in url or "youtube.com" in url or "rutube" in url):
                        oynat(url, baslik)
                else:
                        addLink(baslik,url,'')
                        listitem = xbmcgui.ListItem(baslik, iconImage="DefaultFolder.png", thumbnailImage='')
                        listitem.setInfo('video', {'name': baslik } )
                        playList.add(url,listitem=listitem)
                        xbmcPlayer.play(playList)
        else:
                showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR blue][B]Link Bulunamadi[/B][/COLOR]")


def google(url):

        if 'plus.google.com' in url:
                if "oid" in url:
                        oid = re.findall('oid=([0-9]+)',url)[0]
                        pid = re.findall('pid=([0-9]+)',url)[0]
                else:
                        ids = url.split("/")
                        oid = ids[4]
                        pid = ids[7]
                url = "https://picasaweb.google.com/data/feed/tiny/user/"+oid+"/photoid/"+pid+"?alt=jsonm";
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        response = urllib2.urlopen(request)
        html = response.read().decode('unicode-escape')
        
        if 'picasaweb.google.com' in url:
                links_part = re.findall('"https://redirector(.*?)"', html)
                pre_link = 'https://redirector'


        if 'docs.google.com' in url:
                links_parts = re.findall('"fmt_stream_map","(.*?)"', html)[0]
                links_part = re.findall('\\|(.*?),', links_parts)
                pre_link =''
        videolist = []
        qualitylist = []
        for link_part in links_part:                       
                if link_part.encode('utf_8').find("itag=18") > -1:
                        videolist.append(pre_link + link_part.encode('utf_8'))
                        qualitylist.append("360p")
                if link_part.encode('utf_8').find("itag=22") > -1:
                        videolist.append(pre_link + link_part.encode('utf_8'))
                        qualitylist.append("720p")
                if link_part.encode('utf_8').find("itag=37") > -1:
                        videolist.append(pre_link + link_part.encode('utf_8'))
                        qualitylist.append("1080p")
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',qualitylist)
        return videolist[ret]

def kzd(url):
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        secondpage = urllib2.urlopen(request).read()
        link = re.findall('flashvars\\.file="(.*?)";', secondpage)
        key = re.findall('var fkzd="(.*?)";', secondpage)
        if 'embed.movshare' in url:
                video = 'http://www.movshare.net/api/player.api.php?file=' + link[0] + '&key=' + key[0]
        else:
                video = 'http://www.nowvideo.sx/api/player.api.php?file=' + link[0] + '&key=' + key[0]
        request2 = urllib2.Request(video, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        thirdpage = urllib2.urlopen(request2).read()
        return re.findall('url=(.*?flv)', thirdpage)[0]

def filekey(url):
        
        url = url.replace("http://embed.divxstage.eu/embed.php?v=","http://www.cloudtime.to/video/")
        url = url.replace("http://www.divxstage.eu/video/","http://www.cloudtime.to/video/")
        url = url.replace("http://www.divxstage.to/video/","http://www.cloudtime.to/video/")
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        page = urllib2.urlopen(request).read()
        link = re.findall('flashvars.file="(.*?)";', page)
        key = re.findall('flashvars.filekey="(.*?)";', page)
        if 'novamov' in url:
                video = 'http://www.novamov.com/api/player.api.php?file=' + link[0] + '&key=' + key[0]
        else :
                video = 'http://www.cloudtime.to/api/player.api.php?file=' + link[0] + '&key=' + key[0]
        request2 = urllib2.Request(video, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        page2 = urllib2.urlopen(request2).read()
        return urllib.unquote(re.findall('url=(.*?)&', page2)[0])

def filekey1(url):
        
        url = url.replace ("http://www.videoraj.ch/v/","http://www.videoraj.ch/embed.php?id=")
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        page = urllib2.urlopen(request).read()
        link = re.findall('file:"(.*?)",', page)
        key = re.findall('key: "(.*?)",', page)
        domain = re.findall('domain: "(.*?)",', page)
        if 'videoraj' in url:
                video = "http://www.videoraj.ch/api/player.api.php?file="+ link[0] + "&key="+key[0]
        else:
                video = 'http://www.cloudy.ec/api/player.api.php?user=undefined&codes=1&file=' + link[0] + '&pass=undefined&key=' + key[0]
        request2 = urllib2.Request(video, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        page2 = urllib2.urlopen(request2).read()
        return urllib.unquote(re.findall('url=(.*?)&', page2)[0])


def rutube(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})                    
    page = urllib2.urlopen(request).read()
    page = page.replace ("&quot;","")
    return re.findall('m3u8:(.*?)}', page)[0].replace("&amp;", "&")
               
def stagevu(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    page = urllib2.urlopen(request).read()
    return re.findall('"src" value="(.*?)"', page)[0]
    
def watchcinema(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    page = urllib2.urlopen(request).read()
    page = page.strip(' \t\n\r')
    regex = re.findall('<iframe src="(.*?)"', page)
    return "http://"+regex[0].replace("https:","").replace("http://","").replace("&amp;", "&").replace("vkontakte.ru", "vk.com").replace("watchcinema.ru", "vk.com")

def vimeo(url):
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
        page = urllib2.urlopen(request).read()
        qualitylist = re.findall('(hd|sd|mobile)":\\{"profile".*?"url":".*?["|&]', page)
        videolist = re.findall('":\\{"profile".*?"url":"(.*?)"', page)
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',qualitylist)
        return videolist[ret]
def myvideo(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    response = urllib2.urlopen(request).read()
    a= re.findall("'file': '(.*?)'",response)
    request = urllib2.Request(a[0], None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    response = urllib2.urlopen(request)
    video = response.geturl()
    response.close()
    return video
    
def imdb(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    page = urllib2.urlopen(request).read()
    return re.findall('"url":"(.*?)"', page)[0]    

def veterok(url):
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    page = urllib2.urlopen(request).read()
    return re.findall('<script>files.*?="(.*?)"', page)[0]

                
def epornik(url):
        request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})                                                      
        page = urllib2.urlopen(request).read()
        return re.findall('file: "(.*?)"', page)[0]

def Mailru(url):
       url =  url.replace(".html","")
       var_arr = url.split("/")
       url = "http://m.my.mail.ru/mail/" +var_arr[6] + "/video/" + var_arr[7] + "/" + var_arr[8] + ".html"
       request = urllib2.Request(url, None)
       page = urllib2.urlopen(request).read()
       return re.findall('data-src="(.*?)"' ,page)[0].replace("&amp;","&")


def VKoynat(url):
        url = url.replace('https', 'http')
        page = get_url(url)
        vids = re.findall('"url.*?":"(.*?)"', page)
        quals = re.findall('"url(.*?)":"', page)
        videolist = [ reg.replace('\\','').replace('"','') for reg in vids]
        qualitylist = [ qual + 'p' for qual in quals ]
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',qualitylist)
        return videolist[ret]

def vidagoynat(url):
        page = get_url(url)
        vids = re.findall(',{file:"(.*?mp4)"', page)
        quals = re.findall('",label:"(.*?)"', page)
        videolist = [ reg.replace('\\','').replace('"','') for reg in vids]
        qualitylist = [ qual + '' for qual in quals ]
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',qualitylist)
        return videolist[ret]

def YoutubeOynat(url):

       yt_id = url.replace("http://www.youtube.com/embed/","").replace("http://www.youtube.com/watch?v=","")
       url='plugin://plugin.video.youtube/?action=play_video&videoid=' + yt_id

       return url
   
def dailyoynat(url):
        qualitylist =[]
        videolist=[]
        url = url.replace('dailymotion.com/video/', 'dailymotion.com/embed/video/')
        page = get_url(url)
        array = re.findall('stream_h264_(?:hd1080_|ld_|hq_|hd_|)url":"(.*?H264-(.*?)\\\\/.*?)"', page)
        if array:
                for v, q in array:
                        url = v.replace('\\', '')
                        videolist.append(url)
                        qualitylist.append(q+"p")
        array1 = re.findall('"(\\d+)":\\[{"type":"video\\\\\\/mp4","url":"([^"]+)"}]', page)
        if array1:
                for v, q in array1:
                        url = q.replace('\\', '')
                        videolist.append(url)
                        qualitylist.append(v+"p")
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',qualitylist)
        return videolist[ret]
def root():
        req = urllib2.Request(base64.b64decode("aHR0cDovL2hpdGl0LnRrL21haW4vZ2V0cm9vdC5waHA="), None, {'User-agent': 'Mozilla/5.0 seyirTURK_E2','Connection': 'Close'})
        return base64.b64decode(urllib2.urlopen(req).read())
def get_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 seyirTURK_KODI (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
def showMessage(heading='seyirTURK', message = '', times = 2000, pics = ''):
                try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
                except Exception, e:
                        xbmc.log( '[%s]: showMessage: exec failed [%s]' % ('', e), 1 )
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
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

if mode==None or url==None or len(url)<1:
       
        Basla()
       
elif mode==2:
       
        listele(url)
        
elif mode==3:
       
        oynat(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

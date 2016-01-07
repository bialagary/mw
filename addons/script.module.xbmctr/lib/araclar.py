# -*- coding: utf-8 -*-
import urllib,urllib2
import sys,re,HTMLParser,cookielib
import os,os.path,time,stat
from xml.dom.minidom import Document
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulStoneSoup

# Eklenti bildirimleri --------------------------------------------------------
addon_id = 'script.module.xbmctr'
__ayarlar__ = xbmcaddon.Addon(id=addon_id)
path = __ayarlar__.getAddonInfo('path')
IMAGES_PATH = xbmc.translatePath(os.path.join(path, 'resoures','image'))
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1)"
##XMLYOLU = xbmc.translatePath(os.path.join(home,'resources','temp'))
downloadFolder = __ayarlar__.getSetting('download-folder')
insidans=1
#----------------------------------------------------------------------------

def name_fix(x):        
        x=x.replace('-',' ')
        return x[0].capitalize() + x[1:]

def get_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/230008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xFD',"i").replace('&#39;&#39;',"\"").replace('&#39;',"\'").replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        link=link.replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")
        response.close()
        return link

def addFolder(fileName,name, mode ,url, thumbnail):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(FILENAME)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(url)
    if thumbnail != "":
        thumbnail = os.path.join(IMAGES_PATH, thumbnail+".png")
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    
def addLink(name, url, thumbnail=""):
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    liz.setInfo(type="Video", infoLabels={"Title":name})
    liz.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
    
def addDir(fileName,name, mode, url="", thumbnail=""):
    start()
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(fileName)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus(mode)+"&url="+urllib.quote_plus(url)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def loadImports(yol):
    files = os.listdir(yol)
    global imps
    imps = []

    for i in range(len(files)):
        py_name = files[i].split('.')
        if len(py_name) > 1:
            if py_name[1] == 'py' and py_name[0] != '__init__':
               py_name = py_name[0]
               imps.append(py_name)
    file = open(yol+'/__init__.py','w')
    toWrite = '__all__ = '+str(imps)
    file.write(toWrite)
    file.close()
    return imps

def listChannels(IMAGES_PATH):
    for fileName in imps:
        thumbnail= os.path.join(IMAGES_PATH, fileName+".png")
        addDir(fileName, '[COLOR lightgreen][B]'+fileName+'[/B][/COLOR]' ,"main()", "",thumbnail)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xml_yap(fileName,bolum,MAINRESULT):
    doc = Document()
    liste = doc.createElement("liste")
    doc.appendChild(liste)


    for videoTitle,url,thumbnail,description in MAINRESULT:
            print ('xml yap DOKUM',videoTitle)
            kanal = doc.createElement("channel")
            liste.appendChild(kanal)
            

            ad = doc.createElement("title")
            kanal.appendChild(ad)
            veri_ad = doc.createTextNode(videoTitle.encode( "utf-8" ))
            ad.appendChild(veri_ad)

            adres = doc.createElement("stream_url")
            kanal.appendChild(adres)
            veri_adres = doc.createTextNode(url)
            adres.appendChild(veri_adres)

            resim = doc.createElement("logo_30x30")
            kanal.appendChild(resim)
            veri_resim = doc.createTextNode(thumbnail)
            resim.appendChild(veri_resim)

            info = doc.createElement("description")
            kanal.appendChild(info)
            veri_info = doc.createTextNode(description)
            info.appendChild(veri_info)
    os.chmod(XMLYOLU, stat.S_IRWXO)
    os.chmod(XMLYOLU, stat.S_IRWXG)
    os.chmod(XMLYOLU, stat.S_IRWXU)
    filepath = xbmc.translatePath(os.path.join(XMLYOLU,str(fileName)+'_'+bolum+'.xml'))
    try:
            os.chmod(filepath, stat.S_IRWXO)
            os.chmod(filepath, stat.S_IRWXG)
            os.chmod(filepath, stat.S_IRWXU)
    except:
            pass

    f = open(filepath, "w")
    try:
        f.write(doc.toprettyxml(indent="",encoding="utf-8"))
    finally:
        f.close()
    return filepath

def open_xml(filepath):
        finalResult=[]
        handler=open(filepath,"r")
        handler = handler.read()
        soup=BeautifulStoneSoup(handler)
        print 'ENCODING : ',soup.originalEncoding
        
        channels =soup.findAll('channel')
        for channel in channels:
                title=channel.title
                videoTitle=title.text
                logo=channel.logo_30x30
                thumbnail=contents = "".join([str(item) for item in logo.contents])
                thumbnail=re.sub(r'\s', '', thumbnail)            #bosluklari kesiyoruz
                desc=channel.description
                desc=re.compile(']]>(.*?)</description>').findall(str(desc))
                purl=channel.playlist_url
                surl=channel.stream_url
                if desc:
                        print desc
                else:
                        desc='Bilgi Yok'
                if purl:
                        url=purl.text
                else:
                        if surl:
                                url=surl.text
                        else:
                                print 'xml den url alinmadi.'
                                pass #Hata kodu yazilacak
                finalResult.append((videoTitle, url, thumbnail))
##        print 'finalResult:'+str(finalResult)                
        return finalResult

def check_time(xml):
        try:
                status=''
                t = os.path.getmtime(xml)
                today = time.time()
                diff=today-t
                print diff
                if diff <= 1083000:
                        status="GUNCEL"
                else:
                        status="ESKI"
                return status
        except:
                return ["/unable to control " + xml]

def check_xml_status(kanal,marker,url):
        print ('check xml giris:',kanal,marker)
        finalResult=''
        xml=XMLYOLU +'\\'+kanal+'_'+marker+'.xml'
        Sonuc=check_empty_xml(xml)
        if Sonuc == 'YOK':
                print 'XML YOK'
                exec "import "+kanal+" as channel"
                exec "channel.SCAN(marker,url)"
                print 'XML OLUSTURULDU'
        else:
                print 'XML BULUNDU'
                pass

        status=check_time(xml)
        print "XML DOSYA DURUMU : " +str(status)
        if status == "ESKI":
                print "xml dosya = ESKI / YENIDEN TARANIYOR."
                exec "import "+kanal+" as channel"
                exec "channel.SCAN(marker,url)"
                print 'XML YENILENDI'
                finalResult=open_xml(xml)
        
        elif status == "GUNCEL":
                print "VAROLAN XML OKUNUYOR:"+kanal+'_'+marker+'.xml'
                finalResult=open_xml(xml)
        else:
                print 'RECENT SONUC :xml degerlendirilemedi'
        
        return finalResult

def check_empty_xml(xml):
        print xml
        if os.path.isfile(xml):
                Sonuc='VAR'
        else:
                Sonuc='YOK'
       
        return Sonuc
def liste_olustur(Url,match):
##        print 'Paging started'
        urlList=''
        for pageUrl in match:
                #web page list function
                urlList=urlList+pageUrl #add page to list
                urlList=urlList+':;'    #add seperator
                total=Url+':;'+urlList  #add first url
                match = total.split(':;') #split links
                del match [-1]            #delete first seperator
                #print match
        info='Film '+str(len(match)-1)+' part.'
        match = filter(bool,match)
        return match
def indir_kontrol():
        downloadFolder=__ayarlar__.getSetting("Download")
        if downloadFolder is '':
                d = xbmcgui.Dialog()
                d.ok('Download Error','You have not set the download folder.\n Please set the addon settings and try again.','','')
                __ayarlar__.openSettings(sys.argv[ 0 ])
        else:
                if not os.path.exists(downloadFolder):
                        print 'Download Folder Doesnt exist. Trying to create it.'
                        os.makedirs(downloadFolder,0777)
def indir(videoTitle,urlList):
        indir_kontrol()
        xbmcPlayer = xbmc.Player()
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        
        indir_fonksiyon(videoTitle,urlList)
        xbmc.executebuiltin('Notification("Media Center","Indirildi Oynatiliyor.")')
        playList.clear()
        xbmcPlayer.play(playList)

        

def indir_fonksiyon(videoTitle,urlList):
        nameCount=0
        subfolder=os.path.join(downloadFolder,str(videoTitle))
        try:
                os.makedirs(subfolder)
        except:
                pass
        
        for url in urlList if not isinstance(urlList, basestring) else [urlList]:
                print "inecek url",url
                name='Part'
                nameCount=nameCount+1
                name= name+' '+str(nameCount)
                filename = (videoTitle+' '+name+'.mp4')
                filepath = xbmc.translatePath(os.path.join(subfolder,filename))
                urllib.urlretrieve(url,filepath)
                iscanceled = True
                playList.add(url)
                xbmc.executebuiltin('Notification("Media Center","part Complete")')
        




        
def do_wait(source, account, wait_time):
     # do the necessary wait, with  a nice notice and pre-set waiting time. I have found the below waiting times to never fail.
     
     if int(wait_time) == 0:
         wait_time = 1
         
     if account == 'vk':    
          return handle_wait(int(wait_time),source,'Loading video with your *Platinum* account.')

     else:
          return handle_wait(int(wait_time),source,'Loading video.')


def handle_wait(time_to_wait,title,text):

    print str(time_to_wait)+' saniye '+'bekleyiniz.'

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(' '+title)

    secs=0
    percent=0
    increment = float(13000) / time_to_wait
    increment = int(round(increment))

    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = increment*secs
        secs_left = str((time_to_wait - secs))
        remaining_display = ' Videonuzun yüklenmesine '+secs_left+' saniye kaldi....'
        pDialog.update(percent,' '+ text, remaining_display)
        xbmc.sleep(130000)
        if (pDialog.iscanceled()):
             cancelled = True
             break
    if cancelled == True:     
         print 'wait cancelled'
         return False
    else:
         print 'done waiting'
         return True
def inside():
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

       
        login= __ayarlar__.getSetting("Username")
        password= __ayarlar__.getSetting("password")
        req = urllib2.Request("http://forum.xbmctr.com/member.php"); #Login Page
        req.add_header('User-Agent',"Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/2013000101 Firefox/10.0.1")

        vals = {'action' : 'do_login','url' : 'http://forum.xbmctr.com/','username' : login,'password' : password,'Submit' : 'login'}
        data = urllib.urlencode(vals)
        try:
                opener.open(req,data).read() #Source of Login Page
        except:
                d = xbmcgui.Dialog()
                d.ok(__ayarlar__.getLocalizedString(30001),__ayarlar__.getLocalizedString(30002),__ayarlar__.getLocalizedString(30003))
                d.ok(__ayarlar__.getLocalizedString(30004),__ayarlar__.getLocalizedString(30005),__ayarlar__.getLocalizedString(30006))
                EXIT()
                return False
        resp = opener.open('http://forum.xbmctr.com/manager/')
        data=resp.read()
        if "  V.I.P" in data:
                __ayarlar__.setSetting('log',"True")
                return True
        else:
                __ayarlar__.setSetting('log',"False")
                EXIT()
def start():
        d = xbmcgui.Dialog()
        login=__ayarlar__.getSetting("log")
        if not login or login=="False":
                global insidans
                if insidans==1:
                        cevap=d.yesno(__ayarlar__.getLocalizedString(30007),__ayarlar__.getLocalizedString(30008),__ayarlar__.getLocalizedString(30009),__ayarlar__.getLocalizedString(30010))
                        if cevap:
                                __ayarlar__.openSettings()
                                check=inside()
                        else:
                                __ayarlar__.setSetting('log',"False")
                                EXIT()
                        insidans+=1
                else:
                        pass
        if __ayarlar__.getSetting("log")=="True":
                pass
        else:
                __ayarlar__.setSetting('log',"False")
                EXIT()
def hata():
        d = xbmcgui.Dialog()
        d.ok(__ayarlar__.getLocalizedString(30011),__ayarlar__.getLocalizedString(30012),__ayarlar__.getLocalizedString(30013))
def EXIT():
        xbmc.executebuiltin("XBMC.Container.Refresh(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")                
def playlist_yap(playList,name,url):
        listitem = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="")
        listitem.setInfo('video', {'name': name } )
        playList.add(url,listitem=listitem)
        return playList

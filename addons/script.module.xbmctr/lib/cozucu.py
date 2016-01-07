# -*- coding: utf-8 -*-
# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Dr Ayhan Colak
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# for more info please visit http://xbmctr.com

'''
Author: drascom
Date: 13/04/2012
'''

import urllib, urllib2, re, sys, cookielib
import xbmc, xbmcaddon, xbmcgui,xbmcplugin
import araclar
import mechanize
import urlresolver
import time

    
__settings__ = xbmcaddon.Addon(id='script.module.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "cozucu"




'''Constants'''
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
vk=[]
value=[]




'''
listing,pagination function
for multipage web site
'''

def unique(l):
    s = set(); n = 0
    for x in l:
        if x not in s: s.add(x); l[n] = x; n += 1
    del l[n:]

    
def fullfilm_gizli_player(url):
##        print 'GIZLI PLaYER url ',url
        link=araclar.get_url(url)
        link=link.replace('%3A',":").replace('%3F',"?").replace('%3D',"=")
        match=re.compile('v=(.*?)&').findall(link)
##        print 'GIZLI PLaYER',match
        url=match[0]
        return url

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


def prepare_face_links(videoTitle,match):
        i=0
        for pageLink in match:
                link=araclar.get_url(pageLink)
                match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                    
                for videoLink in match:
                        i+=1
                        araclar.addVideoLink(videoTitle+' Part '+str(i),videoLink,'')
                        playList.add(videoLink)
def Youtube_Player(url):
        code=re.match(r"http://www.youtube.com/embed/(.*?)$", url).group(1)

        print '[code]'+str(code)
        url='plugin://plugin.video.youtube/?action=play_video&videoid=' + str(code)
        return url

def Divxshare_Player(url):
        value=''
        xbmc.executebuiltin('Notification("Media Center",DIVXSTAGE Deneniyor.)')
        link=araclar.get_url(url)
        match=re.compile('domain="(.*?)";\n\t\t\tflashvars.file="(.*?)";\n\t\t\tflashvars\.filekey="(.*?)"').findall(link)
        if not match:
            xbmc.executebuiltin('Notification("Sitede HATA ",ilk Linki yok.)')
        for domain,dosya,key in match:
            transfer =domain+"/api/player.api.php?file="+dosya+"&codes=undefined&user=undefined&key="+key+"&pass=undefined"
            link=araclar.get_url(transfer)
            match=re.compile('url=(.*?)&').findall(link)
            if not match:
                xbmc.executebuiltin('Notification("Serverda HATA ",Ikinci Linki yok.)')
            for url in match:
                if url.endswith('flv'):
                        value=url
                else:
                    pass
        print value
        return value
def stagevu_player(code):
    link=araclar.get_url(url)
    sv1 = re.compile('src="(.+?)" border="0">').findall(link)
    link=araclar.get_url(sv1[0])
    sv3 = re.compile('src="(.+?)" border="0"').findall(link)
    link=araclar.get_url(sv3[0])
    StageVu=re.compile('<param name="src" value="(.+?)" />').findall(link)
    print "stagevu",StageVu
    return StageVu[0]
def wfih_player(code):
    return code
                        
def Yesload_Player(code):
    value=''
    link=araclar.get_url(code)
    yesloadurlbul1=re.compile('<a target="_blank" href="http://yesload.net/(.*?)">').findall(link)
    for x in yesloadurlbul1:
        code='http://yesload.net/player_api/info?token='+x
    link=araclar.get_url(code)
    yesloadurlbul2=re.compile('premium.token=(.*?)"').findall(link)
    for x in yesloadurlbul2:
        code='http://yesload.net/player_api/info?token='+x
    link=araclar.get_url(code)
    yesloadplayer=re.compile('url=(.*?).flv&').findall(link)
    for url in yesloadplayer:
        value=url
    return value

def Streamcloud_Player(url):
    value=''
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    cookie = response.info().getheader('Set-Cookie')  
    response.close()
    match=re.compile('<input type="hidden" name="op" value="(.*?)">\n\t\t\t\t\t\t<input type="hidden" name="usr_login" value="(.*?)">\n\t\t\t\t\t\t<input type="hidden" name="id" value="(.*?)">\n\t\t\t\t\t\t<input type="hidden" name="fname" value="(.*?)">\n\t\t\t\t\t\t<input type="hidden" name="referer" value="(.*?)">\n\t\t\t\t\t\t<input type="hidden" name="hash" value="(.*?)">\n\t\t\t\t\t\t<input type="submit" name="imhuman" .*? value="(.*?)">').findall(link)
    print "3.match:",match
    for op,usr_login,id,fname,referer,hash,imhuman in match:
        import time
        time.sleep(10)

        gidecekveriler=urllib.urlencode({'op' : op, 'usr_login' : usr_login, 'id' : id, 'fname' : fname, 'referer' : referer, 'hash' : hash, 'imhuman' : imhuman.replace(" ","+")})
        req=urllib2.Request(url)
        req.add_header('Referer', url)
        req.add_data(gidecekveriler)
        req.add_header('Cookie',cookie)
        post = urllib2.urlopen(req)
        gelen_veri=post.read()
        gelen_veri=re.compile('file: "(.+?)"').findall(gelen_veri)
        print "4.match",gelen_veri
        for final in gelen_veri:
                value=final
                print "final url",value
                
        return value


    
def stream2k_Player(code):
    value=''
    link=araclar.get_url(code)
    match=re.compile('<iframe.*?src="(.*?)"><\/iframe><BR><\/div>\W+<div id="underplayer">').findall(link)
    link=araclar.get_url(match[0])
    match1=re.compile("file: .(.*)'").findall(link)
    for url in match1:
        value=url
    return value

def Dailymotion(code):
        value=[]
        count=[]
        url="http://www.dailymotion.com/embed/video/"+code
        link=araclar.get_url(url)
        link = urllib.unquote(link).decode('utf8').replace('\\/', '/')
        dm_high = re.compile('"stream_h264_url":"(.+?)"').findall(link)
        dm_low = re.compile('"stream_h264_ld_url":"(.+?)"').findall(link)
        if dm_high:
                count.append('Dailymotion 360kb/s HD')
        if dm_low:
                count.append('Dailymotion 180kb/s SD ')
        else:
                pass
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008),count)
        if ret == 0:
                
                value.append(('Dailymotion 384 p',dm_high[0]))
        if ret == 1:

                value.append(('Dailymotion 240 p',dm_low[0]))
        
        return value
def Flashx_Player(url):
     link=araclar.get_url(url)
     print url
     playerbul=re.compile('href="http://flashx.tv/video\/(.*?)\/.*?">').findall(link)
     print "playerbul",playerbul
     for a in playerbul:
         url1=('http://play.flashx.tv/nuevo/player/cst.php?hash='+a)
         url=url1
         
         link=araclar.get_url(url)
         match=re.compile('<file>(.*?).flv</file>').findall(link)
         print "playerbul2",match
         for a in match:
             url=a+'.flv'
             print "playerbul3",url
             return url

            
def Putlocker_Player(url):
    xbmc.executebuiltin('Notification("Media Center",PUTLOCKER Deneniyor.)')
    link=araclar.get_url(url)
    match=re.compile('<input type="hidden" value="(.*?)" name="(.*?)">').findall(link)
    print "ilk match",match
    for a,b in match:
        bilgiler=urllib.urlencode({b : a,'confirm': 'Close Ad and Watch as Free User'})
        adres=urllib.urlopen(url,bilgiler)
        #Gelen bilgiyi okuyalim
        adres=adres.read()
        #Gelen bilginin icinde URL adresini alalim
        adres=re.compile('playlist: \'(.*?)\'').findall(adres)
        for son_url in adres:
            url='http://www.putlocker.com'+son_url
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            link=link.replace('amp;',"").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('#038;',"")
            response.close()
            match=re.compile('content url="(.*?)"').findall(link)
            print "putlocker son",match
            del match[0]#burasi onemli kalmali ok
            for url in match:
                return url
    
    
            
def vk_Player(vk_list):
        value=[]
        count=[]
        fixed=''
        gecis=0
        resolutions = ["240", "360", "480", "720", "1080"]
        
        for url in vk_list if not isinstance(vk_list, basestring) else [vk_list]:
                try:   
                    link=araclar.get_url(url)
                    host=re.compile("host=(.*?)&").findall(link)
                    uid=re.compile("uid=(.*?)&").findall(link)
                    vtag=re.compile("vtag=(.*?)&").findall(link)
                    hd = re.compile("hd_def=(.*?)&").findall(link)
                    if not hd or hd[0]=="-1":
                        hd = re.compile("max_hd = '(.*?)';").findall(link)
                    flv = re.compile("no_flv=(.*?)&").findall(link)
                    #http://cs514110.userapi.com/u175995076/video/ac8f196d08.xxx.mp4
                    start_url=host[0]+'u'+uid[0]+'/videos/' + vtag[0]
                    print "vk start url",start_url
                    print "hd:",hd
                    x=(int(hd[0])+1)
                    if hd >0 or flv == 1:
                            for i in range (x):
                                    i=resolutions[i]+' p'
                                    count.append(i) 
                            if gecis==0:
                                    dialog = xbmcgui.Dialog()
                                    ret = dialog.select(__language__(30014),count)
                                    for i in range (x):
                                            if ret == i:
                                                    url=start_url+'.'+str(resolutions[i])+'.mp4'
                                                    fixed=str(resolutions[i])
                                                    gecis+=1
                                                    
                                            else:
                                                    'VK SECIM YOK'
                            else:
                                    url=start_url+'.'+fixed+'.mp4'
                                    print ('SECIM :'+fixed)
                                    gecis+=1
                            value.append(url)
                    else:
                            print 'HD FLV YANLIS'
                except:
                        print 'LINK TARAMA FAILED'
                        pass
        return value




def xml_scanner(videoTitle,url):
        value=[]
        xmlScan=araclar.get_url(url)
        dizihd=re.compile('git=(.*?)"').findall(xmlScan)
        face_1=re.compile('http://dizihd.com/dizihdd.php(.+?)"').findall(xmlScan)#xml ici face link
        youtube_1=re.compile('v=(.*?)"').findall(xmlScan)#xml içi youtube link
        dizimag=re.compile('url="(.*?)"').findall(xmlScan) #xml ici dizimag                               
        music=re.compile('<file>(.*?)</file>').findall(xmlScan)
        if len(youtube_1)> 0  :
                for i, url in enumerate(youtube_1):
                        Url='plugin://plugin.video.youtube/?action=play_video&videoid='+str(youtube_1[0])
                        value.append(Url)
        
        if len(face_1)> 0  :
                for i, url in enumerate(face_1):
                        Url='http://dizihd.com/dizihdd.php'+str(url)
                        value.append(Url)
                        
        if len(dizimag)> 0:
                for i, url in enumerate(dizimag):
                        value.append(url)
                       
        if len(music)> 0  :
                for i, url in enumerate(music):
                        value.append(url)
                       
        
        print 'XML DONUS DEGERI',value
        return value                      
                                
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)


def videobul(urlList):
    value=[]
    try:
        print "Bizim Sistem Deneniyor"
        value=denetle(urlList)
        print "Bizim sistem sonuc:",value
        if not value:
            print "urlresolver Sistem Deneniyor"
            for url in urlList if not isinstance(urlList, basestring) else [urlList]:
                url=urlresolver.resolve(url)
                if url:
                    value.append(("Server",url))
                else:
                    value="False"
            print "********* resolver sonuc ***********",value
    except:
        araclar.hata()
    if not value=="False":
            return value
    else:
        return False


def denetle(urlList):
        vk=[]
        value=[]
        for url in urlList if not isinstance(urlList, basestring) else [urlList]:
                print "cozulecek url",url
                if 'vk.com' in url:
                    print 'VK BULUNDU'
                    vk.append(url)

                if "divxstage" in url:
                    value.append(("DivxStage",Divxshare_Player(url)))

                if "novamov" in url:
                    value.append(("NovaMov",Divxshare_Player(url)))

                if "flashx" in url:
                    value.append(("Flashx",Flashx_Player(url)))
                
                if 'youtube' in url:
                    print 'YOUTUBE BULUNDU'
                    value.append(("YT Server",Youtube_Player(url)))
    
                if 'http://www.videoslasher.com' in url:
                    value.append(("VS Server",Videoslasher_Player(url)))

                if "movshare" in url:
                    value.append(("MovShare",Divxshare_Player(url)))

                if "vimple" in url:
                    xbmc.executebuiltin('Notification("Beklenen Hata",vimple henuz cozulmedi.)')

                if "stream2k.com" in url:
                    value.append(("Stream2k",stream2k_Player(url)))
                
                if "stagevu" in url:
                    value.append(("StageVu",stagevu_Player(url)))

                if "streamcloud" in url:
                    value.append(("Streamcloud",Streamcloud_Player(url)))

                if "nowvideo" in url:
                    value.append(("NowVideo",Divxshare_Player(url)))

                if "yesload" in url:
                    value.append(("Yesload",Yesload_Player(url)))

                if "putlocker" in url:
                    value.append(("Putlocker",Putlocker_Player(url)))
                    
        if vk:
                print 'VK ILK OKUMA:'
                vk_sonuc=vk_Player(vk)
                for url in vk_sonuc:
                        value.append(("VK Server",url))
                        
        print "bizimki ne dondu"
        if  value:
            return value
        else:
            return False
       
       


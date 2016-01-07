import xbmc, xbmcgui, xbmcaddon, xbmcplugin, re
import urllib, urllib2
import re, string
import threading
import os
import base64
#from t0mm0.common.addon import Addon
#from t0mm0.common.net import Net
import urlparse
import xbmcplugin
#addon = Addon('plugin.video.mxrte', sys.argv)
#net = Net()

mode =None
play=False

#play = addon.queries.get('play', None)
paramstring=sys.argv[2]
#url = addon.queries.get('playurl', None)
print paramstring
if paramstring:
    paramstring="".join(paramstring[1:])
    params=urlparse.parse_qs(paramstring)
    print params
    url = params['url'][0]#
    name = params['name'][0]
    mode =  params['mode'][0]
    maxbitrate=0
    try:
        maxbitrate =  int(params['maxbitrate'][0])
    except: pass
    play=True

def playF4mLink(url,name,proxy=None,use_proxy_for_chunks=False):
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    #progress = xbmcgui.DialogProgress()
    #progress.create('Starting local proxy')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    player.playF4mLink(url, name, proxy, use_proxy_for_chunks,maxbitrate)
    
    return   
    
def GUIEditExportName(name):

    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading('Enter Url')
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name  = kb.getText()
              #name_correct = name_confirmed.count(' ')
              #if (name_correct):
              #   GUIInfo(2,__language__(33224)) 
              #else: 
              #     name = name_confirmed
              #     exit = False
          #else:
          #    GUIInfo(2,__language__(33225)) 
          exit = False
    return(name)
    
if mode ==None:
    
    videos=[['','High Speed Stream up to 720p','http://remoteman.tv/pic/bbc/inet.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte1/rte1_720p.f4m','RTE One HD','http://img4.wikia.nocookie.net/__cb20130331190918/logopedia/images/thumb/3/3c/RT%C3%89_One.svg/300px-RT%C3%89_One.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte2/rte2_720p.f4m','RTE Two HD','http://upload.wikimedia.org/wikipedia/en/thumb/3/36/RT%C3%89_Two.svg/250px-RT%C3%89_Two.svg.png',0],
['','Medium Speed Stream up to 576p','http://remoteman.tv/pic/bbc/inet.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte1/rte1_540p.f4m','RTE One','http://img4.wikia.nocookie.net/__cb20130331190918/logopedia/images/thumb/3/3c/RT%C3%89_One.svg/300px-RT%C3%89_One.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte2/rte2_540p.f4m','RTE Two','http://upload.wikimedia.org/wikipedia/en/thumb/3/36/RT%C3%89_Two.svg/250px-RT%C3%89_Two.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/newsnow/newsnow_540p.f4m','RTE News','http://j.static-locatetv.com/images/content/3/277173_rt_news_and_farming_weather.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rsw5/rsw5_576p.f4m','RTE Jnr','http://www.rte.ie/rtejr/wp-content/themes/rtejr-2013/img/rtejr-logo-large.jpg',0],
['','Slower Speed Stream up to 360p','http://remoteman.tv/pic/bbc/inet.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte1/rte1_360p.f4m','RTE One','http://img4.wikia.nocookie.net/__cb20130331190918/logopedia/images/thumb/3/3c/RT%C3%89_One.svg/300px-RT%C3%89_One.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte2/rte2_360p.f4m','RTE Two','http://upload.wikimedia.org/wikipedia/en/thumb/3/36/RT%C3%89_Two.svg/250px-RT%C3%89_Two.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/newsnow/newsnow_360p.f4m','RTE News','http://j.static-locatetv.com/images/content/3/277173_rt_news_and_farming_weather.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rsw5/rsw5_360p.f4m','RTE Jnr','http://www.rte.ie/rtejr/wp-content/themes/rtejr-2013/img/rtejr-logo-large.jpg',0],
['','Slowest Speed Stream up to 288p','http://remoteman.tv/pic/bbc/inet.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte1/rte1_288p.f4m','RTE One','http://img4.wikia.nocookie.net/__cb20130331190918/logopedia/images/thumb/3/3c/RT%C3%89_One.svg/300px-RT%C3%89_One.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/rte2/rte2_288p.f4m','RTE Two','http://upload.wikimedia.org/wikipedia/en/thumb/3/36/RT%C3%89_Two.svg/250px-RT%C3%89_Two.svg.png',0],
['http://livehds.rasset.ie/hds-live/_definst_/newsnow/newsnow_288p.f4m','RTE News','http://j.static-locatetv.com/images/content/3/277173_rt_news_and_farming_weather.jpg',0],
['http://livehds.rasset.ie/hds-live/_definst_/rsw5/rsw5_288p.f4m','RTE Jnr','http://www.rte.ie/rtejr/wp-content/themes/rtejr-2013/img/rtejr-logo-large.jpg',0]]
     

    #['http://dummy','Custom']]
    #print videos

    if 1==2: #disable it as these links are not working, not sure why
        req = urllib2.Request('http://www.gzcbn.tv/app/?app=ios&controller=cmsapi&action=pindao')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        ##	print link

        s='title\":\"(.*?)\",\"stream\":\"(.*?)\"'
        #    
        match=re.compile(s).findall(link)
        i=0
        for i in range(len(match)):
            match[i]= (match[i][1].replace('\\/','/'),match[i][0])


        videos+=match #disabled for time being as these are not working
    #print videos
    for (file_link,name,imgurl,maxbitrate) in videos:
        liz=xbmcgui.ListItem(name,iconImage=imgurl, thumbnailImage=imgurl)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        #liz.setProperty("IsPlayable","true")
        u = sys.argv[0] + "?" + urllib.urlencode({'url': file_link,'mode':'play','name':name,'maxbitrate':maxbitrate}) 
        print u
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, )


   
    
elif mode == "play":
    print 'PLAying ',mode,url
    if not name=='Custom':
        playF4mLink(url,name)
    else:
        newUrl=GUIEditExportName('')
        if not newUrl=='':
            playF4mLink(newUrl,name)




if not play:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
 
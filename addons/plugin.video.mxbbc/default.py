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
#addon = Addon('plugin.video.mxbbc', sys.argv)
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
    
    videos=[['','   *** Low Speed at least 2mbis needed ***   ','http://thaisatellite.tv/pic/bbc/inet.jpg',0],

    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_480.f4m|X-Forwarded-For=212.58.241.131','bbc 1','http://www.parker1.co.uk/myth/icons/tv/bbc1.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc2/bbc2_480.f4m|X-Forwarded-For=212.58.241.131','bbc 2','http://www.parker1.co.uk/myth/icons/tv/bbc2.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_480.f4m|X-Forwarded-For=212.58.241.131','bbc 3','http://thaisatellite.tv/pic/bbc/bbc_three.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_480.f4m|X-Forwarded-For=212.58.241.131','bbc 4','http://thaisatellite.tv/pic/bbc/bbc_four_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_480.f4m|X-Forwarded-For=212.58.241.131','cbbc','http://thaisatellite.tv/pic/bbc/bbc_cbbc.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_480.f4m|X-Forwarded-For=212.58.241.131','cbeebeies ','http://thaisatellite.tv/pic/bbc/bbc_cbeebies_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/parl/parl_480.f4m|X-Forwarded-For=212.58.241.131','bbc parliment','http://thaisatellite.tv/pic/bbc/bbc_parliament.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/newsch/newsch_480.f4m|X-Forwarded-For=212.58.241.131','bbc news','http://thaisatellite.tv/pic/bbc/bbc_news.png',0],

    ['','   *** Medium Speed at least 8mbis needed ***   ','http://thaisatellite.tv/pic/bbc/inet.jpg',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_800.f4m|X-Forwarded-For=212.58.241.131','bbc 1','http://www.parker1.co.uk/myth/icons/tv/bbc1.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc2/bbc2_800.f4m|X-Forwarded-For=212.58.241.131','bbc 2','http://www.parker1.co.uk/myth/icons/tv/bbc2.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_800.f4m|X-Forwarded-For=212.58.241.131','bbc 3','http://thaisatellite.tv/pic/bbc/bbc_three.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_800.f4m|X-Forwarded-For=212.58.241.131','bbc 4','http://thaisatellite.tv/pic/bbc/bbc_four_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_800.f4m|X-Forwarded-For=212.58.241.131','cbbc','http://thaisatellite.tv/pic/bbc/bbc_cbbc.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_800.f4m|X-Forwarded-For=212.58.241.131','cbeebeies ','http://thaisatellite.tv/pic/bbc/bbc_cbeebies_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/parl/parl_800.f4m|X-Forwarded-For=212.58.241.131','bbc parliment','http://thaisatellite.tv/pic/bbc/bbc_parliament.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/newsch/newsch_800.f4m|X-Forwarded-For=212.58.241.131','bbc news','http://thaisatellite.tv/pic/bbc/bbc_news.png',0],
    ['','   *** High Speed at least 16mbis needed ***   ','http://thaisatellite.tv/pic/bbc/inet.jpg',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_1500.f4m|X-Forwarded-For=212.58.241.131','bbc 1','http://www.parker1.co.uk/myth/icons/tv/bbc1.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc2/bbc2_1500.f4m|X-Forwarded-For=212.58.241.131','bbc 2','http://www.parker1.co.uk/myth/icons/tv/bbc2.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_1500.f4m|X-Forwarded-For=212.58.241.131','bbc 3','http://thaisatellite.tv/pic/bbc/bbc_three.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_1500.f4m|X-Forwarded-For=212.58.241.131','bbc 4','http://thaisatellite.tv/pic/bbc/bbc_four_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_1500.f4m|X-Forwarded-For=212.58.241.131','cbbc','http://thaisatellite.tv/pic/bbc/bbc_cbbc.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_1500.f4m|X-Forwarded-For=212.58.241.131','cbeebeies ','http://thaisatellite.tv/pic/bbc/bbc_cbeebies_uk.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/parl/parl_1500.f4m|X-Forwarded-For=212.58.241.131','bbc parliment','http://thaisatellite.tv/pic/bbc/bbc_parliament.png',0],
    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/newsch/newsch_1500.f4m|X-Forwarded-For=212.58.241.131','bbc news','http://thaisatellite.tv/pic/bbc/bbc_news.png',0]]
     

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
    
 
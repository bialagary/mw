import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import re
import fileinput

 
addon_handle = int(sys.argv[1])
 
xbmcplugin.setContent(addon_handle, 'movies')

response = urllib2.urlopen('http://goo.gl/u3Nwfx')
for lines in response:
    print lines

url = '111.223.37.199/live/thaitv3_33/chunklist_w773808452.m3u8'
li = xbmcgui.ListItem('Channel 3', iconImage='http://offsite.tv/mx/ch/3.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = 'edge10.psitv.tv:1935/liveedge/308661309596_600/playlist.m3u8'
li = xbmcgui.ListItem('Channel 5', iconImage='http://offsite.tv/mx/ch/5.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge9.psitv.tv:1935/liveedge/308091128717_600/playlist.m3u8'
li = xbmcgui.ListItem('Channel 7', iconImage='http://offsite.tv/mx/ch/7.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge6.psitv.tv:1935/liveedge/307803302519_600/playlist.m3u8'
li = xbmcgui.ListItem('Channel 9', iconImage='http://offsite.tv/mx/ch/9.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge10.psitv.tv:1935/liveedge/308806374084_600/playlist.m3u8'
li = xbmcgui.ListItem('NBT', iconImage='http://offsite.tv/mx/ch/nbt.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge10.psitv.tv:1935/liveedge/308950239342_600/playlist.m3u8'
li = xbmcgui.ListItem('Thai PBS', iconImage='http://offsite.tv/mx/ch/pbs.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = '202.170.127.178:1935/dcinode001/nation.sdp/playlist.m3u8'
li = xbmcgui.ListItem('Nation Channel', iconImage='http://offsite.tv/mx/ch/nation.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge2.psitv.tv:1935/liveedge/308078198120_600/playlist.m3u8'
li = xbmcgui.ListItem('Bangkok Channel', iconImage='http://offsite.tv/mx/ch/bkkc.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = 'solution01.stream.3bb.co.th:1935/MonoTV720/720p_th/playlist.m3u8'
li = xbmcgui.ListItem('Mono 29', iconImage='http://offsite.tv/mx/ch/mono29.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'live-th.dmc.tv/live/th_silver.stream/playlist.m3u8'
li = xbmcgui.ListItem('DMC', iconImage='http://offsite.tv/mx/ch/dmc.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = '202.170.127.178:1935/dcinode001_money/moneybb.sdp/playlist.m3u8'
li = xbmcgui.ListItem('Money Channel', iconImage='http://offsite.tv/mx/ch/money.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'livestream.voicetv.co.th:1935/live-edge/smil:voicetv_all.smil/playlist.m3u8?DVR'
li = xbmcgui.ListItem('Voice TV', iconImage='http://offsite.tv/mx/ch/voice.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = '103.14.10.12:1935/liveedge/307626143200_300/playlist.m3u8'
li = xbmcgui.ListItem('Asia Update', iconImage='http://offsite.tv/mx/ch/asiaup.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge5.psitv.tv:1935/liveedge/292277350688_600/playlist.m3u8'
li = xbmcgui.ListItem('Blue Sky channel', iconImage='http://offsite.tv/mx/ch/bluesjy.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = 'edge6.psitv.tv:1935/liveedge/292277210375_600/playlist.m3u8'
li = xbmcgui.ListItem('Grand Prix Channel', iconImage='http://offsite.tv/mx/ch/grandprix.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = '210.1.60.208:1935/live/bang.sdp/playlist.m3u8'
li = xbmcgui.ListItem('Bang Channel', iconImage='http://offsite.tv/mx/ch/bang.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge5.psitv.tv:1935/liveedge/292277227873_600/playlist.m3u8'
li = xbmcgui.ListItem('Workpoint TV', iconImage='http://offsite.tv/mx/ch/workpoint.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge2.psitv.tv:1935/liveedge/292277206574_600/playlist.m3u8'
li = xbmcgui.ListItem('You Channel', iconImage='http://offsite.tv/mx/ch/you.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'http://edge5.psitv.tv:1935/liveedge/292277209720_600/playlist.m3u8'
li = xbmcgui.ListItem('Channel 8', iconImage='http://offsite.tv/mx/ch/tvpool.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = 'solution01.stream.3bb.co.th:1935/edgezaanetwork/zaa_all.smil/playlist.m3u8'
li = xbmcgui.ListItem('Zaa HD', iconImage='http://offsite.tv/mx/ch/zaa.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)

url = '202.44.53.13:1935/dtac/gmmmusic_240p.stream/playlist.m3u8'
li = xbmcgui.ListItem('GMM Music HD', iconImage='http://offsite.tv/mx/ch/gmm.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


url = 'edge5.psitv.tv:1935/liveedge/292277442241_600/playlist.m3u8'
li = xbmcgui.ListItem('Cartoon Club', iconImage='http://offsite.tv/mx/ch/cartoonclub.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=lines+url, listitem=li)


response.close()

xbmcplugin.endOfDirectory(addon_handle)

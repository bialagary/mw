import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import re
import fileinput

 
addon_handle = int(sys.argv[1])
 
xbmcplugin.setContent(addon_handle, 'movies')

 
url = 'http://goo.gl/0CofPI'
li = xbmcgui.ListItem('Pac 12 Network', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/yy2Y0F'
li = xbmcgui.ListItem('Arizona', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/gHG3ty'
li = xbmcgui.ListItem('Bay Area', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/m4Xaul'
li = xbmcgui.ListItem('Los Angeles', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/6QnKIG'
li = xbmcgui.ListItem('Mountain', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/FLfuDu'
li = xbmcgui.ListItem('Oregon', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

 
url = 'http://goo.gl/ZOww80'
li = xbmcgui.ListItem('Washington', iconImage='http://goo.gl/lmA5Uv')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


xbmcplugin.endOfDirectory(addon_handle)

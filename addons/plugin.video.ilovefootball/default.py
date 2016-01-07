import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser

addon_id = 'plugin.video.ilovefootball'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'ilovefootball.db')
BASE_URL = 'http://real-madrid-cf-hd.blogspot.co.uk/'
net = Net()
addon = Addon('plugin.video.ilovefootball', sys.argv)

###### PATHS ###########
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"

##### Queries ##########
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
text = addon.queries.get('text', None)

################################################################################# Titles #################################################################################

def GetTitles(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('''<a dir='ltr' href='(.+?)'>(.+?)</a>\s*?<span dir='ltr'>.+?</span>\s*?</li>''').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles1', 'url': url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('''<h3 class='post-title entry-title' itemprop='name'>\s*?<a href='(.+?)'>(.+?)</a>\s*?</h3''').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles2', 'url': url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles2(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="https://archive.org/download/(.+?)" target="_blank">(.+?)</a>').findall(content)
        for url, name in match:
                name = name.replace('<span', '')
                name = name.replace('style=', '')
                name = name.replace('font-family: Arial,Helvetica,sans-serif;', '')
                name = name.replace('font-size: x-large', '')
                name = name.replace('"', '')
                name = name.replace('<', '')
                name = name.replace('>', '')
                name = name.replace('<b>', '')
                name = name.replace('</b>', '')
                name = name.replace('/', '')
                name = name.replace('b', '')
                name = name.replace(';', '')
                name = name.replace('span', '')
                addon.add_directory({'mode': 'PlayVideo', 'url': 'https://archive.org/download/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip().replace('<span style="font-family: Arial,Helvetica,sans-serif;"><span style="font-size: x-large;">', '')}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry no links [/B][/COLOR],[COLOR blue][B]Please try a different movie/tv show[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##.replace('', '')## \s*? ##
############################################################################# Play Video #####################################################################################

def PlayVideo(url, listitem, text):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]PLAY : [/B][/COLOR]' + text, iconImage='http://www.iconsdb.com/icons/preview/white/football-xxl.png', thumbnailImage= 'http://www.iconsdb.com/icons/preview/white/football-xxl.png')
        li.setProperty('fanart_image', 'http://blogs.bmj.com/bjsm/files/2014/08/football-on-the-stadium-4565.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

def GetDomain(url):
        tmp = re.compile('//(.+?)/').findall(url)
        domain = 'Unknown'
        if len(tmp) > 0 :
            domain = tmp[0].replace('www.', '')
        return domain

def GetMediaInfo(html):
        listitem = xbmcgui.ListItem()
        match = re.search('og:title" content="(.+?) \((.+?)\)', html)
        if match:
                print match.group(1) + ' : '  + match.group(2)
                listitem.setInfo('video', {'Title': match.group(1), 'Year': int(match.group(2)) } )
        return listitem

###################################################################### menus ####################################################################################################

def MainMenu():    #homescreen
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[COLOR blue][B]Latest Uploaded[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[COLOR blue][B]Football Library[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


#################################################################################################################################################################################

if mode == 'main': 
	MainMenu()
elif mode == 'GetTitles': 
	GetTitles(url, text)
elif mode == 'GetTitles1': 
	GetTitles1(url, text)
elif mode == 'GetTitles2': 
	GetTitles2(url, text)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem, text)	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
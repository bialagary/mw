import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser

addon_id = 'plugin.video.tvonlineER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'tvonlineER.db')
BASE_URL = 'http://tvonline.tw/'
net = Net()
addon = Addon('plugin.video.tvonlineER', sys.argv)

###### PATHS ###########
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"

##### Queries ##########
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
text = addon.queries.get('text', None)
img = addon.queries.get('img', None)
#\s*?#
################################################################################# Titles #################################################################################

def GetTitles3(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="http://tvonline.tw/tv-listings(.+?)">(.+?)<').findall(content)
        for url, name in match:
                name = name.replace('TV Listings', '[COLOR blue][B]TV Listings A to Z[/COLOR][/B]')
                addon.add_directory({'mode': 'GetTitles', 'url': 'http://tvonline.tw/tv-listings' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles4(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="http://tvonline.tw/genres(.+?)">(.+?)<').findall(content)
        for url, name in match:
                name = name.replace('Genres', '[COLOR blue][B]By Genres[/COLOR][/B]')
                addon.add_directory({'mode': 'GetTitles', 'url': 'http://tvonline.tw/genres' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles5(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<ul><li><a href="http://tvonline.tw/(.+?)" title="Wtach.+?online">(.+?)</a></li></ul>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://tvonline.tw/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def GetTitles(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<ul><li><a href="http://tvonline.tw/(.+?)" title="Wtach.+?online">(.+?)</a></li></ul>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles1', 'url': 'http://tvonline.tw/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<h3><a href='http://tvonline.tw/(.+?)' title='Wtach.+?online'>(.+?)</a></h3>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles2', 'url': 'http://tvonline.tw/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles2(url, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<li><a href='http://tvonline.tw/(.+?)' title='Wtach.+?online'><strong>(.+?)</strong>(.+?)</a></li>").findall(content)
        for url, name, name1 in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://tvonline.tw/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip() + ' ' + name1}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("'(http://.+?)'").findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PlayVideo(url, listitem):
    try:
        print 'in PlayVideo %s' % text
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

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


def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green][B]Search tv shows[/B][/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return

        
def Search(query):
        url = 'http://tvonline.tw/search.php?key=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<ul><li><a href="(.+?)" target="_blank">(.+?)</a></li></ul>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetTitles1', 'url':'http://tvonline.tw/' +  url}, {'title':  title}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

###################################################################### menus ####################################################################################################

def MainMenu(url, text):    #homescreenserie
        addon.add_directory({'mode': 'GetTitles5', 'section': 'ALL', 'url': BASE_URL + '/new-episodes/'}, {'title':  '[COLOR blue][B]New Episodes[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/latest-added/'}, {'title':  '[COLOR blue][B]Latest Added[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/most-popular/'}, {'title':  '[COLOR blue][B]Most Popular[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL + '/tv-listings/a/'}, {'title':  '[COLOR blue][B]A to Z[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/genres/action/'}, {'title':  '[COLOR blue][B]Genres[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[B][COLOR green]Search[/B][/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#################################################################################################################################################################################

if mode == 'main': 
	MainMenu(url, text)
elif mode == 'GetTitles': 
	GetTitles(url, text)
elif mode == 'GetTitles1': 
	GetTitles1(url, text)
elif mode == 'GetTitles2': 
	GetTitles2(url, text)
elif mode == 'GetTitles3': 
	GetTitles3(url, text)
elif mode == 'GetTitles4': 
	GetTitles4(url, text)
elif mode == 'GetTitles5': 
	GetTitles5(url, text)
elif mode == 'GetLinks':
	GetLinks(section, url, text)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
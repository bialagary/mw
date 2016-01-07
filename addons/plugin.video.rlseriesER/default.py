import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.rlseriesER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'rlseriesER.db')
net = Net()
addon = Addon('plugin.video.rlseriesER', sys.argv)
BASE_URL = 'http://rlseries.com/'
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)

def GetTitles(section, url, startPage= '1', numOfPages= '1'): 
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('<div class="img_wrp">\s*?<a href="(.+?)" title="(.+?)" class="anm_det_pop">\s*?<img width="140" height="200" src="(.+?)" class=".+?" alt=".+?" srcset=".+?" sizes=".+?" />\s*?</a>\s*?</div>\s*?</td>\s*?</tr>\s*?<tr>\s*?<td>\s*?<table border=".+?" cellpadding=".+?" cellspacing=".+?" width=".+?" bgcolor=".+?" style=".+?">\s*?<tbody>\s*?<tr>\s*?<td align="left" width=".+?">\s*?<font color="orange">.+?</font>.+?</td>\s*?<td align="right" width=".+?">\s*?<font color=".+?">.+?</font>.+?</td>\s*?</tr>\s*?</tbody>\s*?</table>\s*?</td>\s*?</tr>\s*?</tbody>\s*?</table>\s*?<div style=".+?">\s*?<a href=".+?" title=".+?" class=".+?"><b><font color=".+?">.+?</font></b></a><br/>\s*?<div class="vws"><a class=".+?" href=".+?" title="(.+?)">', re.DOTALL).findall(html)
                for movieUrl, name, img, name1 in match:
                        addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img }, {'title':  name.strip() + ' ' + name1}, img= img, fanart=FanartPath + 'fanart.jpg')     
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.jpg')      
        setView('tvshows', 'tvshows-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a class="lst" href="(.+?)" title="(.+?)">\s*?<b class="val"><font color=".+?" size=".+?" style=".+?">.+?</font>.+?</b>\s*?<b class="dte">(.+?)</b>').findall(content)
        match1 = re.compile('<div class="vdesc">\s*?<p>(.+?)</p>').findall(content)
        match2 = re.compile('<a href="http://www.imdb.com/title/.+?" target="_blank">(.+?)</a></strong>(.+?)</p>').findall(content)
        match3 = re.compile('<a href="(.+?)" class="vurl" target="_blank">.+?</a>').findall(content)
        for name in match1:
                addon.add_directory({'url': url, 'listitem': listitem}, {'title': '[COLOR blue][B]' + name.strip() + '[/COLOR][/B]'}, img= img, fanart=FanartPath + 'fanart.jpg') 
        for name, name1 in match2:
                addon.add_directory({'url': url, 'listitem': listitem}, {'title': '[COLOR pink][B]' +  name.strip() + ' ' + name1 + '[/COLOR][/B]'}, img= img, fanart=FanartPath + 'fanart.jpg') 
        for url, name, date in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url, 'listitem': listitem, 'img': img}, {'title':  name.strip() + ' - ' + date}, img= img, fanart=FanartPath + 'fanart.jpg') 
        for url in match3:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" class="vurl" target="_blank">.+?</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^ Press back ^[/B] [/COLOR]'},'','')
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

def MainMenu():   
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B][COLOR blue]Latest :[/COLOR] Episodes & Seasons[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B][COLOR blue]Genre :[/COLOR] Full Seasons[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/sport/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Sport [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/western/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Western [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/music/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Music [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/action/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Action [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/horror/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Horror [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/thriller/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Thriller [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/mystery/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Mystery [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/crime/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Crime [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/fantasy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Fantasy [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/sci-fi/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Sci-fi [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/adventure/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Adventure [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/romance/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Romance [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/animation/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Animation [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/history/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]History [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/drama/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Drama [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/war/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]War [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/documentary/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Documentary [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/comedy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Comedy [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/family/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Family [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/reality-tv/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Reality Tv [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/game-show/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Game Show [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/talk-show/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Talk Show [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return

def Search(query):
        url = 'http://rlseries.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="img_wrp">\s*?<a href="(.+?)" title="(.+?)".+? src="(.+?)"', re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img }, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.jpg') 
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )

if mode == 'main': 
	MainMenu()
elif mode == 'GenreMenu':
        GenreMenu()
elif mode == 'GetTitles': 
	GetTitles(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(url, img)
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)	
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
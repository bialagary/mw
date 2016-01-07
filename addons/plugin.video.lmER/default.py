import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.lmER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'lmER.db')
net = Net()
addon = Addon('plugin.video.lmER', sys.argv)
BASE_URL = 'http://latestdude.com/'
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
                match = re.compile('<div class="item">\s*?<a href="(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl, 'img': img }, {'title':  name.strip()}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        match1 = re.compile('<meta itemprop="headline" content=".+?" />\s*?<meta itemprop="description" content="(.+?)" />').findall(content)
        match2 = re.compile('(https://archive.org/.+?.mp4)"').findall(content)
        match3 = re.compile('<iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" allowfullscreen></iframe></div>').findall(content)
        match4 = re.compile('<span class="dato"><a href="http://www.imdb.com/.+?" target="_blank">(.+?)</a> <b>(.+?)</b> <b>(.+?)</b></span>').findall(content)
        listitem = GetMediaInfo(content)
        for name in match1:
                addon.add_directory({'img': img}, {'title':  '[COLOR darkturquoise][B]' + name.strip() + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for name, name1, name2 in match4:
                addon.add_directory({'img': img}, {'title':  '[COLOR pink][B]' + name.strip() + ' ' + name1 + '.. ' + name2 + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for url in match3:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' : [COLOR red][B]Trailer[/B][/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        for url in match2:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem , 'img': img, 'text': text }, {'title':  'direct link'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo1(text, img, url, listitem):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem('Play', iconImage=img, thumbnailImage=img)
        li.setProperty('fanart_image', 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

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
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/english/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest Movies[/B]'}, img=IconPath + 'lm.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/1080p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]1080p Movies[/B]'}, img=IconPath + 'lm.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/brrip/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]720p Movies[/B]'}, img=IconPath + 'lm.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B]Movies Genre[/B]'}, img=IconPath + 'mg.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/tv-show/',
                             #'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest Shows[/B]'}, img=IconPath + 'lt.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'se.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'url.png', fanart= 'http://www.htbackdrops.org/v2/albums/userpics/10097/orig_oefg_kino_im_kesselhaus.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/3d/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]3D [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/western/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Western [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/music/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Music [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/science-fiction/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Science Fiction [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/action/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Action [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/horror/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Horror [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/thriller/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Thriller [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/mystery/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Mystery [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/crime/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Crime [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/fantasy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Fantasy [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/sci-fi/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Sci-fi [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/adventure/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Adventure [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/romance/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Romance [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/animation/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Animation [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/history/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]History [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/drama/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Drama [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/war/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]War [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/documentary/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Documentary [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/comedy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Comedy [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/family/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Family [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/english/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]English [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/hindi-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Hindi [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/hindi-dubbed/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Hindi Dubbed [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/malayalam-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Malayalam movies [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/telugu/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Telugu [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/httplatestdude-comsunrated/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Unrated [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/uncategorized/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]Uncategorized [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
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
        url = 'http://latestdude.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="item">\s*?<a href="http://latestdude.com/(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" />\s*?<span class="player"></span>\s*?<span class="imdb"><b><b class="icon-star"></b></b>(.+?)</span></div>').findall(html)
        for url, img, title, imdb in match:
                addon.add_directory({'mode': 'GetLinks', 'url':'http://latestdude.com/' +  url}, {'title':  title + ' : ' + imdb}, img= img, fanart=FanartPath + 'fanart.jpg')
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
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)	
elif mode == 'PlayVideo1':
	PlayVideo1(text, img, url, listitem)
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
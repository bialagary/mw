import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.streamthisER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'streamthisER.db')
net = Net()
addon = Addon('plugin.video.streamthisER', sys.argv)
BASE_URL = 'http://streamthis.tv/'
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

#----------------------------------------------------------------------------movies-----------------------------------------------------------------------------------------#

def GetTitles4(section, url): 
        pageUrl = url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html                    
        match = re.compile('<div class="col xs12 s6 m3 l2 animated bounceInUp">\s*?<a href="(.+?)" title="Watch .+?">\s*?<div class="card">\s*?<img class="hide-on-med-and-down" alt=".+?" src=".+?src=(.+?)&amp.+?" width="100%">\s*?<img class="hide-on-large-only" alt=".+?" src=".+?" width="100%">\s*?<p class="smalltitle">\s*?(.+?)\s*?</p>\s*?<p class="tinytitle">\s*?(.+?)\s*?</p>', re.DOTALL).findall(html)
        match1 = re.compile('''<li class='current'><a href=".+?">.+?</a></li> <li><a href="(.+?)">.+?</a></li>''').findall(content) 
        for movieUrl, img, name, name1 in match:
                addon.add_directory({'mode': 'GetLinks1', 'section': section, 'url': movieUrl, 'img': img }, {'title':  name.strip() + '  ' + name1}, img= img, fanart=FanartPath + 'fanart1.jpg')     
        for url in match1:
                addon.add_directory({'mode': 'GetTitles4', 'url': url, 'listitem': listitem}, {'title': 'next page'}, img='http://www.megatoner.si/media/mw_promobox/icon/open-left.png', fanart=FanartPath + 'fanart1.jpg')      
        setView('tvshows', 'tvshows-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks1(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a class="collection-item black-text" href="(.+?)"').findall(content)
        match1 = re.compile('twitter:description" content="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for name in match1:
                addon.add_directory({'url': url, 'listitem': listitem, 'img': img }, {'title': '[COLOR powderblue][B]' + name.strip() + '[/COLOR][/B]'}, img=img, fanart=FanartPath + 'fanart1.jpg') 
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart=FanartPath + 'fanart1.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------tv-----------------------------------------------------------------------------------------#

def GetTitles(section, url): 
        pageUrl = url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html                    
        match = re.compile('<div class="col xs12 s6 m3 l2 animated bounceInUp">\s*?<a href="(.+?)" title="Watch .+?">\s*?<div class="card">\s*?<img class="hide-on-med-and-down" alt=".+?" src=".+?src=(.+?)&amp.+?" width="100%">\s*?<img class="hide-on-large-only" alt=".+?" src=".+?" width="100%">\s*?<p class="smalltitle">\s*?(.+?)\s*?</p>\s*?<p class="tinytitle">\s*?(.+?)\s*?</p>', re.DOTALL).findall(html)
        match1 = re.compile('''<li class='current'><a href=".+?">.+?</a></li> <li><a href="(.+?)">.+?</a></li>''').findall(content) 
        for movieUrl, img, name, name1 in match:
                addon.add_directory({'mode': 'GetTitles1', 'section': section, 'url': movieUrl, 'img': img }, {'title':  name.strip() + '  ' + name1}, img= img, fanart=FanartPath + 'fanart.jpg')     
        for url in match1:
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'listitem': listitem}, {'title': 'next page'}, img='http://www.megatoner.si/media/mw_promobox/icon/open-left.png', fanart=FanartPath + 'fanart.jpg')      
        setView('tvshows', 'tvshows-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<li><a href='http://streamthis.tv/show/(.+?)'>(.+?)</a></li>").findall(content) 
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles2', 'url': 'http://streamthis.tv/show/' + url, 'listitem': listitem, 'img': img }, {'title':  name.strip()}, img=img, fanart=FanartPath + 'fanart.jpg') 
        setView('tvshows', 'tvshows-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles2(url, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a class="collection-item black-text" href="(.+?)">(.+?)</a>').findall(content) 
        match1 = re.compile('twitter:description" content="(.+?)"').findall(content) 
        for name in match1:
                addon.add_directory({'url': url, 'listitem': listitem, 'img': img }, {'title': '[COLOR powderblue][B]' + name.strip() + '[/COLOR][/B]'}, img=img, fanart=FanartPath + 'fanart.jpg') 
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url, 'listitem': listitem, 'img': img }, {'title':  name.strip()}, img=img, fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a class="collection-item black-text" href="(.+?)"').findall(content)
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
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + 'movies'}, {'title':  '[B][COLOR blue]Latest :[/COLOR] Movies[/B]'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movies/imdb_rating'}, {'title':  '[B][COLOR blue]Top IMDB :[/COLOR] Movies[/B]'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GenreMenu1'}, {'title':  '[B][COLOR blue]Genre :[/COLOR] Movies[/B]'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-shows/date/'}, {'title':  '[B][COLOR blue]Latest :[/COLOR] Episodes & Seasons[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-shows/imdb_rating'}, {'title':  '[B][COLOR blue]Top IMDB :[/COLOR] Full Seasons[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B][COLOR blue]Genre :[/COLOR] Full Seasons[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/action'}, {'title':  '[COLOR lime]action [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/adventure'}, {'title':  '[COLOR lime]adventure [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/animation'}, {'title':  '[COLOR lime]animation [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/biography'}, {'title':  '[COLOR lime]biography [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/comedy'}, {'title':  '[COLOR lime]comedy [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/crime'}, {'title':  '[COLOR lime]crime [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/documentary'}, {'title':  '[COLOR lime]documentary [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/drama'}, {'title':  '[COLOR lime]drama [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/family'}, {'title':  '[COLOR lime]family [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/fantasy'}, {'title':  '[COLOR lime]fantasy [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/game-show'}, {'title':  '[COLOR lime]game show [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/history'}, {'title':  '[COLOR lime]history [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/horror'}, {'title':  '[COLOR lime]horror [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/music'}, {'title':  '[COLOR lime]music [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/musical'}, {'title':  '[COLOR lime]musical [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/mystery'}, {'title':  '[COLOR lime]mystery [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/news'}, {'title':  '[COLOR lime]news [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/reality-tv'}, {'title':  '[COLOR lime]reality tv [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/romance'}, {'title':  '[COLOR lime]romance [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/sci-fi'}, {'title':  '[COLOR lime]sci-fi [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/sitcom'}, {'title':  '[COLOR lime]sitcom [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/sport'}, {'title':  '[COLOR lime]sport [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/talk-show'}, {'title':  '[COLOR lime]talk show [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/thriller'}, {'title':  '[COLOR lime]thriller [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/war'}, {'title':  '[COLOR lime]war [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/tv-tags/western'}, {'title':  '[COLOR lime]western [/COLOR] >>'}, img= 'http://i132.photobucket.com/albums/q6/HecklerUK/Misc/MediaBrowser%20Issues/TVSeries.png', fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu1(): 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/action'}, {'title':  '[COLOR lime]action [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/adventure'}, {'title':  '[COLOR lime]adventure [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/animation'}, {'title':  '[COLOR lime]animation [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/biography'}, {'title':  '[COLOR lime]biography [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/comedy'}, {'title':  '[COLOR lime]comedy [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/crime'}, {'title':  '[COLOR lime]crime [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/documentary'}, {'title':  '[COLOR lime]documentary [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/drama'}, {'title':  '[COLOR lime]drama [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/family'}, {'title':  '[COLOR lime]family [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/fantasy'}, {'title':  '[COLOR lime]fantasy [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/film-noir'}, {'title':  '[COLOR lime]film noir [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/history'}, {'title':  '[COLOR lime]history [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/horror'}, {'title':  '[COLOR lime]horror [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/music'}, {'title':  '[COLOR lime]music [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/musical'}, {'title':  '[COLOR lime]musical [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/mystery'}, {'title':  '[COLOR lime]mystery [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')   
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/romance'}, {'title':  '[COLOR lime]romance [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/sci-fi'}, {'title':  '[COLOR lime]sci-fi [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/sport'}, {'title':  '[COLOR lime]sport [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')  
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/thriller'}, {'title':  '[COLOR lime]thriller [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/war'}, {'title':  '[COLOR lime]war [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/movie-tags/western"'}, {'title':  '[COLOR lime]western [/COLOR] >>'}, img=IconPath + 'movie.png', fanart=FanartPath + 'fanart1.jpg') 
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
        url = 'http://streamthis.tv/show/' + query 
        url = url.replace(' ', '-')
        print url
        html = net.http_GET(url).content
        match = re.compile("<li><a href='http://streamthis.tv/show/(.+?)'>(.+?)</a></li>", re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetTitles2', 'section': section, 'url': 'http://streamthis.tv/show/' + movieUrl, 'img': 'http://orig14.deviantart.net/7d96/f/2013/287/d/3/tv_series_icon_by_quaffleeye-d6qj64q.png' }, {'title':  name.strip()}, img= 'http://orig14.deviantart.net/7d96/f/2013/287/d/3/tv_series_icon_by_quaffleeye-d6qj64q.png', fanart=FanartPath + 'fanart.jpg') 
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
elif mode == 'GenreMenu1':
        GenreMenu1()
elif mode == 'GetTitles': 
	GetTitles(section, url)
elif mode == 'GetTitles1': 
	GetTitles1(url, img)
elif mode == 'GetTitles2': 
	GetTitles2(url, img)
elif mode == 'GetTitles4': 
	GetTitles4(section, url)
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetLinks1':
	GetLinks1(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)	
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
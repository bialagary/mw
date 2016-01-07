'''
    Fun and Movies (funandmovies.com) XBMC Plugin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.		
'''

import re
import os
import string
import sys
import urlresolver
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

try:
    import json
except:
    import simplejson as json

addon_id = 'plugin.video.funandmovies'
addon = Addon(addon_id, sys.argv)

net = Net()

BASEURL = 'http://www.funandmovies.com/'
SEARCHURL = 'http://www.google.com/uds/GblogSearch?start=[START]&q=[QUERY]+blogurl:http://www.funandmovies.com/&v=1.0'

def AddSysPath(path):
    if path not in sys.path:
        sys.path.append(path)

#PATHS
AddonPath = addon.get_path()
LibsPath = os.path.join(AddonPath, 'resources', 'libs')
AddSysPath(LibsPath)        

from universal import watchhistory

mode = addon.queries['mode']
url = addon.queries.get('url', '')
title = addon.queries.get('title', '')
img = addon.queries.get('img', '')
start = addon.queries.get('start', '')
section = addon.queries.get('section', '')
historytitle = addon.queries.get('historytitle', '')
historylink = addon.queries.get('historylink', '')
queued = addon.queries.get('queued', '')

'''
class Paths:
    rootDir = addon.get_path()

    if rootDir[-1] == ';':
        rootDir = rootDir[0:-1]

    resDir = os.path.join(rootDir, 'resources')
    imgDir = os.path.join(resDir, 'images')

    pluginFanart = os.path.join(rootDir, 'fanart.jpg')
    defaultVideoIcon = os.path.join(imgDir, 'video.png')
    defaultCategoryIcon = os.path.join(imgDir, 'folder.png')    
'''

def WatchedCallback():
    print 'Video completed successfully'

def escape(text):
        try:            
            rep = {" ": "%20"                  
                   }
            for s, r in rep.items():
                text = text.replace(s, r)

        except TypeError:
            pass

        return text
        
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",  
                   "&#8217;" : "'"
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text

def reformat_movie_name(text):
    text = re.sub("Online Watch Movies Free: ", "", text)
    text = re.sub(r"([0-9]{4}).+?$", "\g<1>", text)
    text = re.sub(r"(\([0-9]{4})", "\g<1>)", text)
    return text

def MainMenu():
    addon.add_directory({'mode' : 'Browse', 'section': 'movies'}, {'title':  'Movies'})
    addon.add_directory({'mode': 'Search'}, {'title':  'Search'})
    addon.add_directory({'mode': 'Resolver'}, {'title':  'Resolver Settings'})
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def Browse(section):
    
    if section == 'movies':
        addon.add_directory({'mode' : 'Browse', 'section': 'atoz'}, {'title':  'A-Z'})
        addon.add_directory({'mode' : 'Browse', 'section': 'featured'}, {'title':  'Featured'})
        addon.add_directory({'mode' : 'Browse', 'section': 'years'}, {'title':  'Years'})
        
    elif section == 'featured':
        site_data = net.http_GET(BASEURL).content
        
        for movies_match in re.finditer(r"(?s)HTML2.*?Bollywood Movies.*?<ul>(.+?)hindi-movies-list", site_data):

            movies = movies_match.group(1)
            movies = addon.unescape(movies)
            movies = unescape(movies)

            for movie in re.finditer(r"<li><a.*?href=\"(.+?)\">(.+?)<", movies):

                movie_url = movie.group(1)
                movie_name = movie.group(2)
                movie_name = addon.unescape(movie_name)
                movie_name = unescape(movie_name)
                
                try:
                    movie_url_data = net.http_GET(movie_url).content
                    movie_img = re.search(r"(?s)<div class='post-body entry-content'>.*?<img.*?src=\"(.+?)\".*?</div>", movie_url_data)
                    if movie_img:
                        movie_img = movie_img.group(1)                    
                        addon.add_directory({'mode': 'links', 'url' : movie_url, 'title' : movie_name, 'img' : movie_img }, {'title':  movie_name }, img= movie_img)
                except:
                    pass
    elif section == 'atoz' or section == 'years':
        site_data = net.http_GET(BASEURL).content
        
        items = ''
        if ( section == 'atoz' ):
            items = re.search(r"(?s)<h2>A-Z Movies(.+?)</div>", site_data).group(1)
        elif ( section  == 'years' ):
            items = re.search(r"(?s)<h2>All Movies Years(.+?)</div>", site_data).group(1)

        for item in re.finditer(r"(?s)<a.*?href='(.+?)'>(.+?)</a>", items):

            item_url = item.group(1)
            item_name = item.group(2)
            
            addon.add_directory({'mode': 'section', 'url' : item_url}, {'title':  item_name })
            
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def Search(query, start):
    search_url_format = SEARCHURL
    search_url_query = re.sub("\[QUERY\]", query, search_url_format)
    search_url = re.sub("\[START\]", start, search_url_query)

    search_result = net.http_GET(search_url).content
    result_json = json.loads(search_result)

    for search_item in result_json['responseData']['results']:

        movie_title = search_item['title']        

        movie_url = search_item['postUrl']

        movie_name = search_item['titleNoFormatting']
        if re.search(r"\)", movie_name):
            movie_name = movie_name[0:movie_name.index(')')+1]        
        movie_name = addon.unescape(movie_name)
        movie_name = unescape(movie_name)
        movie_name = reformat_movie_name(movie_name) 
        
        movie_url_data = net.http_GET(movie_url).content
        movie_img = re.search(r"(?s)<div class='post-body entry-content'>.*?<img.*?src=\"(.+?)\".*?</div>", movie_url_data).group(1)                    
        
        addon.add_directory({'mode': 'links', 'url' : movie_url, 'title' : movie_name, 'img' : movie_img }, {'title':  movie_name }, img= movie_img)

    result_count = int(result_json['responseData']['cursor']['estimatedResultCount'])

    new_start = int(start) + 4
    if (new_start < result_count):                
        addon.add_directory({'mode': 'Search', 'url' : query, 'start' : str(new_start) }, {'title':  'Next Page >>' })
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def GetSection(url):
    label_url_data = net.http_GET(url).content

    for movie in re.finditer(r"(?s)<h3 class='post-title entry-title'>.*?<a href='(.+?)'>(.+?)</a>.*?</h3>.*?<img.*?src=\"(.+?)\"", label_url_data):

        movie_url = movie.group(1)
        movie_name = movie.group(2)
        movie_name = unescape(movie_name)
        movie_name = addon.unescape(movie_name)        
        movie_name = reformat_movie_name(movie_name) 
        movie_img = movie.group(3)
        
        addon.add_directory({'mode': 'links', 'url' : movie_url, 'title' : movie_name, 'img' : movie_img }, {'title':  movie_name }, img= movie_img)

    next_page_match = re.search(r"<a.*?href='(.+?)' id=.*?title='Older Posts'>", label_url_data)
    if next_page_match:
        next_page_url = addon.unescape( next_page_match.group(1) )
        next_page_url = unescape(next_page_url)
        #next_page_url = next_page_url.replace("&", "%26")
        #next_page_url = next_page_url.replace("?", "%3f")
        addon.add_directory({'mode': 'section', 'url' : next_page_url }, {'title':  'Next Page >>' })
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(url):
    
    movie_url_data = net.http_GET(url).content
    movie_url_data = addon.unescape(movie_url_data)
    movie_url_data = unescape(movie_url_data)

    movie_img = re.search(r"(?s)<div class='post-body entry-content'>.*?<img.*?src=\"(.+?)\".*?</div>", movie_url_data).group(1)                    

    playable_items_match = re.search(r"(?s)<div class='post-body entry-content'>(.+?)<div class='post-footer'>", movie_url_data)
    
    if playable_items_match:
        
        playable_items = playable_items_match.group(1)
        playable_items = addon.unescape(playable_items)        
        playable_items = unescape(playable_items)        

        for playable_item in re.finditer(r"<a.*?href=\"(.+?)\".*?\">(.+?)/a>", playable_items):

            playable_item_url = playable_item.group(1)
            

            if (re.search("bollywoodsantabanta",playable_item_url)):
                
                embed_url_data = net.http_GET(playable_item_url).content

                iframe = re.search("(?s)<div class='post-body entry-content'>.*?<iframe.*?src=\"(.+?)\".*?\"></iframe>", embed_url_data)

                if iframe:
                    playable_item_url = iframe.group(1)                    
                    playable_item_url = playable_item_url.replace("embed-", "")
                    playable_item_url = re.sub(r"-.*?\.",".",playable_item_url)

                    
            elif (re.search("desihome",playable_item_url)):
                
                embed_url_data = net.http_GET(playable_item_url).content

                playable_item_title = playable_item.group(2)
                playable_item_part_match = re.search(r"[Pp]art(.*?)<", playable_item_title)
                playable_item_name_part = ''
                if playable_item_part_match:
                    playable_item_name_part = " - Part" + playable_item_part_match.group(1)

                for iframe in re.finditer("(?s)<div id=tab.*?<iframe.*?src=\"(.+?)\".*?\"></iframe>", embed_url_data):
                    playable_item_url = iframe.group(1)
                    playable_item_url = playable_item_url.replace("embed-", "")                        
                    playable_item_url = re.sub(r"-.*?\.",".",playable_item_url)

                    playable_item_url = playable_item_url.replace("dailymotion.com/embed/", "dailymotion.com/swf/")
                    playable_item_url = playable_item_url.replace(".html", "")                        

                    hosted_media = urlresolver.HostedMediaFile(url=playable_item_url)
                    if hosted_media:

                        playable_item_name = playable_item_url
                        if re.search("http://www.", playable_item_name):
                            playable_item_name = playable_item_name[playable_item_name.index('.')+1:]
                        elif re.search("http://", playable_item_name):
                            playable_item_name = playable_item_name.replace("http://", "")                
                        playable_item_name = playable_item_name[0:playable_item_name.index('.')] + playable_item_name_part

                        queries = {'mode' : 'play', 'url' : playable_item_url, 'title' : title + ' - ' + playable_item_name, 'historytitle': title, 'historylink': sys.argv[0]+sys.argv[2], 'img':movie_img}
                        contextMenuItems = []
                        from universal import playbackengine    
                        contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title + ' - ' + playable_item_name, addon.build_plugin_url( queries ) ) ) )
                                                        
                        addon.add_directory(queries, {'title' : playable_item_name}, contextMenuItems, context_replace=False, img= movie_img)
                
                for iframe in re.finditer("(?s)<div id=tab.*?<embed.*?src=\"(.+?)\".*?\"></embed>", embed_url_data):
                    playable_item_url = iframe.group(1)
                    playable_item_url = playable_item_url.replace("embed-", "")                        
                    playable_item_url = re.sub(r"-.*?\.",".",playable_item_url)

                    playable_item_url = playable_item_url.replace("dailymotion.com/embed/", "dailymotion.com/swf/")
                    playable_item_url = playable_item_url.replace(".html", "")                        

                    hosted_media = urlresolver.HostedMediaFile(url=playable_item_url)
                    if hosted_media:

                        playable_item_name = playable_item_url
                        if re.search("http://www.", playable_item_name):
                            playable_item_name = playable_item_name[playable_item_name.index('.')+1:]
                        elif re.search("http://", playable_item_name):
                            playable_item_name = playable_item_name.replace("http://", "")                
                        playable_item_name = playable_item_name[0:playable_item_name.index('.')] + playable_item_name_part
                        
                        queries={'mode' : 'play', 'url' : playable_item_url, 'title' : title + ' - ' + playable_item_name, 'historytitle': title, 'historylink': sys.argv[0]+sys.argv[2], 'img':movie_img}
                        contextMenuItems = []
                        from universal import playbackengine    
                        contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title + ' - ' + playable_item_name, addon.build_plugin_url( queries ) ) ) )
                                                        
                        addon.add_directory(queries, {'title' : playable_item_name}, contextMenuItems, context_replace=False, img= movie_img)
                continue

            
            playable_item_url = playable_item_url.replace(".html", "")
            playable_item_url = playable_item_url.replace("dailymotion.com/embed/", "dailymotion.com/swf/")
                        
            hosted_media = urlresolver.HostedMediaFile(url=playable_item_url)
            if hosted_media:
                
                playable_item_title = playable_item.group(2)

                playable_item_name = playable_item_url
                if re.search("http://www.", playable_item_name):
                    playable_item_name = playable_item_name[playable_item_name.index('.')+1:]
                elif re.search("http://", playable_item_name):
                    playable_item_name = playable_item_name.replace("http://", "")                
                playable_item_name = playable_item_name[0:playable_item_name.index('.')]
                    
                playable_item_part_match = re.search(r"[Pp]art(.*?)<", playable_item_title)
                if playable_item_part_match:
                    playable_item_name = playable_item_name + " - Part" + playable_item_part_match.group(1)
                
                queries = {'mode' : 'play', 'url' : playable_item_url, 'title' : title + ' - ' + playable_item_name, 'historytitle': title, 'historylink': sys.argv[0]+sys.argv[2], 'img':movie_img}
                contextMenuItems = []
                from universal import playbackengine    
                contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title + ' - ' + playable_item_name, addon.build_plugin_url( queries ) ) ) )

                addon.add_directory(queries, {'title' : playable_item_name }, contextMenuItems, context_replace=False, img= movie_img)
                
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def Play(url):
    from universal import playbackengine
    
    item_title = title
    display_name = title
    
    if queued == 'true':
    
        resolved_media_url = urlresolver.resolve(url)
        if resolved_media_url:
    
            
            player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type='movie', 
                                title=item_title,season='', episode='', year='', watchedCallback=WatchedCallback)
            
            '''
            add to watch history - start
            '''
            wh = watchhistory.WatchHistory(addon_id)
            
            if historylink:
                wh.add_video_item(display_name, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                wh.add_directory(historytitle, historylink, img=img, level='1')
            else:
                wh.add_video_item(display_name, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
            '''
            add to watch history - end
            '''
            
            player.KeepAlive()
    else:
        playbackengine.PlayInPL(display_name, img=img)
         
def ShowSearchDialog():
    last_search = addon.load_data('search')
    if not last_search: last_search = ''
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search')
    keyboard.setDefault(last_search)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        query = keyboard.getText()
        addon.save_data('search',query)
        Search(escape(query), "0")
    else:
        return

def ShowResolverSettingsDialog():
    urlresolver.display_settings()
        
if mode == 'main': 
    MainMenu()
elif mode == 'Browse':
    Browse(section)
elif mode == 'section':
    GetSection(url)
elif mode == 'links':
    GetLinks(url)
elif mode == 'play':
    Play(url)
elif mode == 'Search':
    if start:
        Search(url, start)        
    else:
        ShowSearchDialog()
elif mode == 'Resolver':
    ShowResolverSettingsDialog()
elif mode == 'universalsettings':    
    from universal import _common
    _common.addon.show_settings()
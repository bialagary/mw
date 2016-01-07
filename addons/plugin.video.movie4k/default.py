# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie4k
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc
import xbmcaddon
import xbmcgui
import datetime
import urlparse
import urllib2
import re
import HTMLParser
import codecs

# The following modules require an import entry in the addon.xml.
import urlresolver.types
from xbmcswift2 import Plugin
from bs4 import BeautifulSoup

plugin = Plugin()

MYNAME = "Movie4k.to"
CACHE_TTL = 360 # 6 hours
THUMBNAIL_PATH = os.path.join( plugintools.get_runtime_path() , "resources" , "img" )
FANART = os.path.join( plugintools.get_runtime_path() , "fanart.jpg" )
FORUM_URL = 'http://forums.tvaddons.ag'
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")
HOSTERS_BLACKLIST = [] # ["filenuke", "divxstage", "streamclou", "xvidstage", "rapidvideo"]

if plugintools.get_setting("use_anonymizer_site")=="true":
    ANON_URL = 'http://anonymouse.org/cgi-bin/anon-www.cgi/'
    MAIN_URL = ANON_URL + 'http://www.movie4k.to/'
elif plugintools.get_setting("use_alternative_site_url")=="true":
    MAIN_URL = plugintools.get_setting("alternative_site_url")
    if MAIN_URL[-1] != '/':
        MAIN_URL += '/'
else:
    MAIN_URL = 'http://www.movie4k.to/'

if plugintools.get_setting('clear_cache') == 'true':
    plugin.clear_function_cache()
    plugintools.set_setting('clear_cache', 'false')
    plugintools.log("movie4k clear cache")

# Entry point
def run():
    plugintools.log("movie4k.run")

    # Get params
    params = plugintools.get_params()

    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("movie4k.main_list "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="movies",    title="Movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="tvshows",   title="TV Shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True )
    if plugintools.get_setting("show_adult")=="true":
        plugintools.add_item( action="xxxmovies", title="XXX Movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="search",    title="Search" , thumbnail = os.path.join(THUMBNAIL_PATH,"search.png") , fanart=FANART , folder=True )
    plugintools.add_item( action="settings",  title="Settings" , thumbnail = os.path.join(THUMBNAIL_PATH,"settings.png") , fanart=FANART , folder=False )

# Settings dialog
def settings(params):
    plugintools.log("movie4k.settings "+repr(params))
    plugintools.open_settings_dialog()

# Search
def search(params):
    plugintools.log("movie4k.search "+repr(params))
    text = plugintools.keyboard_input(title="Input search terms")

    url = MAIN_URL+"movies.php?list=search"
    post = "search="+text.replace(" ","+")

    body,response_headers = read_body_and_headers_cached(url, post=post)
    pattern  = '<TR id="coverPreview\d+">(.*?)</TR>'
    matches = plugintools.find_multiple_matches(body,pattern)
    for match in matches:
        pattern = '<a href="([^"]+)">([^<]+).*?<img border=0 src="([^"]+)'
        scrapedurl, scrapedtitle, flag = plugintools.find_single_match(match, pattern)
        pattern = '/img/smileys/(\d).gif'
        quality = plugintools.find_single_match(match, pattern)
        pattern = '<STRONG>(\d+\.*\d*)'
        rating = plugintools.find_single_match(match, pattern)

        url = urljoin(url,scrapedurl)
        title = html_unescape(scrapedtitle)
        title = re.sub('\s+', ' ', title).strip() + "  (" + get_language_from_flag_img(flag) + "  IMDB:" + rating + "  Quality:" + quality + ")"
        plugintools.log("movie4k.search title=" + title + ", url=" + url)

        if "watch-tvshow" in url:
            url = MAIN_URL+"tvshows-season-"+plugintools.find_single_match(url,MAIN_URL+"([A-Za-z0-9\-]+)-watch-tvshow-\d+.html")+".html"
            plugintools.add_item( action="tvshow_seasons", title=title, url=url, fanart=FANART , folder=True )
        else:
            plugintools.add_item( action="single_movie", title=title, url=url, fanart=FANART , folder=True )

# Movies
def movies(params):
    plugintools.log("movie4k.movies "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="movies_cinema",    title="Cinema movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, url=MAIN_URL+"index.php", folder=True )
    plugintools.add_item( action="movies_updates",   title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, url=MAIN_URL+"movies-updates.html", folder=True )
    plugintools.add_item( action="movies_random", title="Random movie", thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png"), fanart=FANART, url=MAIN_URL, folder=True )
    plugintools.add_item( action="letters",          title="All movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, extra="movies-all", url=MAIN_URL+"movies-all.html", folder=True )
    plugintools.add_item( action="genres",           title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"movies.png") , fanart=FANART, extra="movies-genre", url=MAIN_URL+"genres-movies.html", folder=True )

# TV Shows
def tvshows(params):
    plugintools.log("movie4k.tvshows "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="tvshows_featured",  title="Featured" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , url=MAIN_URL+'tvshows_featured.php' )
    plugintools.add_item( action="tvshow_episodes",   title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , url=MAIN_URL+'tvshows-updates.html' )
    plugintools.add_item( action="letters",           title="All TV shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , extra="tvshows-all", url = MAIN_URL+'tvshows-all.html' )
    plugintools.add_item( action="genres",            title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"tvshows.png") , fanart=FANART , folder=True , extra="tvshows-genre", url = MAIN_URL+'genres-tvshows.html' )

# XXX Movies
def xxxmovies(params):
    plugintools.log("movie4k.xxxmovies "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    plugintools.add_item( action="xxx_movies_updates", title="Latest updates" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , url=MAIN_URL+'xxx-updates.html' )
    plugintools.add_item( action="letters",            title="All movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , extra="xxx-all", url=MAIN_URL+'xxx-all.html' )
    plugintools.add_item( action="genres",             title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"xxx.png") , fanart=FANART , folder=True , extra="xxx-genre", url=MAIN_URL+'genres-xxx.html' )

# Cinema movies
def movies_cinema(params):
    plugintools.log("movie4k.movies_cinema "+repr(params))

    #plugintools.set_view(plugintools.MOVIES)

    body,response_headers = read_body_and_headers_cached(params.get("url"))

    pattern = '<div style="float:left">(.*?)<div id="xline">'
    matches = plugintools.find_multiple_matches(body, pattern)
    for match in matches:
        pattern = '<a href="([^"]+)"><img src="([^"]+)'
        scrapedurl, scrapedthumbnail = plugintools.find_single_match(match, pattern)
        pattern = '<font color="#000000">([^<]+)</a>&nbsp; <img src="([^"]+)'
        scrapedtitle, flag = plugintools.find_single_match(match, pattern)
        pattern = 'Genre: <a.*?>(.*?)</a> &nbsp;'
        scrapedgenre = plugintools.find_single_match(match, pattern)
        pattern = 'IMDB Rating:.*?>([^<]+)'
        rating = plugintools.find_single_match(match, pattern)
        pattern = '/img/smileys/(\d).gif'
        quality = plugintools.find_single_match(match, pattern)
        pattern = '<BR>([^<]+)</div>'
        plot = html_unescape(plugintools.find_single_match(match, pattern))
        
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()

        # Cinema movies page displays movies only in one language, no need
        # to show the language code in the title.
        #title += "  " + get_language_from_flag_img(flag) 
        genre = re.sub('</a>.*?>', ', ', scrapedgenre)
        title += "  (IMDB:" + rating + "  Quality:" + quality + "  " + genre + ")"
        thumbnail = urljoin(params.get("url"),scrapedthumbnail)
        plugintools.log("movie4k.movies_cinema title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , plot=plot, fanart=thumbnail, folder=True )

    pattern = '<div id="maincontent2"[^<]+<div style="float: left;"><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        thumbnail = urljoin(params.get("url"),scrapedthumbnail)
        plugintools.log("movie4k.movies_cinema title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail , fanart=thumbnail , folder=True )

# Latest updates
def movies_updates(params):
    plugintools.log("movie4k.movies_updates "+repr(params))
    body,response_headers = read_body_and_headers_cached(params.get("url"))
    only_english = plugintools.get_setting("only_english") == "true"

    pattern  = '<TR id="coverPreview\d+">(.*?)</TR>'
    matches = plugintools.find_multiple_matches(body,pattern)
    for match in matches:
        pattern = '<a href="([^"]+)">([^<]+).*?<img border=0 src="([^"]+)'
        scrapedurl, scrapedtitle, flag = plugintools.find_single_match(match, pattern)
        if not (only_english and get_language_from_flag_img(flag) != "EN"):
            pattern = '/img/smileys/(\d).gif'
            quality = plugintools.find_single_match(match, pattern)
            pattern = '<STRONG>(\d+\.*\d*)'
            rating = plugintools.find_single_match(match, pattern)

            url = urljoin(params.get("url"),scrapedurl)
            title = html_unescape(scrapedtitle).strip()
            title=title + "  (" + get_language_from_flag_img(flag) + "  IMDB:" + rating + "  Quality:" + quality + ")"
            plugintools.log("movie4k.movies_updates title="+title+", url="+url)
            plugintools.add_item( action="single_movie", title=title, url=url, thumbnail='.', fanart=FANART, folder=True )

# Random movie
def movies_random(params):
    plugintools.log("movie4k.movies_random " + repr(params))

    random_single = 'random-movie.html'
    plugintools.add_item(action="single_movie", title='Any genre', url=urljoin(MAIN_URL, random_single), extra='random', thumbnail='.', fanart=FANART , folder=True )

    random_genres = 'genres-movies.html'
    body,response_headers = read_body_and_headers_cached(urljoin(MAIN_URL, random_genres))
    pattern = '<TR>[^<]+<TD id="tdmovies" width="155"><a[^>]+>([^<]+).*?'
    pattern += '<a href="([^"]+)">Random'
    matches = plugintools.find_multiple_matches(body,pattern)
    for scrapedtitle, scrapedurl in matches:
        url = urljoin(MAIN_URL,scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        plugintools.log("movie4k.movies_random title="+title+", url="+url)
        plugintools.add_item(action="single_movie", title=title, url=url, extra='random', thumbnail='.', fanart=FANART, folder=True )

# Latest updates
def xxx_movies_updates(params):
    plugintools.log("movie4k.xxx_movies_updates "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers_cached(params.get("url"))

    pattern  = '<div style="float. left.">'
    pattern += '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        thumbnail = urljoin(params.get("url"),scrapedthumbnail)
        plugintools.log("movie4k.xxx_movies_updates title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="single_movie", title=title, url=url, thumbnail=thumbnail, fanart=thumbnail , folder=True )

# All movies by letter
def letters(params):
    plugintools.log("movie4k.letters " + repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers_cached(params.get("url"))

    # pattern  = '<div id="boxgrey"><a href="(./'+params.get("extra")+'[^"]+)">([^<]+)</a>'
    pattern  = '<div id="boxgrey"><a href="([^"]+)">(\D)</a>'
    matches = plugintools.find_multiple_matches(body,pattern)

    plugintools.add_item(action="letter_pages", title="#", plot="", thumbnail='.', fanart=FANART, url=params.get("url"), folder=True)
    for scrapedurl, letter in matches:
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(letter).strip()
        if params.get("extra")=="tvshows-all":
            extra = "tvshows-all"
        else:
            extra = ""
        plugintools.log("movie4k.letters title=" + title + ', scrapedurl=' + scrapedurl + ", url=" + url)
        plugintools.add_item(action="letter_pages", title=title, thumbnail='.', fanart=FANART, url=url, extra=extra, folder=True)

# All pages for one letter.
def letter_pages(params):
    plugintools.log("movie4k.letter_pages " + repr(params))
    
    body,response_headers = read_body_and_headers_cached(params.get("url"))
    pattern = '<div id="boxgrey"><a href="([^"]+)">(\d+)'
    matches = plugintools.find_multiple_matches(body,pattern)

    plugintools.add_item(action="movies_updates", title="Page 1", thumbnail='.', fanart=FANART, url=params.get("url"), folder=True)
    for scrapedurl, pagenumber in matches:
        url = urljoin(params.get("url"),scrapedurl)
        plugintools.log("movie4k.letters title= Page " + pagenumber + ', scrapedurl=' + scrapedurl + ", url=" + url)
        if params.get("extra")=="tvshows-all":
            plugintools.add_item(action="tvshow_all", title="Page " + pagenumber, thumbnail='.', fanart=FANART, url=url, folder=True)
        else:
            plugintools.add_item(action="movies_updates", title="Page " + pagenumber, thumbnail='.', fanart=FANART, url=url, folder=True)
        
# Movie genres
def genres(params):
    plugintools.log("movie4k.genres "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers_cached(params.get("url"))

    pattern = '<TR>[^<]+<TD id="tdmovies" width="155"><a href="([^"]+)">([^<]+)'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle in matches:
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        plugintools.log("movie4k.genres title="+title+", url="+url)

        if params.get("extra") == "tvshows-genre":
            plugintools.add_item( action="tvshows_all", title=title, url=url, thumbnail='.', fanart=FANART, folder=True )
        else:
            plugintools.add_item( action="letter_pages", title=title, url=url, thumbnail='.', fanart=FANART, folder=True )

# Featured tv shows
def tvshows_featured(params):
    plugintools.log("movie4k.tvshows_featured "+repr(params))

    #plugintools.set_view(plugintools.MOVIES)

    body,response_headers = read_body_and_headers_cached(params.get("url"))
    pattern  = '<div style="float.left"[^<]+'
    pattern += '<a href="([^"]+)"><img src="([^"]+)".*?'
    pattern += '<h2[^<]+<a[^<]+<font[^>]+>([^<]+)</a[^<]+<img src="([^"]+)".*?'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedthumbnail, scrapedtitle, flag in matches:
        
        url = urljoin(params.get("url"),scrapedurl)
        url = MAIN_URL+"tvshows-season-"+plugintools.find_single_match(url,MAIN_URL+"([A-Za-z0-9\-]+)-watch-tvshow-\d+.html")+".html"

        title = html_unescape(scrapedtitle).strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title= title + "  (" + get_language_from_flag_img(flag) + ")"
        thumbnail = urljoin(params.get("url"),scrapedthumbnail)
        plugintools.log("movie4k.tvshows_featured title="+title+", url="+url+", thumbnail="+thumbnail)

        plugintools.add_item( action="tvshow_seasons", title=title, url=url, thumbnail=thumbnail , fanart=thumbnail , folder=True )

# All tv shows by letter
def tvshows_all(params):
    plugintools.log("movie4k.tvshows_all "+repr(params))

    #plugintools.set_view(plugintools.THUMBNAIL)

    body,response_headers = read_body_and_headers_cached(params.get("url"))
    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="538"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a.*?<img border=0 src="([^\"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, flag in matches:
        
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title=title + "  (" + get_language_from_flag_img(flag) + ")"
        plugintools.log("movie4k.tvshows_all title="+title+", url="+url)

        plugintools.add_item( action="tvshow_seasons", title=title, url=url, fanart=FANART , folder=True )

# TV Show seasons
def tvshow_seasons(params):
    plugintools.log("movie4k.tvshow_seasons "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    body,response_headers = read_body_and_headers_cached(params.get("url"))

    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"><a href="([^"]+)">([^<]+)</a></TD[^<]+'
    pattern += '<TD id="tdmovies"><img border=0 src="([^\"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, flag in matches:
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        title = title + "  (" + get_language_from_flag_img(flag) + ")"
        plugintools.log("movie4k.tvshow_seasons title="+title+", url="+url)

        plugintools.add_item( action="tvshow_episodes", title=title, url=url, fanart=FANART , folder=True )

# Latest updates
def tvshow_episodes(params):
    plugintools.log("movie4k.tvshow_episodes "+repr(params))

    #plugintools.set_view(plugintools.LIST)
    body,response_headers = read_body_and_headers_cached(params.get("url"))

    pattern  = '<TR[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"[^<]+'
    pattern += '<a href="([^"]+)">([^<]+)</a></TD[^<]+'
    pattern += '<TD id="tdmovies" width="\d+"[^<]+'
    pattern += '<img[^>]+>([^<]+)</TD[^<]+'
    pattern += '.*?<img border=0 src="([^"]+)"'
    matches = plugintools.find_multiple_matches(body,pattern)

    for scrapedurl, scrapedtitle, mirrorname, flag in matches:
        url = urljoin(params.get("url"),scrapedurl)
        title = html_unescape(scrapedtitle).strip()
        if title.strip().endswith(":"):
            title = title.strip()[:-1]
        title = title + " ("+mirrorname.strip().replace("watch on ","")+")"
        title = title + "  (" + get_language_from_flag_img(flag) + ")"
        plugintools.log("movie4k.tvshow_episodes title="+title+", url="+url)

        for hoster in HOSTERS_BLACKLIST:
            #plugintools.log("<<<<<"+hoster+">>>>> IN <<<<<<"+title.lower()+">>>>>>")
            if hoster in title.lower():
                break;
        else:
            plugintools.add_item( action="play", title=title, url=url, fanart=FANART, folder=True )

def scrap_hosters_list(page_url):
    body,response_headers = read_body_and_headers_cached(page_url)

    hosters = []
    pattern = '<tr id="tablemoviesindex2">(.*?)</tr>'
    pattern += '|Array\(\);.links\[\d+\]=\\"<tr id=\\\\"tablemoviesindex2\\\\">(.*?)</tr>\\";.links\[\d+\]'
    matches = plugintools.find_multiple_matches(body, pattern)
    for match in matches:
        match = "".join(match)
        match = match.replace('\\\"', '\"')
        pattern = '<a href="([^"]+)">([^ ]+)'
        scrapedurl, date_added = plugintools.find_single_match(match, pattern)
        url = urljoin(page_url, scrapedurl)
        pattern = '<img border=0.*?&nbsp;([^<]+)'
        server_name = plugintools.find_single_match(match, pattern)
        # The first [^"]* is for the anonymizer URL.
        pattern = 'src="[^"]*/img/smileys/(\d)\.gif'
        quality = plugintools.find_single_match(match, pattern)
        thumbnail = ""
        hosters.append((url, server_name, quality, date_added, thumbnail))
    return hosters

# Show movie links
def single_movie(params):
    plugintools.log("movie4k.single_movie "+repr(params))

    #plugintools.set_view(plugintools.LIST)
    found = False

    url = params.get("url")
    
    # Resolve the URL of the random movie.
    if 'random' in params.get("extra"):
        body, response_headers = read_body_and_headers(url=params.get("url"), follow_redirects=False)
        url = urljoin(MAIN_URL, dict(response_headers)['location'])
        body, response_headers = read_body_and_headers_cached(url)
    else:
        body, response_headers = read_body_and_headers_cached(url)
    plugintools.log("movie4k.single_movie headers: " + repr(response_headers) + ", url: " + url + ", body: " + repr(body))

    # Add Info and Play list-items with information about the title.
    # Play list-item searches for a valid link and plays it.
    pattern = '<H1.*?000000;">([^<]*)'
    scrapedtitle = plugintools.find_single_match(body, pattern)
    title = html_unescape(scrapedtitle).strip()
    pattern = '<div class="moviedescription">([^<]*)'
    scrapedplot = plugintools.find_single_match(body, pattern)
    plot = html_unescape(scrapedplot).strip()
    pattern = 'IMDB Rating:[^>]*>([^<]+)</a>'
    scrapedrating = plugintools.find_single_match(body, pattern)
    rating = 0.0
    try:
        rating = float(scrapedrating)
    except ValueError as e:
        plugintools.log("movie4k.single_movie " + str(e))
    pattern = 'Genre:(.*?)&nbsp;'
    scrapedgenre = plugintools.find_single_match(body, pattern)
    genre = html_to_text(scrapedgenre).replace(',', ', ')
    pattern = '(?:Length:|Länge:) (.*?)&nbsp;'
    duration = plugintools.find_single_match(body, pattern)
    pattern = 'Land/(?:Year:|Jahr:) ([^<]*)'
    scraped_land_year = plugintools.find_single_match(body, pattern)
    country = ""
    year = 0
    try:
        if '/' in scraped_land_year:
            country, year = scraped_land_year.split('/')
            year = int(year)
        elif scraped_land_year.isdigit():
            year = int(scraped_land_year)
        elif scraped_land_year.isalpha():
            country = scraped_land_year
    except ValueError as e:
        plugintools.log("movie4k.single_movie " + str(e))
    pattern = 'Regie: (.*?)&nbsp;'
    scrapeddirector = plugintools.find_single_match(body, pattern)
    director = html_to_text(scrapeddirector).replace(',', ', ')
    pattern = '(?:Actors:|Schauspieler:) (.*?)<BR>'
    scrapedcast = plugintools.find_single_match(body, pattern)
    cast = html_to_text(scrapedcast).split(',')
    # The first [^"]* is for the anonymizer URL.
    pattern = '<img src="([^"]*https://img.movie4k.tv/thumbs/[^"]*)' 
    thumbnail = plugintools.find_single_match(body, pattern)
    thumbnail = re.sub('https://img.movie4k.tv', 'http://img.movie4k.tv', thumbnail) # otherwise: CCurlFile::Stat - Failed: SSL connect error(35) for https: ...
    plugintools.log("movie4k.single_movie thumbnail_url=" + str(thumbnail))
    info_labels = {"title":title, "plot":plot, "rating":rating, "genre":genre, "duration":duration, "country":country, "year":year, "director":director, "cast":cast}
    plugintools.add_item(action="play_first_playable", title="[I]Play[/I]", url=url, thumbnail=thumbnail, fanart=thumbnail, info_labels=info_labels, isPlayable=True, folder=False)    
    plugintools.add_item(action="info", title="[I]Info[/I]", thumbnail=thumbnail, fanart=thumbnail, info_labels=info_labels, isPlayable=False, folder=False)
    
    # Add hoster list-items.
    hosters = scrap_hosters_list(url)
    for hoster_url, hoster_name, quality, date_added, hoster_thumbnail in hosters:
        title = hoster_name + "  (Quality:" + quality + "  Added:" + date_added + ")"
        plugintools.log("movie4k.single_movie title="+title+", url="+hoster_url+", thumbnail=" + hoster_thumbnail)
        for bad_hoster in HOSTERS_BLACKLIST:
            if bad_hoster in hoster_name.lower():
                break;
        else:
            plugintools.add_item(action="play", title=title, url=hoster_url, thumbnail=hoster_thumbnail,
                                 plot=plot, fanart=thumbnail , folder=True )
            found = True

    if not found:
        play(params)

def info(params):
    '''Show info'''
    xbmc.executebuiltin('Action(Info)')

def play_first_playable(params):
    hosters = scrap_hosters_list(params.get("url"))

    # If the hoster list is empty, then there is only one link and it is on the
    # title's main page.
    if not hosters:
        hosters.append((params.get("url"), '', '', '', ''))
    direct_link = ''
    for url, hoster_name, _, _, _ in hosters:
        hosted_media_url, alternatives = scrap_stream_url(url, True)
        if hosted_media_url:
            try:
                server_name, direct_link = resolve_media_direct_link(hosted_media_url)
            except RuntimeError:
                for alternative in alternatives:
                    hosted_media_url, _ = scrap_stream_url(url, False)
                    if hosted_media_url:
                        try:
                            server_name, direct_link = resolve_media_direct_link(hosted_media_url)
                        except RuntimeError:
                            pass
        if direct_link:
            plugintools.play_resolved_url(direct_link)
            link_location = hoster_name if hoster_name else server_name
            xbmc.sleep(500)
            xbmcgui.Dialog().notification(MYNAME, 'Link found at ' + link_location)
            break
    if not direct_link:
        xbmc.sleep(500)
        xbmcgui.Dialog().notification(MYNAME, 'No links found', xbmcgui.NOTIFICATION_WARNING)

def scrap_stream_url(page_url, scrap_alternatives):
    body,response_headers = read_body_and_headers_cached(page_url)
    url = plugintools.find_single_match(body,'<a target="_blank" href="([^"]+)">')
    if url == "":
        pattern = '<iframe width="600" height="480" frameborder="0" src="([^"]+)"'
        url = plugintools.find_single_match(body, pattern)
    if url != "" and url.startswith("http://www.nowvideo.sx/video/"):
        url = url.replace("http://www.nowvideo.sx/video/","http://embed.nowvideo.eu/embed.php?v=") + "&width=600&height=480"
    plugintools.log("movie4k.play url=" + repr(url))

    alternatives = []
    if scrap_alternatives:
        bloque = plugintools.find_single_match(body,'<SELECT name="hosterlist(.*?)</SELECT')
        pattern  = '<OPTION value="([^"]+)"[^>]+'
        alternatives = plugintools.find_multiple_matches(bloque,pattern)

    return url, alternatives

def resolve_media_direct_link(hosted_media_url):
    if plugintools.get_setting("use_anonymizer_site")=="true":
        plugintools.log("movie4k.resolve original hosted_media_url=" + repr(hosted_media_url))
        # Remove the anonymizer URL from the hosted media url for urlresolver
        # to be able to resolve it properly.
        hosted_media_url = hosted_media_url[len(ANON_URL):]
        plugintools.log("movie4k.resolve truncated hosted_media_url=" + repr(hosted_media_url))
    plugintools.log("movie4k.resolve hosted_media_url=" + repr(hosted_media_url))
    hosted_media_file = urlresolver.types.HostedMediaFile(url=hosted_media_url)
    plugintools.log("movie4k.resolve hosted_media_file=" + repr(bool(hosted_media_file)) + " " + repr(hosted_media_file))
    if hosted_media_file:
        direct_link = hosted_media_file.resolve()
        plugintools.log("movie4k.resolve media_url=" + repr(bool(direct_link)) + " " + repr(direct_link))
        if direct_link:
            return hosted_media_file.get_host(), direct_link
        else:
            raise RuntimeError('Broken link. Try an alternative link or another hoster')
    else:
        raise RuntimeError('Unknown hoster. Try another one')

# Resolve hoster links
def play(params):
    plugintools.log("movie4k.play "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    try:
        scrap_alternatives = "noalternatives" not in params.get("extra")
        url, alternatives = scrap_stream_url(params.get("url"), scrap_alternatives)
    except urllib2.URLError as e:
        plugintools.add_item(action="play", title="Movie4k.to is not responding, please try again", fanart=FANART, isPlayable=True, folder=False )

    # Resolve stream url
    if url:
        try:
            hoster_name, direct_link = resolve_media_direct_link(url)
            plugintools.add_item(action="playable", title="[B]" + hoster_name + "[/B]", url=direct_link, fanart=FANART, isPlayable=True, folder=False )
        except RuntimeError as e:
            plugintools.add_item( action="play", title=str(e), fanart=FANART, isPlayable=True, folder=False )
    else:
        plugintools.add_item( action="play", title="No links found. Try an alternative link or another hoster", fanart=FANART, isPlayable=True, folder=False )

    # Process alternatives
    if alternatives:
        for i, alternative_page_url in enumerate(alternatives):
            url = urljoin(params.get('url'), alternative_page_url)
            counter = str(i+1) + '/' + str(len(alternatives))
            plugintools.add_item(action='play', title='Alternative link ' + counter, url=url, fanart=FANART , folder=True, extra="noalternatives" )
            plugintools.log("movie4k.play alternative=" + url)
    else:
        plugintools.log("movie4k.play noalternatives")

# Play hoster link
def playable(params):
    plugintools.play_resolved_url( params.get("url") )

def get_filename_from_url(url):
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""
    return filename

def get_language_from_flag_img(url):
    if "us_flag" in url:
        return "EN"
    elif "us_ger" in url:
        return "DE"
    elif "flag_greece" in url:
        return "EL"
    elif "flag_spain" in url:
        return "ES"
    elif "flag_france" in url:
        return "FR"
    elif "flag_india" in url:
        return "HI"
    elif "flag_italy" in url:
        return "IT"
    elif "flag_japan" in url:
        return "JA"
    elif "flag_poland" in url:
        return "PL"
    elif "flag_russia" in url:
        return "RU"
    elif "flag_turkey" in url:
        return "TR"
    return ""

@plugin.cached(TTL=CACHE_TTL)
def read_body_and_headers_cached(url, post=None, headers=[], follow_redirects=True, timeout=None):
    plugintools.log("movie4k.read_body_and_headers_cached url=" + url)
    body, response_headers = read_body_and_headers(url, post=post, headers=headers, follow_redirects=follow_redirects, timeout=timeout)
    return body, response_headers

def read_body_and_headers(url, post=None, headers=[], follow_redirects=True, timeout=None):
    plugintools.log("movie4k.read_body_and_headers url="+url)

    # Spoof user agent ID
    headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0"])

    expiration = datetime.datetime.now() + datetime.timedelta(days=365)
    expiration_gmt = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    # The functionality "only movies in english" of the site is broken on the
    # movie's "Latest updates" page (no titles are displayed).  If the option
    # "only_english" is enabled inthe addon preferences, the titles in other
    # languages are filtered out in the movies_updates() function.
    if plugintools.get_setting("only_english")=="true" and not url.endswith('/movies-updates.html'):
        plugintools.log("movie4k.read_body_and_headers only english")
        headers.append(["Cookie","onlylanguage=en; expires="+expiration_gmt+"; xxx2=ok; expires="+expiration_gmt+";"])
    else: #TODO WHY else and not if get_settings(xxx == enabled)???
        headers.append(["Cookie","xxx2=ok; expires="+expiration_gmt+";"])

    body, response_headers = "", ""
    try:
        body,response_headers = plugintools.read_body_and_headers(url,post,headers,follow_redirects,timeout)
        plugintools.log("movie4k.read_body_and_headers response_headers: " + str(response_headers))
    except:
        plugintools.set_setting('clear_cache', 'true')
        import traceback
        plugintools.log("movie4k.read_body_and_headers unexpected error: " + "".join(traceback.format_exception(*sys.exc_info())))
        xbmc.sleep(3000)
        try:
            support_string = "For support, report this error on " + FORUM_URL
            body, response_headers = plugintools.read_body_and_headers(url,post,headers,follow_redirects,timeout)
        except urllib2.HTTPError as e:
            xbmcgui.Dialog().ok(MYNAME, "HTTP error for " + MAIN_URL, 'Reason: ' + str(e.code) + ' ' + str(e.reason), support_string)
        except urllib2.URLError as e:
            xbmcgui.Dialog().ok(MYNAME, "Connection failure for " + MAIN_URL, 'Reason: ' + str(e.reason), support_string)
        except:
            xbmcgui.Dialog().ok(MYNAME, "Unknown connection error: " + str(sys.exc_info()), support_string)
    return body, response_headers

def html_unescape(string):
    if "unescape" not in html_unescape.__dict__:
        html_unescape.unescape = HTMLParser.HTMLParser().unescape
    string = string.decode('utf-8')
    string = html_unescape.unescape(string)
    string = codecs.encode(string, 'utf-8')
    return string

def html_to_text(string):
    plugintools.log("movie4k.html_to_text string=" + string)

    # Use Python's built-in HTML parser (features='html.parser'), because lxml,
    # which is used by default, throws an exception (TypeError: "'NoneType'
    # object is not callable" in 'lxml.etree._ExceptionContext._store_raised')
    # on some inputs for an unkown reason.  The exception deos not appear in
    # the error log, but only in the console output of Kodi and is therefore
    # not easy to debug.
    #
    # Example of the input that triggers the exception:
    #
    # <a href="//movies-genre-2-Drama.html">Drama</a>
    # , <a href="//movies-genre-6-Biography.html">Biography</a>
    # , <a href="//movies-genre-7-Crime.html">Crime</a>
    return BeautifulSoup(string, features='html.parser', from_encoding='utf-8').getText()

def urljoin(base, url):

    # Fix a bug on the tvshows-all page on which relative paths (url parameter)
    # start with '//'.  '//' is interpreted as an absolute url by urlparse and
    # joined incorrectly.
    if url.startswith('//'):
        url = url[2:]
    return urlparse.urljoin(base, url)

run()

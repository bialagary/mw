# -*- coding: utf-8 -*-
#------------------------------------------------------------
# XBMC Add-on for RuYa IPTV
# Version 1.1.2
#------------------------------------------------------------

import os
import sys
import urlparse
import plugintools
import api
import re

SKIN_VIEW_FOR_MOVIES="500"
SKIN_VIEW_FOR_TVSHOWS="500"
SKIN_VIEW_FOR_EPISODES="512"
SKIN_VIEW_FOR_LIVETV="512"

THUMBNAIL_PATH = os.path.join( plugintools.get_runtime_path() , "resources" , "img" )
MAX_ITEMS_PER_PAGE = 10
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")

# Entry point
def run():
    plugintools.log("ruyaiptv.run")
    
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
    plugintools.log("ruyaiptv.main_list "+repr(params))

    if plugintools.get_setting("username")=="":
        settings(params)

    token = api.login( plugintools.get_setting("server") , plugintools.get_setting("username") , plugintools.get_setting("password") )

    if token!="":
        plugintools.set_setting("token",token)
        import os
        plugintools.add_item( action="movies",   title="Movies" , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb0.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )
        plugintools.add_item( action="tvshows",  title="TV Shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb1.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )
        plugintools.add_item( action="livetv",   title="Live TV" , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb2.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
        plugintools.add_item( action="livetv_catchup",   title="Catch-up TV" , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb2.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    else:
        plugintools.message("RuYa IPTV","Invalid login, check your account in add-on settings")

    import os
    plugintools.add_item( action="settings", title="Settings..." , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb3.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart3.jpg") , folder=False )

    if plugintools.get_setting("force_advancedsettings")=="true":
        # Ruta del advancedsettings
        import xbmc,xbmcgui,os
        advancedsettings = xbmc.translatePath("special://userdata/advancedsettings.xml")

        if not os.path.exists(advancedsettings):
            # Copia el advancedsettings.xml desde el directorio resources al userdata
            fichero = open( os.path.join(plugintools.get_runtime_path(),"resources","advancedsettings.xml") )
            texto = fichero.read()
            fichero.close()
            
            fichero = open(advancedsettings,"w")
            fichero.write(texto)
            fichero.close()

            plugintools.message("plugin", "A new file userdata/advancedsettings.xml","has been created for optimal streaming")

    if token!="" and plugintools.get_setting("check_for_updates")=="true":
        import updater
        updater.check_for_updates()

    plugintools.set_view( plugintools.LIST )

# Settings dialog
def settings(params):
    plugintools.log("ruyaiptv.settings "+repr(params))

    if plugintools.get_setting("pincode")!="":
        text = plugintools.keyboard_input(default_text="", title="Enter PIN Code")

        if text==plugintools.get_setting("pincode"):
            plugintools.open_settings_dialog()

    else:
        plugintools.open_settings_dialog()

# Movies
def movies(params):
    plugintools.log("ruyaiptv.movies "+repr(params))

    plugintools.add_item( action="movies_latest_releases", title="Latest releases" , thumbnail = os.path.join(THUMBNAIL_PATH,"hot.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )
    plugintools.add_item( action="movies_recent", title="Recent" , thumbnail = os.path.join(THUMBNAIL_PATH,"recent.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )
    plugintools.add_item( action="movies_az",     title="A-Z" , thumbnail = os.path.join(THUMBNAIL_PATH,"letter.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )
    plugintools.add_item( action="movies_genres", title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )
    plugintools.add_item( action="movies_search", title="Search..." , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def movies_search(params):
    plugintools.log("ruyaiptv.movies_search "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    if params.get("url")=="":
        terms = plugintools.keyboard_input(default_text="", title="Enter search terms")
    else:
        terms = params.get("url")

    items = api.movie_search(token,terms=terms,num_page=current_page)
    for item in items:
        if item["title"].endswith("(3D)"):
            item["title"] = item["title"].replace("(3D)","[COLOR red](3D)[/COLOR]")
        plugintools.add_item( action="play_movie", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="movies_search", title=">> Next page" , url=terms, page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.MOVIES )
    #import xbmcplugin
    #xbmcplugin.setContent( int(sys.argv[1]) ,"Movies" )
    #xbmc.executebuiltin("Container.SetViewMode("+SKIN_VIEW_FOR_MOVIES+")") # Wall

def movies_latest_releases(params):
    plugintools.log("ruyaiptv.movies_latest_releases "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_latest_releases(token,num_page=current_page)
    for item in items:
        if item["title"].endswith("(3D)"):
            item["title"] = item["title"].replace("(3D)","[COLOR red](3D)[/COLOR]")
        plugintools.add_item( action="play_movie", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="movies_latest_releases", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    #import xbmcplugin
    #xbmcplugin.setContent( int(sys.argv[1]) ,"Movies" )
    #xbmc.executebuiltin("Container.SetViewMode("+SKIN_VIEW_FOR_MOVIES+")") # Wall
    plugintools.set_view( plugintools.MOVIES )

def movies_recent(params):
    plugintools.log("ruyaiptv.movies_recent "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_recent_movies(token,num_page=current_page)
    for item in items:
        if item["title"].endswith("(3D)"):
            item["title"] = item["title"].replace("(3D)","[COLOR red](3D)[/COLOR]")
        plugintools.add_item( action="play_movie", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="movies_recent", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    #import xbmcplugin
    #xbmcplugin.setContent( int(sys.argv[1]) ,"Movies" )
    #xbmc.executebuiltin("Container.SetViewMode("+SKIN_VIEW_FOR_MOVIES+")") # Wall
    plugintools.set_view( plugintools.MOVIES )

def movies_az(params):
    plugintools.log("ruyaiptv.movies_az "+repr(params))

    for letra in ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        plugintools.add_item( action="movies_by_letter", title=letra, url=letra, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def movies_by_letter(params):
    plugintools.log("ruyaiptv.movies_az "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    letter = params.get("url")

    items = api.get_movies_by_letter(token,letter,num_page=current_page)
    for item in items:
        if item["title"].endswith("(3D)"):
            item["title"] = item["title"].replace("(3D)","[COLOR red](3D)[/COLOR]")
        plugintools.add_item( action="play_movie", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="movies_by_letter", title=">> Next page" , url=letter , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.MOVIES )

def movies_genres(params):
    plugintools.log("ruyaiptv.movies_az "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_movie_genres(token)
    for item in items:
        plugintools.add_item( action="movies_by_genre", title=item["title"] , url=item["title"], fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def movies_by_genre(params):
    plugintools.log("ruyaiptv.movies_az "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    genre = params.get("url")

    items = api.get_movies_by_genre(token,genre,num_page=current_page)
    for item in items:
        if item["title"].endswith("(3D)"):
            item["title"] = item["title"].replace("(3D)","[COLOR red](3D)[/COLOR]")
        plugintools.add_item( action="play_movie", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="movies_by_genre", title=">> Next page" , url=genre , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart0.jpg") , folder=True )

    plugintools.set_view( plugintools.MOVIES )

# TV Shows
def tvshows(params):
    plugintools.log("ruyaiptv.tvshows "+repr(params))

    plugintools.add_item( action="tvshows_recent_episodes", title="Latest episodes" , thumbnail = os.path.join(THUMBNAIL_PATH,"recent.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )
    plugintools.add_item( action="tvshows_updated",         title="Updated TV Shows" , thumbnail = os.path.join(THUMBNAIL_PATH,"updated.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )
    plugintools.add_item( action="tvshows_az",              title="A-Z" , thumbnail = os.path.join(THUMBNAIL_PATH,"letter.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )
    plugintools.add_item( action="tvshows_genres",          title="Genres" , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )
    plugintools.add_item( action="tvshows_search",          title="Search..." , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def tvshows_search(params):
    plugintools.log("ruyaiptv.tvshows_search "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    if params.get("url")=="":
        terms = plugintools.keyboard_input(default_text="", title="Enter search terms")
    else:
        terms = params.get("url")

    items = api.tvshow_search(token,terms,num_page=current_page)
    for item in items:
        plugintools.add_item( action="tvshow_seasons", title=item["title"] , url=item["title"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="tvshows_search", title=">> Next page" , url=terms , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.TV_SHOWS )

def tvshows_recent_episodes(params):
    plugintools.log("ruyaiptv.tvshows_recent_episodes "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_recent_episodes(token,num_page=current_page)
    for item in items:
        plugintools.add_item( action="play_episode", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="tvshows_recent_episodes", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def tvshows_updated(params):
    plugintools.log("ruyaiptv.tvshows_updated "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_updated_tvshows(token,num_page=current_page)
    for item in items:
        plugintools.add_item( action="tvshow_seasons", title=item["title"] , url=item["title"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="tvshows_updated", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.TV_SHOWS )

def tvshows_az(params):
    plugintools.log("ruyaiptv.tvshows_az "+repr(params))

    for letra in ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        plugintools.add_item( action="tvshows_by_letter", title=letra, url=letra, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def tvshows_by_letter(params):
    plugintools.log("ruyaiptv.tvshows_by_letter "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    letter = params.get("url")

    items = api.get_tvshows_by_letter(token,letter,num_page=current_page)
    for item in items:
        plugintools.add_item( action="tvshow_seasons", title=item["title"] , url=item["title"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="tvshows_by_letter", title=">> Next page" , url=letter , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.TV_SHOWS )

def tvshows_genres(params):
    plugintools.log("ruyaiptv.tvshows_genres "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_tvshow_genres(token)
    for item in items:
        plugintools.add_item( action="tvshows_by_genre", title=item["title"] , url=item["title"], fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def tvshows_by_genre(params):
    plugintools.log("ruyaiptv.tvshows_by_genre "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    genre = params.get("url")

    items = api.get_tvshows_by_genre(token,genre,num_page=current_page)
    for item in items:
        plugintools.add_item( action="tvshow_seasons", title=item["title"] , url=item["title"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="tvshows_by_genre", title=">> Next page" , url=genre , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart1.jpg") , folder=True )

    plugintools.set_view( plugintools.TV_SHOWS )

def tvshow_seasons(params):
    plugintools.log("ruyaiptv.tvshow_episodes "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_tvshow_seasons(token,params.get("url"))
    for item in items:
        plugintools.add_item( action="tvshow_episodes", title=item["title"] , url=item["title"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], extra=params.get("title"), folder=True )

    plugintools.set_view( plugintools.SEASONS )

def tvshow_episodes(params):
    plugintools.log("ruyaiptv.tvshow_episodes "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    tvshow = params.get("extra")
    season = params.get("url")
    items = api.get_tvshow_episodes(token,tvshow,season)
    for item in items:
        plugintools.add_item( action="play_episode", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=item["fanart"], isPlayable=True, folder=False )

    plugintools.set_view( plugintools.EPISODES )

# Live TV
def livetv(params):
    plugintools.log("ruyaiptv.livetv "+repr(params))

    plugintools.add_item( action="livetv_all", title="All channels" , thumbnail = os.path.join(THUMBNAIL_PATH,"hot.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_packages", title="Packages" , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_genres", title="Categories" , thumbnail = os.path.join(THUMBNAIL_PATH,"genres.png") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_epg", title="EPG" , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_epg(params):
    plugintools.log("ruyaiptv.livetv_epg "+repr(params))

    plugintools.add_item( action="livetv_epg_channels", title="EPG by channel" , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_epg_search", title="EPG search..." , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )


def livetv_epg_channels(params):
    plugintools.log("ruyaiptv.livetv_epg_channels "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))
    plugintools.log("ruyaiptv.livetv_epg_channels current_page="+repr(current_page)+" next_page="+next_page)

    items = api.get_livetv_epg_channels(num_page=current_page)
    for item in items:
        plugintools.add_item( action="livetv_epg_by_channel", title=item["title"] , url=item["url"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_epg_channels", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_epg_by_channel(params):
    plugintools.log("ruyaiptv.livetv_epg_by_channel "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    channel = params.get("url")

    items = api.get_livetv_epg_by_channel(channel,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="", title=format_title(item["title"]).strip() , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_epg_by_channel", title=">> Next page" , url=channel , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def livetv_epg_search(params):
    plugintools.log("ruyaiptv.livetv_epg_search "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    if params.get("url")=="":
        terms = plugintools.keyboard_input(default_text="", title="Enter search terms")
    else:
        terms = params.get("url")

    items = api.livetv_epg_search(terms,num_page=current_page)
    for item in items:
        plugintools.add_item( action="", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_epg_by_genre", title=">> Next page" , url=terms, page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )
    #import xbmcplugin
    #xbmcplugin.setContent( int(sys.argv[1]) ,"Movies" )
    #xbmc.executebuiltin("Container.SetViewMode("+SKIN_VIEW_FOR_MOVIES+")") # Wall







def livetv_catchup(params):
    plugintools.log("ruyaiptv.livetv_catchup "+repr(params))

    plugintools.add_item( action="livetv_catchup_countries", title="Recordings by channel" , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_catchup_genres", title="Recordings by genre" , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    plugintools.add_item( action="livetv_catchup_search", title="Search..." , thumbnail = os.path.join(THUMBNAIL_PATH,"") , fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )


def livetv_catchup_search(params):
    plugintools.log("ruyaiptv.livetv_catchup_search "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    if params.get("url")=="":
        terms = plugintools.keyboard_input(default_text="", title="Enter search terms")
    else:
        terms = params.get("url")

    items = api.livetv_catchup_search(terms,num_page=current_page)
    for item in items:
        plugintools.add_item( action="play_catchup", title=item["title"] , url=item["url"] , plot=item["plot"], thumbnail=item["thumbnail"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_by_genre", title=">> Next page" , url=terms, page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )
    #import xbmcplugin
    #xbmcplugin.setContent( int(sys.argv[1]) ,"Movies" )
    #xbmc.executebuiltin("Container.SetViewMode("+SKIN_VIEW_FOR_MOVIES+")") # Wall

def livetv_catchup_countries(params):
    plugintools.log("ruyaiptv.livetv_catchup_countries "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_livetv_catchup_countries(num_page=current_page)
    for item in items:
        plugintools.add_item( action="livetv_catchup_categories_by_country", title=item["title"] , url=item["url"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_countries", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_catchup_categories_by_country(params):
    plugintools.log("ruyaiptv.livetv_catchup_categories_by_country "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    country = params.get("url")

    items = api.get_livetv_catchup_categories_by_country(country,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="livetv_catchup_channels_by_category", title=item["title"] , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_categories_by_country", title=">> Next page" , url=genre , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def livetv_catchup_channels_by_category(params):
    plugintools.log("ruyaiptv.livetv_catchup_channels_by_category "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    category = params.get("url")

    items = api.get_livetv_catchup_channels_by_category(category,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="livetv_catchup_dates_by_channel", title=item["title"] , url=item["url"] , thumbnail="", plot="", fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_channels_by_category", title=">> Next page" , url=category , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def livetv_catchup_dates_by_channel(params):
    plugintools.log("ruyaiptv.livetv_catchup_dates_by_channel "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    channel = params.get("url")

    items = api.get_livetv_catchup_dates_by_channel(channel,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="livetv_catchup_by_channel_and_date", title=item["title"] , url=item["url"] , thumbnail="", plot="", fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=True )

    plugintools.set_view( plugintools.EPISODES )

def livetv_catchup_by_channel_and_date(params):
    plugintools.log("ruyaiptv.livetv_catchup_by_channel_and_date "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    channel = params.get("url")
    date = params.get("title")

    items = api.get_livetv_catchup_by_channel_and_date(channel,date,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="play_catchup", title=format_title(item["title"]).strip() , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    plugintools.set_view( plugintools.EPISODES )

def livetv_catchup_genres(params):
    plugintools.log("ruyaiptv.livetv_catchup_genres "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    items = api.get_livetv_catchup_genres(num_page=current_page)
    for item in items:
        plugintools.add_item( action="livetv_catchup_by_genre", title=item["title"] , url=item["title"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_genres", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_catchup_by_genre(params):
    plugintools.log("ruyaiptv.livetv_catchup_by_genre "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    genre = params.get("url")

    items = api.get_livetv_catchup_by_genre(genre,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="play_catchup", title=format_title(item["title"]).strip() , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_by_genre", title=">> Next page" , url=genre , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def livetv_catchup_channels(params):
    plugintools.log("ruyaiptv.livetv_catchup_channels "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))
    plugintools.log("ruyaiptv.livetv_catchup_channels current_page="+repr(current_page)+" next_page="+next_page)

    items = api.get_livetv_catchup_channels(num_page=current_page)
    for item in items:
        plugintools.add_item( action="livetv_catchup_by_channel", title=item["title"] , url=item["url"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_channels", title=">> Next page" , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_catchup_by_channel(params):
    plugintools.log("ruyaiptv.livetv_catchup_by_channel "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    current_page , next_page = get_current_and_next_page(params.get("page"))

    channel = params.get("url")

    items = api.get_livetv_catchup_by_channel(channel,num_page=current_page)
    for item in items:
        plugintools.log(repr(item))
        plugintools.add_item( action="play_catchup", title=format_title(item["title"]).strip() , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    if len(items)>=MAX_ITEMS_PER_PAGE:
        plugintools.add_item( action="livetv_catchup_by_channel", title=">> Next page" , url=channel , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.EPISODES )

def format_title(title):
    partes = title.split(" (Now")
    if len(partes)==2:
        new_title = "  [COLOR white]"+partes[0]+"[/COLOR]"+" (Now"+partes[1]
    else:
        if title.strip().startswith("---"):
            new_title = "[COLOR blue]"+re.compile("[\-]+",re.DOTALL).sub("",title).strip()+"[/COLOR]"
        else:
            new_title = "  [COLOR white]"+title+"[/COLOR]"

    return new_title

def livetv_all(params):
    plugintools.log("ruyaiptv.livetv_all "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_all_livetv_channels(token)
    for item in items:
        plugintools.add_item( action="play_livetv", title=format_title(item["title"]) , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , extra=item["fanart"], isPlayable=True, folder=False )

    plugintools.set_view( plugintools.EPISODES )

def livetv_genres(params):
    plugintools.log("ruyaiptv.livetv_genres "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_livetv_genres(token)
    for item in items:
        plugintools.add_item( action="livetv_by_genre", title=item["title"] , url=item["title"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_packages(params):
    plugintools.log("ruyaiptv.livetv_packages "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    items = api.get_livetv_packages(token)
    for item in items:

        plugintools.add_item( action="livetv_by_package", title=item["title"] , url=item["title"], thumbnail=api.get_base_url()+"img/package/"+item["title"]+".png", fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.set_view( plugintools.LIST )

def livetv_by_genre(params):
    plugintools.log("ruyaiptv.livetv_by_genre "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    genre = params.get("url")

    items = api.get_livetv_channels_by_genre(token,genre)
    for item in items:
        plugintools.add_item( action="play_livetv", title=format_title(item["title"]).strip() , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    plugintools.set_view( plugintools.EPISODES )

def livetv_by_package(params):
    plugintools.log("ruyaiptv.livetv_by_package "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    package = params.get("url")

    items = api.get_livetv_channels_by_package(token,package)
    for item in items:
        plugintools.add_item( action="play_livetv", title=format_title(item["title"]) , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )

    plugintools.set_view( plugintools.EPISODES )

def play_catchup(params):
    plugintools.log("ruyaiptv.play_catchup "+repr(params))

    mediaurl = params.get("url")

    plugintools.play_resolved_url( mediaurl )

def play_movie(params):
    plugintools.log("ruyaiptv.play_movie "+repr(params))

    mediaurl = params.get("url")

    if "|" in params.get("url"):

        if plugintools.get_setting("quality_selector")=="0":
            selected = plugintools.selector(["Watch in SD","Watch in HD"],"Select quality")
            if selected==-1:
                return
        elif plugintools.get_setting("quality_selector")=="1":
            selected = 0
        elif plugintools.get_setting("quality_selector")=="2":
            selected = 1

        mediaurl = params.get("url").split("|")[selected]

    plugintools.play_resolved_url( mediaurl )

def play_episode(params):
    return play_movie(params)

def play_livetv(params):
    plugintools.log("ruyaiptv.play_livetv "+repr(params))

    token = plugintools.get_setting("token")
    if token=="":
        return

    mediaurl = params.get("url")
    plugintools.log("ruyaiptv.play_livetv mediaurl="+repr(mediaurl))
    
    if "|" in params.get("url"):

        if plugintools.get_setting("quality_selector_live")=="0":
            plugintools.log("ruyaiptv.play_livetv asking for quality")
            selected = plugintools.selector(["Watch in SD","Watch in HD"],"Select quality")
            if selected==-1:
                return
        elif plugintools.get_setting("quality_selector_live")=="1":
            plugintools.log("ruyaiptv.play_livetv default to SD quality")
            selected = 0
        elif plugintools.get_setting("quality_selector_live")=="2":
            plugintools.log("ruyaiptv.play_livetv default to HD quality")
            selected = 1

        mediaurl = params.get("url").split("|")[selected]
        plugintools.log("ruyaiptv.play_livetv mediaurl="+repr(mediaurl))

    plugintools.log("ruyaiptv.play_livetv mediaurl="+repr(mediaurl))
    mediaurl = api.get_livetv_url(token,mediaurl)
    plugintools.log("ruyaiptv.play_livetv mediaurl="+repr(mediaurl))
    plugintools.play_resolved_url( mediaurl )

def get_current_and_next_page(current_page):
    if current_page=="":
        current_page="0"

    next_page = str(int(current_page)+1)

    return current_page,next_page

run()
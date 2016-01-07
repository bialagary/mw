'''
    ** My Favorites ** XBMC Plugin
    Copyright (C) 2013 XUNITYTALK.com

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

import os
import string
import sys
import re
import urlresolver
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

from metahandler import metahandlers

net = Net()
addon_id = 'plugin.video.favorites'
addon = Addon(addon_id, sys.argv)

def AddSysPath(path):
    if path not in sys.path:
        sys.path.append(path)

#PATHS
AddonPath = addon.get_path()

from universal import favorites
fav = favorites.Favorites(addon_id, sys.argv)

#VARIABLES
VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'
VideoType_Link = 'link'

mode = addon.queries['mode']
fav_addon_id = addon.queries.get('addon_id', '')
section = addon.queries.get('section', '')
sub_section = addon.queries.get('sub_section', '')
local = addon.queries.get('local', '')
item_mode = addon.queries.get('item_mode', 'main')



def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
  
meta_setting = str2bool(addon.get_setting('use-meta'))

metaget=metahandlers.MetaData()
  
  
#################### Meta-Data related functions ##################################

def refresh_movie(vidtitle, year=''):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
        
    search_meta = metaget.search_movies(vidtitle)
    
    if search_meta:
        movie_list = []
        for movie in search_meta:
            movie_list.append(movie['title'] + ' (' + str(movie['year']) + ')')
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose', movie_list)
        
        if index > -1:
            new_imdb_id = search_meta[index]['imdb_id']
            new_tmdb_id = search_meta[index]['tmdb_id']       
            meta = metaget.update_meta('movie', vidtitle, imdb_id=imdb_id, new_imdb_id=new_imdb_id, new_tmdb_id=new_tmdb_id, year=year)   
            xbmc.executebuiltin("Container.Refresh")
    else:
        msg = ['No matches found']
        addon.show_ok_dialog(msg, 'Refresh Results')


def episode_refresh(vidname, imdb, season_num, episode_num):
    #refresh info for an episode   
    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
        
    metaget.update_episode_meta(vidname, imdb, season_num, episode_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")


def season_refresh(vidname, imdb, season_num):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()          	
        
    metaget.update_season(vidname, imdb, season_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def get_metadata(video_type, vidtitle, vidname='', year='', imdb='', season_list=None, season_num=0, episode_num=0, img=''):    
    meta = {}
    
    if meta_setting:
        #Get Meta settings
        poster = addon.get_setting('movie-poster')
        fanart = addon.get_setting('movie-fanart')
        
        if video_type in (VideoType_Movies, VideoType_TV):
            meta = metaget.get_meta(video_type, vidtitle, year=year)
            
        returnlist = True
        if video_type == VideoType_Season:            
            if not season_list:
                season_list = []
                season_list.append(season_num)
                returnlist = False
            meta = metaget.get_seasons(vidtitle, imdb, season_list)
            if not returnlist:
                meta = meta[0]
    
        if video_type == VideoType_Episode:
            meta=metaget.get_episode_meta(vidname, imdb, season_num, episode_num)
        
        if not returnlist:
            #Check for and blank out covers if option disabled
            if poster == 'false':
                meta['cover_url'] = ''                    
            #Check for and blank out fanart if option disabled
            if fanart == 'false':
                meta['backdrop_url'] = ''        
            if meta.get('title', '') == '':
                meta['title'] = vidname
            if meta.get('cover_url', '') == '':
                meta['cover_url'] = img
            if meta.get('imdb_id', '') == '':
                meta['imdb_id'] = imdb
            if meta.get('backdrop_url', '') == '':
                meta['backdrop_url'] = ''
            if meta.get('year', '') == '':
                meta['year'] = year
            if meta.get('overlay', '') == '':
                meta['overlay'] = 0
        
    else:
        
        meta['title'] = vidname
        meta['cover_url'] = img
        meta['imdb_id'] = imdb
        meta['backdrop_url'] = ''
        meta['year'] = year
        meta['overlay'] = 0
        if video_type in (VideoType_TV, VideoType_Episode):
            meta['TVShowTitle'] = vidtitle                    

    return meta

def AddFavoriteItems(fav_addon_id, section='', sub_section='', item_mode='main'):

    fav_items=''    
    fav_items_1=''
    str_fav_items_1=''
    if not section:
        fav_items = fav.get_main_sections(fav_addon_id, item_mode)    
    elif section and sub_section:
        fav_items = fav.get_favorites(section, sub_section, fav_addon_id, item_mode)
    else:
        fav_items = fav.get_sub_sections(section, fav_addon_id, item_mode)
        if len(fav_items) <= 0:
            sub_section = 'all'
            fav_items = fav.get_favorites(section, sub_section, fav_addon_id, item_mode)
        else:
            fav_items_1 = fav.get_favorites(section, '', fav_addon_id, item_mode)
            str_fav_items_1=str(fav_items_1)
            fav_items = fav_items + fav_items_1
        
    for item in fav_items:
    
        tmp_section = section
        tmp_sub_section = sub_section
    
        str_item = str(item)
        item = dict(item)
        title = item['title']
        if not local:
            title = re.sub('\[.+?\]', '', title)
        
        if (section and sub_section) or (str_item in str_fav_items_1):
            infolabels = item['infolabels']
                
            img = item['image_url']
            fanart = item['fanart_url']
            
            if infolabels and infolabels.get('supports_meta', 'false') == 'true':
                infolabels = get_metadata(infolabels.get('video_type', ''), infolabels.get('name', ''), infolabels.get('name', ''), infolabels.get('year', ''), 
                                            imdb=infolabels.get('imdb_id', ''), season_num=infolabels.get('season', ''), 
                                            episode_num=infolabels.get('episode', ''), img=item['image_url'])

                if infolabels.get('cover_url', '') != '': img = infolabels.get('cover_url', '')
                if infolabels.get('backdrop_url', '') != '': fanart = infolabels.get('backdrop_url', '')
            
            listitem = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
            listitem.setInfo(type="video", infoLabels=infolabels)            
            listitem.setProperty('fanart_image', fanart)            
            listitem.setProperty('IsPlayable', item['isplayable'])
            
            tmp_fav_addon_id = item['addon_id']
            tmp_fav = favorites.Favorites(tmp_fav_addon_id, sys.argv)
            context_menu_items = []
            context_menu_items.append(('Show Information', 'XBMC.Action(Info)'))
            context_menu_items.append(('Delete from Favorites', tmp_fav.delete_item(title, section_title=item['section_title'], section_addon_title=item['section_addon_title'], sub_section_title=item['sub_section_title'], sub_section_addon_title=item['sub_section_addon_title'], item_mode=item_mode)))
            listitem.addContextMenuItems(context_menu_items, replaceItems=True)                    

            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=item['url']+'&favortite=true',isFolder=str2bool(item['isfolder']),listitem=listitem)

        else:
            if tmp_section:
                tmp_sub_section = title
            else:
                tmp_section = title
            addon.add_directory({ 'mode':'browse', 'addon_id' : fav_addon_id, 'local' : local, 'section' : tmp_section, 'sub_section' : tmp_sub_section, 'item_mode':item_mode}, {'title' : title.title()} )
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
  
def MainMenu():  #home-page

    addon.add_directory({ 'mode':'browse', 'addon_id': 'all'}, {'title' : 'All'})
    addon.add_directory({ 'mode':'byaddons'}, {'title' : 'By Addons'} )
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def ByAddons():  #home-page    

    addons = fav.get_addons_that_have_favorites()
    
    for tmp_addon in addons:
        
        addon.add_directory({ 'mode':'browse', 'addon_id' : tmp_addon['id']}, {'title' : tmp_addon['title']}, img=tmp_addon['img'], fanart=tmp_addon['fanart'] )
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    

if mode == 'main': 
    MainMenu()
elif mode == 'browse':
    AddFavoriteItems(fav_addon_id, section, sub_section, item_mode)
elif mode == 'byaddons':
    ByAddons()
elif mode == 'universalsettings':    
    favorites.settings()
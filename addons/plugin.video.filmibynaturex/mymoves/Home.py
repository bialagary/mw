'''
Created on Nov 20, 2012

@author: ajju
'''
from TurtleContainer import Container
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport
from common import AddonUtils


def displayMenuItems(request_obj, response_obj):
    
    addonContext = Container().getAddonContext()
    
    # HD Movies
    hd_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='HD_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('HDMovie')
    xbmcListItem = xbmcgui.ListItem(label='HD MOVIES', iconImage=hd_movie_icon_filepath, thumbnailImage=hd_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
                             
    # Movies item
    movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('Movie')
    xbmcListItem = xbmcgui.ListItem(label='All Movies', iconImage=movie_icon_filepath, thumbnailImage=movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # A-Z
#     az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='AZ_Dir_V1.png')
#     item = ListItem()
#     item.set_next_action_name('AZ')
#     xbmcListItem = xbmcgui.ListItem(label='Movies A to Z', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
#     item.set_xbmc_list_item_obj(xbmcListItem)
#     response_obj.addListItem(item)
    
    
    # Movies By Year
    az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Release_Decades_V1.png')
    item = ListItem()
    item.set_next_action_name('ByYear')
    xbmcListItem = xbmcgui.ListItem(label='Movies By Year', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    
    # Movies By Genre
    az_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('ByGenre')
    xbmcListItem = xbmcgui.ListItem(label='Movies By Genre', iconImage=az_movie_icon_filepath, thumbnailImage=az_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # English Subtitles Movies
    punjabi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'English%20Subtitled')
    xbmcListItem = xbmcgui.ListItem(label='English Subtitles', iconImage=punjabi_movie_icon_filepath, thumbnailImage=punjabi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
#     response_obj.addListItem(item)
    
    # Hindi Dubbed Movies
    punjabi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'hindi-dubbed')
    xbmcListItem = xbmcgui.ListItem(label='Hindi Dubbed', iconImage=punjabi_movie_icon_filepath, thumbnailImage=punjabi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    
    # Trailers
    trailer_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Trailers.png')
    item = ListItem()
    item.set_next_action_name('Trailer')
    item.add_request_data('categoryUrlSuffix', 'Trailer')
    xbmcListItem = xbmcgui.ListItem(label='Trailers', iconImage=trailer_movie_icon_filepath, thumbnailImage=trailer_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    
    # YouTube TV item
    youtube_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='YouTube_V1.png')
    item = ListItem()
    item.set_next_action_name('YouTube')
    xbmcListItem = xbmcgui.ListItem(label='YouTube Channels', iconImage=youtube_icon_filepath, thumbnailImage=youtube_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


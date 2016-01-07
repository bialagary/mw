'''
Created on Mar 30, 2013

@author: ajju
'''
from TurtleContainer import Container
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport
from common import AddonUtils, ExceptionHandler
from common import XBMCInterfaceUtils


def displayMainMenu(request_obj, response_obj):
    addonContext = Container().getAddonContext()
    
    # Hindi Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Hindi_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'hindi-movies')
    xbmcListItem = xbmcgui.ListItem(label='HINDI', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Telugu Movies
    telugu_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Telugu_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'telugu')
    xbmcListItem = xbmcgui.ListItem(label='TELUGU', iconImage=telugu_movie_icon_filepath, thumbnailImage=telugu_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Tamil Movies
    tamil_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Tamil_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'tamil')
    xbmcListItem = xbmcgui.ListItem(label='TAMIL', iconImage=tamil_movie_icon_filepath, thumbnailImage=tamil_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Punjabi Movies
    punjabi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'punjabi')
    xbmcListItem = xbmcgui.ListItem(label='PUNJABI', iconImage=punjabi_movie_icon_filepath, thumbnailImage=punjabi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Malayalam Movies
    malayalam_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Malayalam_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'malayalam')
    xbmcListItem = xbmcgui.ListItem(label='MALAYALAM', iconImage=malayalam_movie_icon_filepath, thumbnailImage=malayalam_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    

def displayHDMainMenu(request_obj, response_obj):
    addonContext = Container().getAddonContext()
    # All Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='HD_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'bluray')
    xbmcListItem = xbmcgui.ListItem(label='All HD Movies', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Hindi Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Hindi_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'hindi-blurays')
    xbmcListItem = xbmcgui.ListItem(label='HINDI', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Telugu Movies
    telugu_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Telugu_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'telugu-blurays')
    xbmcListItem = xbmcgui.ListItem(label='TELUGU', iconImage=telugu_movie_icon_filepath, thumbnailImage=telugu_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Tamil Movies
    tamil_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Tamil_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('listMovies')
    item.add_request_data('categoryUrlSuffix', 'tamil-blurays')
    xbmcListItem = xbmcgui.ListItem(label='TAMIL', iconImage=tamil_movie_icon_filepath, thumbnailImage=tamil_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


def displayUC(request_obj, response_obj):
    print 'UNDER CONSTRUCTION'
    XBMCInterfaceUtils.displayDialogMessage(heading='UNDER Construction', line1='Please wait for update!!', line2='Enjoy HD movies for the time being.', line3='')
    
    
def displayAtoZMenu(request_obj, response_obj):
    addonContext = Container().getAddonContext()
    # Hindi Movies
    hindi_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Hindi_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('ChooseChar')
    item.add_request_data('categorySuffix', '_H')
    xbmcListItem = xbmcgui.ListItem(label='HINDI', iconImage=hindi_movie_icon_filepath, thumbnailImage=hindi_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Telugu Movies
    telugu_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Telugu_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('ChooseChar')
    item.add_request_data('categorySuffix', '_T')
    xbmcListItem = xbmcgui.ListItem(label='TELUGU', iconImage=telugu_movie_icon_filepath, thumbnailImage=telugu_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Tamil Movies
    tamil_movie_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Tamil_Movies_V1.png')
    item = ListItem()
    item.set_next_action_name('ChooseChar')
    item.add_request_data('categorySuffix', '_TT')
    xbmcListItem = xbmcgui.ListItem(label='TAMIL', iconImage=tamil_movie_icon_filepath, thumbnailImage=tamil_movie_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    

def displayAtoZList(request_obj, response_obj):
    d = xbmcgui.Dialog()
    chars = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    index = d.select('Select Category:', chars)
    if index == -1:
        raise Exception(ExceptionHandler.EXCEPTIONS.get(ExceptionHandler.CATEGORY_NOT_SELECTED));
    char = chars[index]
    if index == 0:
        char = '%23'
    categoryUrl = char + request_obj.get_data()['categorySuffix']
    request_obj.set_data({'categoryUrlSuffix': categoryUrl})
    

def displayYearList(request_obj, response_obj):
    d = xbmcgui.Dialog()
    years = ['2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', 'Pre-2000']
    index = d.select('Select year:', years)
    if index == -1:
        raise Exception(ExceptionHandler.EXCEPTIONS.get(ExceptionHandler.CATEGORY_NOT_SELECTED));
    year = years[index]
    request_obj.set_data({'categoryUrlSuffix': year.lower()})
    
def displayGenreList(request_obj, response_obj):
    d = xbmcgui.Dialog()
    genres = ['Action', 'Comedy', 'Crime', 'Drama', 'Horror', 'Romance', 'Social', 'Thriller']
    index = d.select('Select genre:', genres)
    if index == -1:
        raise Exception(ExceptionHandler.EXCEPTIONS.get(ExceptionHandler.CATEGORY_NOT_SELECTED));
    genre = genres[index]
    request_obj.set_data({'categoryUrlSuffix': genre.lower()})
    
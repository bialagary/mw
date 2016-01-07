
from common import XBMCInterfaceUtils, Logger
from metahandler import metahandlers  # @UnresolvedImport
import sys


    
def retieveMovieInfoAndAddItem(request_obj, response_obj):
    items = response_obj.get_item_list()
    XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__addMovieInfo_in_item'), items, 'Retrieving MOVIE info', 'Failed to retrieve movie information, please try again later')

__metaget__ = None

def __addMovieInfo_in_item(item):
    if item.get_next_action_name() == 'Movie_Streams':
        year = unicode(item.get_moving_data()['movieYear'], errors='ignore').encode('utf-8')
        title = unicode(item.get_moving_data()['movieTitle'], errors='ignore').encode('utf-8')
        meta = None
        try:
            global __metaget__
            if __metaget__ is None:
                __metaget__ = metahandlers.MetaData()
            meta = __metaget__.get_meta('movie', title, year=year)
        except:
            Logger.logDebug('Failed to load metahandler module')
        xbmc_item = item.get_xbmc_list_item_obj()
        
        if(meta is not None):
            xbmc_item.setIconImage(meta['thumb_url'])
            xbmc_item.setThumbnailImage(meta['cover_url'])
            videoInfo = {'trailer_url':meta['trailer_url']}
            for key, value in meta.items():
                if type(value) is str:
                    value = unicode(value).encode('utf-8')
                videoInfo[key] = value
            xbmc_item.setInfo('video', videoInfo)
            xbmc_item.setProperty('fanart_image', meta['backdrop_url'])
            item.add_request_data('videoInfo', videoInfo)
            
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            xbmc_item.addContextMenuItems(contextMenuItems, replaceItems=False)
        else:
            xbmc_item.setInfo('video', {'title':title, 'year':year})
            item.add_request_data('videoInfo', {'title':title, 'year':year})


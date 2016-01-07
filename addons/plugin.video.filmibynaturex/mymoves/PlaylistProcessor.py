'''
Created on Nov 24, 2011

@author: ajju
'''
from common import AddonUtils
from common.DataObjects import ListItem
import urllib
import xbmcgui  # @UnresolvedImport

def preparePlayListItems(request_obj, response_obj):
    if request_obj.get_data().has_key('videoPlayListItems'):
        playList = request_obj.get_data()['videoPlayListItems']
        for videoItem in playList:
            data = {}
            data['videoLink'] = videoItem['videoLink']
            data['videoTitle'] = videoItem['videoTitle']
            item = ListItem()
            item.add_moving_data('videoStreamUrl', 'plugin://plugin.video.filmibynaturex/?actionId=snap_and_resolve_video&data=' + urllib.quote_plus(AddonUtils.encodeData(data)))
            item.set_next_action_name('Play')
            xbmcListItem = xbmcgui.ListItem(label=videoItem['videoTitle'])
            if(request_obj.get_data().has_key('videoInfo')):
                meta = request_obj.get_data()['videoInfo']
                xbmcListItem.setIconImage(meta['thumb_url'])
                xbmcListItem.setThumbnailImage(meta['cover_url'])
                xbmcListItem.setInfo('video', meta)
            item.set_xbmc_list_item_obj(xbmcListItem)
            response_obj.addListItem(item)

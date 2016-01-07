
from common import HttpUtils, XBMCInterfaceUtils
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport
try:
    import json
except ImportError:
    import simplejson as json
    
def showUserUploads(request_obj, response_obj):
    try:
        items = None
        if request_obj.get_data().has_key('pageNbr'):
            items = retrieveUserUploads(request_obj.get_data()['userId'], request_obj.get_data()['pageNbr'])
        else:
            items = retrieveUserUploads(request_obj.get_data()['userId'])
        response_obj.set_item_list(items)
    except:
        XBMCInterfaceUtils.displayDialogMessage('No video items found!', 'This channel does not contain any video items.')

def retrieveUserUploads(userId, pageNbr=0, maxCount=50):
    url = 'http://gdata.youtube.com/feeds/api/users/' + userId + '/uploads?alt=json&v=2&max-results=' + str(maxCount) + '&start-index=' + str((pageNbr * maxCount) + 1)
    jData = json.loads(HttpUtils.HttpClient().getHtmlContent(url))
    entries = jData['feed']['entry']
    
    items = []
    for entry in entries:
        videoId = entry['media$group']['yt$videoid']['$t']
        title = unicode(entry['title']['$t']).encode('utf-8')
        thumbnail = entry['media$group']['media$thumbnail'][1]['url']
        
        item = ListItem()
        item.add_request_data('videoLink', 'http://www.youtube.com/watch?v=' + videoId + '&')
        item.add_request_data('videoTitle', title)
        item.set_next_action_name('play_Video')
        xbmcListItem = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail)
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    if(len(items) == maxCount):
        item = ListItem()
        item.add_request_data('userId', userId)
        item.add_request_data('pageNbr', pageNbr + 1)
        item.set_next_action_name('show_Videos')
        xbmcListItem = xbmcgui.ListItem(label='---- Next Page ---->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    return items


def showUserPlaylists(request_obj, response_obj):
    try:
        items = None
        if request_obj.get_data().has_key('pageNbr'):
            items = retrieveUserPlaylists(request_obj.get_data()['userId'], request_obj.get_data()['pageNbr'])
        else:
            items = retrieveUserPlaylists(request_obj.get_data()['userId'])
        response_obj.set_item_list(items)
    except:
        XBMCInterfaceUtils.displayDialogMessage('No playlist items found!', 'This channel does not contain any Playlist items.')
    
def retrieveUserPlaylists(userId, pageNbr=0, maxCount=50):
    url = 'http://gdata.youtube.com/feeds/api/users/' + userId + '/playlists?alt=json&v=2&max-results=' + str(maxCount) + '&start-index=' + str((pageNbr * maxCount) + 1)

    jData = json.loads(HttpUtils.HttpClient().getHtmlContent(url))
    entries = jData['feed']['entry']
    items = []
    for entry in entries:

        playlistId = unicode(entry['yt$playlistId']['$t']).encode('utf-8')
        title = unicode(entry['title']['$t']).encode('utf-8')
        thumbnail = unicode(entry['media$group']['media$thumbnail'][1]['url']).encode('utf-8')

        item = ListItem()
        item.add_request_data('userId', userId)
        item.add_request_data('playlistId', playlistId)
        item.set_next_action_name('show_Playlist_Videos')
        xbmcListItem = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail)
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    if(len(items) == maxCount):
        item = ListItem()
        item.add_request_data('userId', userId)
        item.add_request_data('pageNbr', pageNbr + 1)
        item.set_next_action_name('show_Playlists')
        xbmcListItem = xbmcgui.ListItem(label='---- Next Page ---->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    return items
            

def showUserPlaylistVideos(request_obj, response_obj):
    items = None
    if request_obj.get_data().has_key('pageNbr'):
        items = retrieveUserPlaylistVideos(request_obj.get_data()['playlistId'], request_obj.get_data()['pageNbr'])
    else:
        items = retrieveUserPlaylistVideos(request_obj.get_data()['playlistId'])
    response_obj.set_item_list(items)
    

def retrieveUserPlaylistVideos(playlistId, pageNbr=0, maxCount=50):
    url = 'http://gdata.youtube.com/feeds/api/playlists/' + playlistId + '?alt=json&v=2&max-results=' + str(maxCount) + '&start-index=' + str((pageNbr * maxCount) + 1)

    jData = json.loads(HttpUtils.HttpClient().getHtmlContent(url))
    entries = jData['feed']['entry']
    
    items = []
    for entry in entries:
        videoId = entry['media$group']['yt$videoid']['$t']
        title = unicode(entry['title']['$t']).encode('utf-8')
        thumbnail = 'http://i.ytimg.com/vi/' + videoId + '/default.jpg'
        
        item = ListItem()
        item.add_request_data('videoLink', 'http://www.youtube.com/watch?v=' + videoId + '&')
        item.add_request_data('videoTitle', title)
        item.set_next_action_name('play_Video')
        xbmcListItem = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail)
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    if(len(items) == maxCount):
        item = ListItem()
        item.add_request_data('playlistId', playlistId)
        item.add_request_data('pageNbr', pageNbr + 1)
        item.set_next_action_name('show_Playlist_Videos')
        xbmcListItem = xbmcgui.ListItem(label='---- Next Page ---->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
    return items


def selectContentType(request_obj, response_obj):
    d = xbmcgui.Dialog()
    index = d.select('Select Category:', ['Videos', 'Playlists'])
    if index == -1:
        response_obj.set_redirect_action_name('show_Videos')
    elif index == 0:
        response_obj.set_redirect_action_name('show_Videos')
    elif index == 1:
        response_obj.set_redirect_action_name('show_Playlists')
        

def retrieveYouTubeUserInfo(userId):
    url = 'http://gdata.youtube.com/feeds/api/users/' + userId + '?alt=json&v=2'
    jData = json.loads(HttpUtils.HttpClient().getHtmlContent(url))
    entry = jData['entry']
    userInfo = {}
    userInfo['title'] = entry['title']['$t']
    userInfo['thumbnail'] = entry['media$thumbnail']['url']
    return userInfo

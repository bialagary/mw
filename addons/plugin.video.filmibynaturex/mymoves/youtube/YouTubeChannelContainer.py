from TurtleContainer import Container
from common import AddonUtils, XBMCInterfaceUtils
import xbmcgui, xbmc  # @UnresolvedImport
from common.DataObjects import ListItem
import YouTubeBrowser
import urllib2
import sys
import urllib


CHANNELS_JSON_FILE = "YouTubeChannels.json"
PRE_LOADED_CHANNELS = ['SominalTvTheaters', 'SominalTvHindiMusic', 'erosentertainment', 'tseries', 'UTVMotionPictures', 'Saavn', 'yrf', 'YRFsongs', 'yrfTV', 'YRFTrailers', 'YRFMovies', 'RelianceBigCinemas', 'VenusMovies']

def displayChannels(request_obj, response_obj):
    addonContext = Container().getAddonContext()
    item = ListItem()
    item.set_next_action_name('add_Channel')
    youtube_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='Add_New_YouTube_V1.png')
    xbmcListItem = xbmcgui.ListItem(label='Add New Channel', iconImage=youtube_icon_filepath, thumbnailImage=youtube_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)   
                
    filepath = AddonUtils.getCompleteFilePath(baseDirPath=addonContext.addonProfile, extraDirPath=AddonUtils.ADDON_SRC_DATA_FOLDER, filename=CHANNELS_JSON_FILE, makeDirs=True)
    if not AddonUtils.doesFileExist(filepath):
        new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__retrieveYouTubeUserInfo__'), PRE_LOADED_CHANNELS, 'Loading default list of channels...', 'Remove the channel you hate in default list using context menu.')
        index = 0
        channelsJsonObj = {}
        for username in PRE_LOADED_CHANNELS:
            channelsJsonObj[username] = new_items[index]
            index = index + 1
        AddonUtils.saveObjToJsonFile(filepath, channelsJsonObj)

    try:
        channelsJsonObj = AddonUtils.getJsonFileObj(filepath)
        print 'CHANNELS JSON LOADED'
        if len(channelsJsonObj) == 0:
            d = xbmcgui.Dialog()
            if d.yesno('NO channels added yet!', 'Would you like to add YouTube channel right now?', 'Get username from YouTube URL.'):
                isAdded = addNewChannel(request_obj, response_obj)
                if not isAdded:
                    return
                else:
                    channelsJsonObj = AddonUtils.getJsonFileObj(filepath)

        for channelUsername in channelsJsonObj:
            userInfo = channelsJsonObj[channelUsername]
            item = ListItem()
            item.add_request_data('userId', channelUsername)
            item.set_next_action_name('show_Channel')
            xbmcListItem = xbmcgui.ListItem(label=unicode(userInfo['title']).encode("utf-8"), iconImage=userInfo['thumbnail'], thumbnailImage=userInfo['thumbnail'])
            
            contextMenuItems = []
            data = '?actionId=' + urllib.quote_plus("remove_YouTube_Channel") + '&data=' + urllib.quote_plus(AddonUtils.encodeData({"userId":channelUsername}))
            contextMenuItems.append(('Remove channel', 'XBMC.RunPlugin(%s?%s)' % (sys.argv[0], data)))
            xbmcListItem.addContextMenuItems(contextMenuItems, replaceItems=False)
            item.set_xbmc_list_item_obj(xbmcListItem)
            response_obj.addListItem(item)
        
    except:
        raise
        AddonUtils.deleteFile(filepath)
        print 'MY CHANNELS CORRUPT FILE DELETED = ' + filepath
        

def removeChannel(request_obj, response_obj):
    channelName = request_obj.get_data()['userId']
    d = xbmcgui.Dialog()
    if not d.yesno('Remove Channel : [B]' + channelName + '[/B]', 'Do you want to continue?', 'Note: This action will not delete channel from YouTube.'):
        return
    filepath = AddonUtils.getCompleteFilePath(baseDirPath=Container().getAddonContext().addonProfile, extraDirPath=AddonUtils.ADDON_SRC_DATA_FOLDER, filename=CHANNELS_JSON_FILE, makeDirs=True)
    if AddonUtils.doesFileExist(filepath):
        try:
            channelsJsonObj = AddonUtils.getJsonFileObj(filepath)
            try:
                del channelsJsonObj[channelName]
                print 'CHANNEL DELETED = ' + channelName
                AddonUtils.saveObjToJsonFile(filepath, channelsJsonObj)
                d = xbmcgui.Dialog()
                d.ok('Channel removed SUCCESSFULLY', 'You can add this channel again using same way.', 'ENJOY!')
                xbmc.executebuiltin("Container.Refresh()")
            except KeyError:
                d = xbmcgui.Dialog()
                d.ok('FAILED to remove channel', 'Please try again.')
                
        except ValueError:
            AddonUtils.deleteFile(filepath)
            print 'MY CHANNELS CORRUPT FILE DELETED = ' + filepath
    else:
        d = xbmcgui.Dialog()
        d.ok('NO channels added yet', 'Add new channel using YouTube username.', 'Get username from YouTube URL.')


def addNewChannel(request_obj, response_obj):
    keyb = xbmc.Keyboard('', 'Enter [B]YouTube[/B] username')
    keyb.doModal()
    if (keyb.isConfirmed()):
        username = keyb.getText()
        if username == None or username == '':
            d = xbmcgui.Dialog()
            d.ok('Username not entered', 'Please enter the YouTube username correctly.', 'Get username from YouTube URL.')
        else:
            try:
                channelsJsonObj = {}
                filepath = AddonUtils.getCompleteFilePath(baseDirPath=Container().getAddonContext().addonProfile, extraDirPath=AddonUtils.ADDON_SRC_DATA_FOLDER, filename=CHANNELS_JSON_FILE, makeDirs=True)
                if AddonUtils.doesFileExist(filepath):
                    try:
                        channelsJsonObj = AddonUtils.getJsonFileObj(filepath)
                        print 'CHANNELS JSON LOADED'
                    except ValueError:
                        AddonUtils.deleteFile(filepath)
                        print 'CORRUPT FILE DELETED = ' + filepath
                                
                try:
                    if channelsJsonObj[username] != None:
                        d = xbmcgui.Dialog()
                        d.ok('Channel already exists', 'Please enter the YouTube username correctly.', 'Get username from YouTube URL.')
                        
                except KeyError:
                    print 'Search for YouTube username now = ' + username
                        
                userInfo = YouTubeBrowser.retrieveYouTubeUserInfo(username)
                if userInfo != None:
                    channelsJsonObj[username] = userInfo
                    AddonUtils.saveObjToJsonFile(filepath, channelsJsonObj)
                    d = xbmcgui.Dialog()
                    d.ok('Channel added SUCCESSFULLY', 'ENJOY!')
                    xbmc.executebuiltin("Container.Refresh()")
            except urllib2.HTTPError:
                d = xbmcgui.Dialog()
                d.ok('Username doesn\'t exist', 'Please enter the YouTube username correctly.', 'Get username from YouTube URL.')
                
def __retrieveYouTubeUserInfo__(username):
    print username
    return YouTubeBrowser.retrieveYouTubeUserInfo(username)

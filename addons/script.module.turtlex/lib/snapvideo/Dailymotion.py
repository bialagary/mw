'''
Created on Oct 29, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080, VIDEO_QUAL_LOW
import re
import urllib
try:
    import json
except ImportError:
    import simplejson as json

VIDEO_HOSTING_NAME = 'Dailymotion'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://press.dailymotion.com/fr/wp-content/uploads/logo-Dailymotion.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.dailymotion.com/embed/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        HttpUtils.HttpClient().disableCookies()
        
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(html)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(html)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(html)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(html)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(html)
        dm_LD = None
        dm_SD = None
        dm_720 = None
        dm_1080 = None
        
        if matchFullHD:
            dm_1080 = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        if matchHD:
            dm_720 = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        if dm_720 is None and matchHQ:
            dm_720 = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        if matchSD:
            dm_SD = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        if matchLD:
            dm_LD = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        
        if dm_LD is not None:
            video_info.add_video_link(VIDEO_QUAL_LOW, dm_LD, addReferer=True, refererUrl=video_link)
        if dm_SD is not None:
            video_info.add_video_link(VIDEO_QUAL_SD, dm_SD, addReferer=True, refererUrl=video_link)
        if dm_720 is not None:
            video_info.add_video_link(VIDEO_QUAL_HD_720, dm_720, addReferer=True, refererUrl=video_link)
        if dm_1080 is not None:
            video_info.add_video_link(VIDEO_QUAL_HD_1080, dm_1080, addReferer=True, refererUrl=video_link)
        video_info.set_video_stopped(False)
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    html = HttpUtils.HttpClient().getHtmlContent(url='https://api.dailymotion.com/playlist/' + playlistId + '/videos')
    playlistJsonObj = json.loads(html)
    videoItemsList = []
    for video in playlistJsonObj['list']:
        videoItemsList.append('http://www.dailymotion.com/video/' + str(video['id']))
    return videoItemsList


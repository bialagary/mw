'''
Created on Feb 7, 2015

@author: jchirag
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import logging
import re
import urllib

VIDEO_HOST_NAME = 'CloudEC'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.cloudy.ec/img/logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://www.cloudy.ec/embed.php?id=' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        video_key = re.compile('key\: "(.+?)"').findall(html)[0]
        video.set_stopped(False)
        video.set_thumb_image('')
        video.set_name("CloudEC Video")
        video_url = 'http://www.cloudy.ec/api/player.api.php?user=undefined&codes=1&file=' + video_id + '&pass=undefined&key=' + video_key
        html = http.HttpClient().get_html_content(url=video_url)
        video_link = re.compile('url=(.+?)&title=').findall(html)[0]
        video.add_stream_link(STREAM_QUAL_SD, urllib.unquote_plus(video_link))
        logging.getLogger().debug(video.get_streams())
    except:
        video.set_stopped(True)
    return video

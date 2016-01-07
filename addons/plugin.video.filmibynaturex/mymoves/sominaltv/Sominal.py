'''
Created on Jul 8, 2013

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
from TurtleContainer import Container, AddonContext
from common import HttpUtils, Logger, EnkDekoder, XBMCInterfaceUtils, AddonUtils
from common.DataObjects import ListItem
from moves import SnapVideo
from snapvideo import GoogleDocs, Dailymotion, YouTube, VideoPress, PlayCineFlix, \
    STVFlicks, MediaPlayBox
import BeautifulSoup
import re
import requests
import sys
import xbmcgui # @UnresolvedImport
try:
    import json
except ImportError:
    import simplejson as json


PREFERRED_DIRECT_PLAY_ORDER = [MediaPlayBox.VIDEO_HOSTING_NAME, PlayCineFlix.VIDEO_HOSTING_NAME, VideoPress.VIDEO_HOSTING_NAME, STVFlicks.VIDEO_HOSTING_NAME, GoogleDocs.VIDEO_HOSTING_NAME, Dailymotion.VIDEO_HOSTING_NAME, YouTube.VIDEO_HOSTING_NAME]
BASE_WSITE_URL = 'http://www.playindiafilms.com/'
# pageDict = {0:25, 1:50, 2:100}
# TITLES_PER_PAGE = pageDict[int(Container().getAddonContext().addon.getSetting('moviesPerPage'))]



def listMovies(request_obj, response_obj):
    categoryUrlSuffix = request_obj.get_data()['categoryUrlSuffix']
    page = 1
    if request_obj.get_data().has_key('page'):
        page = int(request_obj.get_data()['page'])
    
    titles = retrieveMovies(categoryUrlSuffix, page)
    
    items = []
    for entry in titles:
        titleInfo = entry['title']
        
        if re.compile('Hindi Dubbed').findall(titleInfo) is not None:
            titleInfo = titleInfo.replace('(Hindi Dubbed)', '').replace('Hindi Dubbed', '')
        
        movieInfo = re.compile("(.+?)\((\d+)\) (.*)").findall(titleInfo)
        if(len(movieInfo) == 0):
            movieInfo = re.compile("(.+?)\((\d+)\)").findall(titleInfo)
        if(len(movieInfo) == 0):
            movieInfo = [[titleInfo]]
        title = unicode(movieInfo[0][0].rstrip()).encode('utf-8').replace('&#8211;', '-').replace('&amp;', '&')
        year = ''
        if(len(movieInfo[0]) >= 2):
            year = unicode(movieInfo[0][1]).encode('utf-8')
        quality = ''
        if categoryUrlSuffix != 'BluRay':
            if(len(movieInfo[0]) >= 3):
                quality = unicode(movieInfo[0][2]).encode('utf-8').strip()
                if quality == '*BluRay*' or quality == '*BluRay* (Hindi Dubbed)' or quality == '*BluRay* Hindi Dubbed':
                    quality = '[COLOR red]*HD*[/COLOR]'
                elif quality == 'DVD' or quality == 'DVD (Hindi Dubbed)' or quality == 'DVD Hindi Dubbed':
                    quality = '[COLOR orange]DVD[/COLOR]'
                quality = ' :: ' + quality
                
        movieInfo = entry['content']
        movieLabel = '[B]' + title + '[/B]' + ('(' + year + ')' + quality if (year != '') else '')
        item = ListItem()
        item.add_moving_data('movieTitle', title)
        item.add_moving_data('movieYear', year)
        item.add_request_data('movieInfo', unicode(movieInfo).encode('utf-8'))
        item.add_request_data('movieTitle', title)
        item.set_next_action_name('Movie_Streams')
        xbmcListItem = xbmcgui.ListItem(label=movieLabel, label2='(' + year + ') :: ' + quality)
        item.set_xbmc_list_item_obj(xbmcListItem)
        items.append(item)
        response_obj.addListItem(item)
    
    total_pages = 4
    count = 0
    next_page = page
    if count < total_pages:
        count = count + 1
        next_page = next_page + 1
        item = ListItem()
        item.add_request_data('page', next_page)
        item.add_request_data('categoryUrlSuffix', request_obj.get_data()['categoryUrlSuffix'])
        item.set_next_action_name('Next_Page')
        xbmcListItem = xbmcgui.ListItem(label='  ---- NEXT PAGE #' + str(next_page) + ' --->')
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    
    response_obj.set_xbmc_content_type('movies')
    
'''
Cached function to retrieve HD movies
'''
def retrieveMovies(categoryUrlSuffix, page):
    url = BASE_WSITE_URL + "category/" + categoryUrlSuffix + "/feed"
    if page > 1:
        url = url + "?paged=" + str(page)
    r = requests.get(url)
    html = r.text
    soup = BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.XML_ENTITIES, fromEncoding='utf-8')
    titles = []
    for item in soup.findAll('item'):
        title = {}
        title['title'] = item.findChild('title').getText()
        title['content'] = item.findChild('content:encoded').getText()
        titles.append(title)
    return titles


def retieveTrailerStream(request_obj, response_obj):
    soup = None
    title = request_obj.get_data()['movieTitle']
    if request_obj.get_data().has_key('movieInfo'):
        soup = BeautifulSoup.BeautifulSoup(request_obj.get_data()['movieInfo'])
    elif request_obj.get_data().has_key('moviePageUrl'):
        contentDiv = BeautifulSoup.SoupStrainer('div', {'dir':'ltr'})
        soup = HttpUtils.HttpClient().getBeautifulSoup(url=request_obj.get_data()['moviePageUrl'], parseOnlyThese=contentDiv)
    if soup is None:
        return
    videoLink = None
    Logger.logDebug(soup.prettify())
    frameTag = soup.findChild('iframe', recursive=True)
    if frameTag is not None:
        videoLink = frameTag['src']
    else:
        paramTag = soup.findChild('param', attrs={'name':'movie'}, recursive=True)
        if paramTag is not None:
            videoLink = paramTag['value']
        else:
            videoLink = soup.findChild('embed', recursive=True)['src']
    request_obj.set_data({'videoLink': videoLink, 'videoTitle':title})


def retieveMovieStreams(request_obj, response_obj):
    if(request_obj.get_data().has_key('videoInfo')):
        title = request_obj.get_data()['videoInfo']['title']
        Container().ga_client.reportContentUsage('movie', title)
    soup = None
    if request_obj.get_data().has_key('movieInfo'):
        soup = BeautifulSoup.BeautifulSoup(request_obj.get_data()['movieInfo'])
    elif request_obj.get_data().has_key('moviePageUrl'):
        soup = HttpUtils.HttpClient().getBeautifulSoup(url=request_obj.get_data()['moviePageUrl'])
    if soup is None:
        return
    videoSources = []
    videoSourceLinks = None
    tags = soup.findAll('p')
    if len(tags) < 5:
        tags.extend(soup.findAll('span'))
    Logger.logDebug(soup.prettify())
    Logger.logDebug('   -------------------------------------------------------       ')
    for tag in tags:
        Logger.logDebug(tag)
        if re.search('^(Source|ONLINE|Server)', tag.getText(), re.IGNORECASE):
            if videoSourceLinks is not None and len(videoSourceLinks) > 0:
                videoSources.append(videoSourceLinks)
            videoSourceLinks = []
        else:
            aTags = tag.findAll('a', attrs={'href':re.compile('(desiflicks.com|desionlinetheater.com|wp.me|cine.sominaltvfilms.com|media.thesominaltv.com|mediaplaybox.com)')}, recursive=True)
            if aTags is None or len(aTags) != 1:
                continue
            aTag = aTags[0]
            if aTag is not None:
                infoLink = str(aTag['href']).replace('http://adf.ly/377117/', '')
                if videoSourceLinks == None:
                    videoSourceLinks = []
                if infoLink not in videoSourceLinks:
                    videoSourceLinks.append(infoLink)
    if videoSourceLinks is not None and len(videoSourceLinks) > 0:
        videoSources.append(videoSourceLinks)
    new_items = []
    sourceCount = 0
    for videoSource in videoSources:
        sourceCount = sourceCount + 1
        new_items.extend(__prepareVideoSourceLinks__(videoSource, str(sourceCount)))
    
    if(request_obj.get_data().has_key('videoInfo')):
        __addVideoInfo__(new_items, request_obj.get_data()['videoInfo'])
    response_obj.set_item_list(new_items)
    
    playNowItem = __findPlayNowStream__(response_obj.get_item_list())
    if playNowItem is not None:
        request_obj.set_data({'videoPlayListItems': playNowItem.get_request_data()['videoPlayListItems']})
    
    
def __addVideoInfo__(video_items, videoInfo):
    for video_item in video_items:
        video_item.add_request_data('videoInfo', videoInfo)
    
    
def __findPlayNowStream__(new_items):
    if Container().getAddonContext().addon.getSetting('autoplayback') == 'false':
        return None
    selectedIndex = None
    selectedSource = None
    for item in new_items:
        if item.get_moving_data().has_key('isContinuousPlayItem') and item.get_moving_data()['isContinuousPlayItem']:
            try:
                preference = PREFERRED_DIRECT_PLAY_ORDER.index(item.get_moving_data()['videoSourceName'])
                if preference == 0:
                    selectedSource = item
                    selectedIndex = 0
                    break
                elif selectedIndex is None or selectedIndex > preference:
                    selectedSource = item
                    selectedIndex = preference
            except ValueError:
                continue
    return selectedSource
    
    
def __preparePlayListItem__(video_items, source):
    video_playlist_items = []
    video_source_img = None
    video_source_name = None
    for item in video_items:
        video_item = {}
        video_item['videoLink'] = item.get_request_data()['videoLink']
        video_item['videoTitle'] = item.get_request_data()['videoTitle']
        video_playlist_items.append(video_item)
        video_source_img = item.get_moving_data()['videoSourceImg']
        video_source_name = item.get_moving_data()['videoSourceName']
    Logger.logDebug('IMAGE :: ')
    Logger.logDebug(video_source_img)
    Logger.logDebug(type(video_source_img))
    item = ListItem()
    item.add_request_data('videoPlayListItems', video_playlist_items)
    item.add_moving_data('isContinuousPlayItem', True)
    item.add_moving_data('videoSourceName', video_source_name)
    item.set_next_action_name('Play_AllStreams')
    xbmcListItem = xbmcgui.ListItem(label='[COLOR blue]' + AddonUtils.getBoldString('Continuous Play') + '[/COLOR]' + ' | ' + 'Source #' + source + ' | ' + 'Parts = ' + str(len(video_playlist_items)) , iconImage=video_source_img, thumbnailImage=video_source_img)
    item.set_xbmc_list_item_obj(xbmcListItem)
    return item
    
    
def __prepareVideoSourceLinks__(videoSourceLinks, source):
    new_items = XBMCInterfaceUtils.callBackDialogProgressBar(getattr(sys.modules[__name__], '__prepareVideoLink__'), videoSourceLinks, 'Retrieving streaming links for source #' + source, 'Failed to retrieve stream information, please try again later')
    if len(new_items) == 0:
        XBMCInterfaceUtils.displayDialogMessage('No video items found!', 'Unable to resolve video items from source #' + source, 'Continuing with next source...')
        return []
    
    count = 0
    for item in new_items:
        xbmcItem = item.get_xbmc_list_item_obj()
        count = count + 1
        xbmcItem.setLabel('Source #' + source + ' | ' + xbmcItem.getLabel() + str(count))
    new_items.append(__preparePlayListItem__(new_items, source))
    return new_items
    
    
def __prepareVideoLink__(videoSourceLink):
    new_items = []
    url = videoSourceLink
    if re.search('wp.me', url, re.I):
        url = HttpUtils.getRedirectedUrl(url)
    if not url.startswith('http://'):
        url = 'http://' + url
    Logger.logDebug(url)
#     contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'left_articles'})
#     soup = BeautifulSoup.BeautifulSoup(html, contentDiv)

    if re.search('', videoSourceLink):
        video_hosting_info = SnapVideo.findVideoHostingInfo(videoSourceLink)
        if video_hosting_info is None:
            Logger.logDebug('Unrecognized video_url = ' + videoSourceLink)
        else:
            video_source_img = video_hosting_info.get_video_hosting_image()
            
            new_item = ListItem()
            new_item.add_request_data('videoTitle', 'Part #')
            new_item.add_request_data('videoLink', videoSourceLink)
            new_item.add_moving_data('videoSourceImg', video_source_img)
            new_item.add_moving_data('videoSourceName', video_hosting_info.get_video_hosting_name())
            new_item.set_next_action_name('Play_Stream')
            xbmcListItem = xbmcgui.ListItem(label='Part #', iconImage=video_source_img, thumbnailImage=video_source_img)
            new_item.set_xbmc_list_item_obj(xbmcListItem)
            new_items.append(new_item)
            return new_items
    
    html = HttpUtils.HttpClient().getHtmlContent(url)
    dek = EnkDekoder.dekode(html)
    Logger.logDebug(dek)
    if dek is not None:
        html = dek
        
    html = html.replace('\n\r', '').replace('\r', '').replace('\n', '').replace('\\', '')
    children = []
    if re.search('http://videos.stvflicks.com/', html):
        docId = re.compile('http://videos.stvflicks.com/(.+?).mp4"').findall(html)[0]
        children.append('src="http://videos.stvflicks.com/' + docId + '.mp4"')
    elif re.search('http://playcineflix.com/', html):
        docId = re.compile('http://playcineflix.com/(.+?).mp4"').findall(html)[0]
        children.append('src="http://playcineflix.com/' + docId + '.mp4"')
    elif re.search('https://video.google.com/get_player', html):
        docId = re.compile('docid=(.+?)"').findall(html)[0]
        children.append('src="https://docs.google.com/file/d/' + docId + '/preview"')
    elif re.search('http://videos.videopress.com/', html):
        docId = re.compile('type="video/mp4" href="http://videos.videopress.com/(.+?).mp4"').findall(html)[0]
        children.append('src="http://videos.videopress.com/' + docId + '.mp4"')
    elif re.search('http://videos.videopress.com/', html):
        docId = re.compile('type="video/mp4" href="http://videos.videopress.com/(.+?).mp4"').findall(html)[0]
        children.append('src="http://videos.videopress.com/' + docId + '.mp4"')
    elif re.search('video_alt_url=http://www.mediaplaybox.com', html):
        docId = re.compile('video_alt_url=http://www.mediaplaybox.com(.+?).mp4').findall(html)[0]
        children.append('src="http://www.mediaplaybox.com:81/' + docId + '.mp4"')
    elif re.search('video_url=http://www.mediaplaybox.com', html):
        docId = re.compile('video_url=http://www.mediaplaybox.com(.+?).mp4').findall(html)[0]
        children.append('src="http://www.mediaplaybox.com:81/' + docId + '.mp4"')
    else:
        children = re.compile('<embed(.+?)>').findall(html)
        if children is None or len(children) == 0:
            children = re.compile('<iframe(.+?)>').findall(html)
    
            
    Logger.logDebug(children)
    for child in children:
        video_url = re.compile('src="(.+?)"').findall(child)[0]
        if(re.search('http://ads', video_url, re.I) or re.search('http://ax-d', video_url, re.I)):
            continue
        if video_url.startswith('http://goo.gl/'):
            Logger.logDebug('Found google short URL = ' + video_url)
            video_url = HttpUtils.getRedirectedUrl(video_url)
            Logger.logDebug('After finding out redirected URL = ' + video_url)
            if re.search('videos.desionlinetheater.com', video_url):
                XBMCInterfaceUtils.displayDialogMessage('Unable to parse', 'A new HTML Guardian is used to protect the page', 'Sounds technical!! hmm, it means cannot find video.', 'Fix: Find me JavaScript Interpreter online service')
        video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
        if video_hosting_info is None:
            Logger.logDebug('Unrecognized video_url = ' + video_url)
            continue
        video_source_img = video_hosting_info.get_video_hosting_image()
        
        new_item = ListItem()
        new_item.add_request_data('videoTitle', 'Part #')
        new_item.add_request_data('videoLink', video_url)
        new_item.add_moving_data('videoSourceImg', video_source_img)
        new_item.add_moving_data('videoSourceName', video_hosting_info.get_video_hosting_name())
        new_item.set_next_action_name('Play_Stream')
        xbmcListItem = xbmcgui.ListItem(label='Part #', iconImage=video_source_img, thumbnailImage=video_source_img)
        new_item.set_xbmc_list_item_obj(xbmcListItem)
        new_items.append(new_item)
    
    return new_items



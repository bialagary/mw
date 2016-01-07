#!/usr/bin/python
#encoding: utf-8

import urllib, urllib2, sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from datetime import datetime, timedelta
import calendar, time
import CommonFunctions
common = CommonFunctions

__addon__ = xbmcaddon.Addon('plugin.video.nbanhlstreams')
__addonname__ = __addon__.getAddonInfo('name')


NBAURL = 'http://www.nbastream.net/'
NHLURL = 'http://www.nhlstream.net/'


def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def GetURL(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0')
    try:
    	response = urllib2.urlopen(request)
    	html = response.read()
    	return html
    except Exception:
    	xbmcgui.Dialog().ok(__addonname__, 'Looks like www.nbastreams.net and www.nhlstream.net are down... Please try later...')
    	sys.exit()


def GetStreams():
	
	html = GetURL(NBAURL)
	block_content = common.parseDOM(html, "div", attrs={"id": "featured"})[0]
	days = common.parseDOM(block_content, "h3",  attrs={"align": "left"})
	today = datetime.utcnow() - timedelta(hours=8)
	today_str = str(today.strftime('%A, %B %d, %Y'))
	matching = [s for s in days if today_str in s]
	tit = ''
	if len(matching)>0:
		block_content = block_content.split(today_str)[1]
		ind = days.index(matching[0])
		if len(days)>1 and ind+1<len(days):
			block_content = block_content.split(days[ind+1])[0]
	else:
		for i, day in enumerate(days):
			game_day = datetime(*(time.strptime(day, '%A, %B %d, %Y')[0:6]))+timedelta(hours=5)
			if game_day>today:
				block_content = block_content.split(day)[1]
				today_str = day
				if i+1<len(days):
					next = days[i+1]
					block_content = block_content.split(next)[0]
				break
			else:
				if i==len(days)-1:
					tit = '[COLOR=FFFF0000]Games start date might be wrong!!![/COLOR]'
				else: continue
	titles = common.parseDOM(block_content, "a", ret="title")
	links = common.parseDOM(block_content, "a",  ret="href")
	times = common.parseDOM(block_content, "strong")
	del times[1::2]
	del titles[1::2]
	del links[1::2]
	addDir('[COLOR=FF00FF00]======= NBA GAMES =======[/COLOR]'+tit, '', iconImg='', mode='')
	for i, title in enumerate(titles):
		game_time = today_str+' '+times[i]+'PM'
		utc_game_time = datetime(*(time.strptime(game_time, '%A, %B %d, %Y %I:%M%p')[0:6]))+timedelta(hours=5)
		game_time = utc_to_local(utc_game_time)
		link = links[i]
		link  = link.split('title')[0]
		link = link.replace('"','')
		link = NBAURL+link
		title = title.split('style')[0]
		title = title.replace('"','')
		title = title.replace('Live Stream','')
		addDir(title+'- '+game_time.strftime(xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S','')), link, iconImg='', mode="PLAYNBA")
	html = GetURL(NHLURL)
	block_content = common.parseDOM(html, "div", attrs={"id": "featured"})[0]
	days = common.parseDOM(block_content, "h3",  attrs={"align": "left"})
	today = datetime.utcnow() - timedelta(hours=8)
	today_str = str(today.strftime('%A, %B %d, %Y'))
	matching = [s for s in days if today_str in s]
	tit = ''
	if len(matching)>0:
		block_content = block_content.split(today_str)[1]
		ind = days.index(matching[0])
		if len(days)>1 and ind+1<len(days):
			block_content = block_content.split(days[ind+1])[0]
	else:
		for i, day in enumerate(days):
			game_day = datetime(*(time.strptime(day, '%A, %B %d, %Y')[0:6]))+timedelta(hours=5)
			if game_day>today:
				block_content = block_content.split(day)[1]
				today_str = day
				if i+1<len(days):
					next = days[i+1]
					block_content = block_content.split(next)[0]
				break
			else:
				if i==len(days)-1:
					tit = '[COLOR=FFFF0000]Games start date might be wrong!!![/COLOR]'
				else: continue
	titles = common.parseDOM(block_content, "a", ret="title")
	links = common.parseDOM(block_content, "a",  ret="href")
	times = common.parseDOM(block_content, "strong")
	del times[1::2]
	del titles[1::2]
	del links[1::2]
	addDir('[COLOR=FF00FF00]======= NHL GAMES =======[/COLOR]'+tit, '', iconImg='', mode='')
	for i, title in enumerate(titles):
		game_time = today_str+' '+times[i]+'PM'
		utc_game_time = datetime(*(time.strptime(game_time, '%A, %B %d, %Y %I:%M%p')[0:6]))+timedelta(hours=5)
		game_time = utc_to_local(utc_game_time)
		link = links[i]
		link  = link.split('title')[0]
		link = link.replace('"','')
		link = NHLURL+link
		title = title.split('style')[0]
		title = title.replace('"','')
		title = title.replace('Live Stream','')
		addDir(title+'- '+game_time.strftime(xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S','')), link, iconImg='', mode="PLAYNHL")

def PlayNBA(url):
    tit = xbmc.getInfoLabel('ListItem.Title')
    html = GetURL(url)
    link = common.parseDOM(html, "iframe",  ret="src")[0]
    html  = GetURL(NBAURL+link)
    link = common.parseDOM(html, "iframe",  ret="src")
    if len(link)>0:
    	link = link[0]
    else:
    	xbmc.executebuiltin('Notification(NBA and NHL Live HD Streams,Stream not found. Please check later.,3000)')
    	sys.exit()
    channel = link.split('/')[3]
    link = 'https://streamup.global.ssl.fastly.net/app/'+channel+'s-stream/playlist.m3u8'
    addLink('Play stream', {'Title': tit}, link)
    
def PlayNHL(url):
    tit = xbmc.getInfoLabel('ListItem.Title')
    html = GetURL(url)
    link = common.parseDOM(html, "iframe",  ret="src")[0]
    html  = GetURL(NHLURL+link)
    link = common.parseDOM(html, "iframe",  ret="src")
    if len(link)>0:
    	link = link[0]
    else:
    	xbmc.executebuiltin('Notification(NBA and NHL Live HD Streams,Stream not found. Please check later.,3000)')
    	sys.exit()
    channel = link.split('/')[3]
    link = 'https://streamup.global.ssl.fastly.net/app/'+channel+'s-stream/playlist.m3u8'
    addLink('Play stream', {'Title': tit}, link)

    	
def addDir(title, url, iconImg="DefaultVideo.png", mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=True)


def addLink(title, infoLabels, url, iconImg="DefaultVideo.png"):
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels=infoLabels)
    xbmcplugin.addDirectoryItem(handle=h, url=url, listitem=item)
    
    
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param


h = int(sys.argv[1])
params = get_params()

mode = None
url = None

try: mode = urllib.unquote_plus(params['mode'])
except: pass

try: url = urllib.unquote_plus(params['url'])
except: pass

if mode == None: GetStreams()
elif mode == 'PLAYNBA': PlayNBA(url)
elif mode == 'PLAYNHL': PlayNHL(url)

xbmcplugin.endOfDirectory(h)
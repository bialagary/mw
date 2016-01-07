import sys
import urllib
import urllib2
import urlparse
import json
import re
import xbmcgui
import xbmcplugin
import xbmcaddon
import os
import urlresolver

from resources.lib.common_addon import Addon
from resources.lib import gdrive
from resources.lib import cloudyvideos

addon_id = 'plugin.video.footballhighlightssubreddit'
addon = Addon(addon_id, sys.argv)
icon = addon.queries.get('icon', '')
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
my_addon = xbmcaddon.Addon(addon_id)
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
fanart = my_addon.getAddonInfo('fanart')
 
xbmcplugin.setContent(addon_handle, 'movies')
data=None
mode = args.get('mode', None)

CVRef = 'http://reddit.com/footballhighlights'
CVUA = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0'
CVHeader = {
 'Referer': CVRef,
 'User-Agent': CVUA,
}
__settings__ = xbmcaddon.Addon(id='plugin.video.footballhighlightssubreddit')
max_video_quality = __settings__.getSetting('max_video_quality')
qual = [360, 480, 720, 1080]
max_video_quality = qual[int(max_video_quality)]
DASH = __settings__.getSetting('DASH')
saved_searches = __settings__.getSetting('saved_searches_1') + ','\
	+ __settings__.getSetting('saved_searches_2') + ','\
	+ __settings__.getSetting('saved_searches_3')
saved_searches = [s.strip() for s in saved_searches.split(',')]
saved_searches = [s for s in saved_searches if s != '']
if saved_searches == []:
	saved_searches = None
subreddit_base_url = 'http://www.reddit.com/r/footballhighlights/.json?after='

re_video = re.compile(r'<a href="(?:(https?://(?:www.)?(?:docs|drive).google.com/file/d/[\w-]+/(?:preview|edit))[^#]*?|'
									'https?://(?:www.)?dailymotion.com/video/([\w-]+).*?|'
								   '(https?://(?:www.)?youtube.com/watch\?v=[\w-]+).*?|'
								   '(https?://(?:www.)?cloudyvideos.com/[\w-]+).*?)">(.*?)</a>')

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def log(message):
	xbmc.log('plugin.video.footballhighlightssubreddit: %s' % message)

def allvideos():
	json_data = get_reddit_json('http://www.reddit.com/r/footballhighlights/.json')
	display_posts(json_data, 'true', subreddit_base_url)

def docs():
        url = 'https://www.googleapis.com/youtube/v3/search?q=soccer+documentary&regionCode=US&part=snippet&hl=en_US&key=AIzaSyA7v1QOHz8Q4my5J8uGSpr0zRrntRjnMmk&type=video&maxResults=50'
        link = open_url(url)
        link = link.replace('\r','').replace('\n','').replace('  ','')
        match=re.compile('"videoId": "(.+?)".+?"title": "(.+?)"',re.DOTALL).findall(link)
        for ytid,name in match:
                if len(name) > 5:
                        url = 'https://www.youtube.com/watch?v='+ytid
                        icon = 'http://img.youtube.com/vi/'+ytid+'/0.jpg'
                        addLink(name,url,6,icon,fanart)


def playlink(url,name):
        xbmc.Player ().play(urlresolver.HostedMediaFile(url).resolve())
	
def cats():
        if saved_searches:
		for s in saved_searches:
			url = build_url({'mode': 'saved_search', 'query': s})
                        icon = art+s+'.png'
			li = xbmcgui.ListItem(s, iconImage=icon)
			li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	xbmc.executebuiltin('Container.SetViewMode(50)')
        
def news():
        link = open_url('http://www.footballwebpages.co.uk/news.xml')
        match = re.compile("<description>(.+?)</description>.+?<published>(.+?)</published>",re.DOTALL).findall(link)
        print match
        for desc,pub in match:
              if '<title>'not in desc:
                      desc = cleanHex(desc)
                      addDir(desc + pub,'url','mode',icon,fanart)
                        
def getrss(url):
        link = open_url(url)
        match = re.compile("<title>(.+?)</title>.+?<description>(.+?)</description>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for title,desc,pub in match:
                desc = desc.replace('<![CDATA[','').replace(']]>','').replace('&#8217;','')
                title = desc.replace('<![CDATA[','').replace(']]>','')
                pub = pub.replace('BST','')
                pub = '[B][COLOR limegreen]'+pub+'[/COLOR][/B]'
                status = pub + ' - ' + desc
                addLink(status,'url','mode','iconimage',fanart)
                      
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

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

def get_reddit_json(url, raw=0):
	header = {'User-Agent' : 'XBMC plugin for /r/footballhighlights'}
	req = urllib2.Request(url, None, header)
	try:
		response = urllib2.urlopen(req)
	except urllib2.URLError as e:
		if hasattr(e, 'reason'):
			log('URLError, %s' % str(e.reason))
			xbmc.executebuiltin('Notification(URLError, Could not reach server)')
		elif hasattr(e, 'code'):
			log('HTTPError, %s' % str(e.code))
			xbmc.executebuiltin('Notification(HTTPError, %s)' % str(e.code))
	else:
		response_data = response.read()
		if not raw:
			response_data = json.loads(response_data)
		return response_data

def display_posts(json_data, to_filter, reddit_base_url):
	if json_data:	
		for p in json_data['data']['children']:
			post_title = p['data']['title'].encode('utf8', 'replace')
			post_url = urllib2.quote(p['data']['url'].encode('utf-8'), ':/')
			if to_filter == 'true':
				log(str(post_url))
				comments_contents = get_reddit_json(post_url, 1)

				video_found = re_video.search(comments_contents)
				
				if video_found:
					url = build_url({'mode': 'folder', 'foldername': post_title, 'comments_contents': comments_contents})
					li = xbmcgui.ListItem(post_title, iconImage='icon')
					li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
					xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
			else:
				url = build_url({'mode': 'folder', 'foldername': post_title, 'post_url': post_url})
				li = xbmcgui.ListItem(post_title, iconImage='icon')
				li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		after_post = json_data['data']['after']
		url = build_url({'mode': 'next_page', 'after_post': after_post, 'to_filter': to_filter, 'reddit_base_url': reddit_base_url})
		li = xbmcgui.ListItem('>> Next Page >>', iconImage='icon')
		li.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
		xbmc.executebuiltin('Container.SetViewMode(50)')
		xbmcplugin.endOfDirectory(addon_handle)

def upcoming(url):
        link = open_url(url)
        match = re.compile("<match>(.+?)</match>",re.DOTALL).findall(link)
        for data in match:
           if not '<status>Full Time</status>' in data:
                matches = re.compile("<date>(.+?)</date>.+?<time>(.+?)</time>.+?<homeTeamName>(.+?)</homeTeamName>.+?<awayTeamName>(.+?)</awayTeamName>",re.DOTALL).findall(data)
                for dte,tme,home,away in matches:
                        
                        string = dte + ' ' + tme + ' ' + home+ ' v ' +  away+ ' '
                        string=string.replace(':00 ',' ')
                        addLink(string,'url','mode','iconimage',fanart)
def results(url):
        link = open_url(url)
        match = re.compile("<match>(.+?)</match>",re.DOTALL).findall(link)
        for data in match:
           if '<status>Full Time</status>' in data:
                matches = re.compile("<date>(.+?)</date>.+?<time>(.+?)</time>.+?<homeTeamName>(.+?)</homeTeamName>.+?<homeTeamScore>(.+?)</homeTeamScore>.+?<awayTeamScore>(.+?)</awayTeamScore>.+?<awayTeamName>(.+?)</awayTeamName>",re.DOTALL).findall(data)
                for dte,tme,home,hscore,ascore,away in matches:
                        string = dte + ' ' + tme + ' ' + home+ ' (' + hscore + ' - ' + ascore + ') ' + away
                        string=string.replace(':00 ',' ')
                        addLink(string,'url','mode','iconimage',fanart)
        
def leagues(url):
        if 'coming' in url:
                mode = 7
        else:
                mode = 8
        addDir('Barclays Premier League','http://www.footballwebpages.co.uk/matches.xml?comp=1',mode,'iconimage',fanart)
	addDir('FA Cup','http://www.footballwebpages.co.uk/matches.xml?comp=21',mode,'url',fanart)
	addDir('UEFA Champions League','http://www.footballwebpages.co.uk/matches.xml?comp=24',mode,'iconimage',fanart)
	addDir('Europa League','http://www.footballwebpages.co.uk/matches.xml?comp=25',mode,'url',fanart)
	addDir('Sky Bet Championship','http://www.footballwebpages.co.uk/matches.xml?comp=2',mode,'iconimage',fanart)
	addDir('Sky Bet League One','http://www.footballwebpages.co.uk/matches.xml?comp=3',mode,'url',fanart)
	addDir('Sky Bet League Two','http://www.footballwebpages.co.uk/matches.xml?comp=4',mode,'iconimage',fanart)
	addDir('Capital One Cup','http://www.footballwebpages.co.uk/matches.xml?comp=22',mode,'url',fanart)
	addDir('Johnstones Paint Trophy','http://www.footballwebpages.co.uk/matches.xml?comp=28',mode,'iconimage',fanart)
	addDir('Scottish Premiership','http://www.footballwebpages.co.uk/matches.xml?comp=17',mode,'url',fanart)
	addDir('Scottish Championship','http://www.footballwebpages.co.uk/matches.xml?comp=18',mode,'iconimage',fanart)
	addDir('Scottish League One','http://www.footballwebpages.co.uk/matches.xml?comp=19',mode,'url',fanart)
	addDir('Scottish League Two','http://www.footballwebpages.co.uk/matches.xml?comp=20',mode,'iconimage',fanart)
	addDir('Scottish FA Cup','http://www.footballwebpages.co.uk/matches.xml?comp=23',mode,'url',fanart)
	addDir('Scottish Communities Cup','http://www.footballwebpages.co.uk/matches.xml?comp=32',mode,'iconimage',fanart)
	addDir('Petrofac Training Cup','http://www.footballwebpages.co.uk/matches.xml?comp=33',mode,'url',fanart)

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

if mode is None:
        addDir('All Videos','url',1,'iconimage',fanart)
	addDir('Videos by Category','url',2,'iconimage',fanart)
	addDir('Football Latest News','url',3,'iconimage',fanart)
	addDir('Football Documentaries','url',5,'iconimage',fanart)
	addDir('Football Upcoming Fixtures','upcoming',9,'iconimage',fanart)
	addDir('Football Results','resu;ts',9,'url',fanart)



elif mode[0] == 'saved_search':
	query = urllib.quote(args['query'][0])
	query_base_url = 'http://www.reddit.com/search/.json?q=' + query + '+subreddit%3Afootballhighlights&sort=new&t=all&limit=10&after='
	query_json_data = get_reddit_json(query_base_url)
	display_posts(query_json_data, 'false', query_base_url)
 
elif mode[0] == 'folder':
	try:
		comments_contents = args['comments_contents'][0]
	except:
		post_url = args['post_url'][0]
		comments_contents = get_reddit_json(post_url, 1)
	video_list = re.findall(re_video, comments_contents)
	for v in video_list:
		title = re.sub(r'<.*?>', '', v[4])
		if v[0]:
			id = v[0]
			print id
			try:
				url = gdrive.get_quality_video_link(max_video_quality, id, DASH)
			except:
				title = '[COLOR red]GD Unavailable[/COLOR]: ' + title
				url = ''
		elif v[1]:
			id = v[1]
			print id
			try:
				url = urlresolver.HostedMediaFile(id).resolve()
			except:
				title = '[COLOR red]DM Unavailable[/COLOR]: ' + title
				url = ''
		elif v[2]:
			id = v[2]
			print id
			try:
				url = urlresolver.HostedMediaFile(id).resolve()
			except:
				title = '[COLOR red]YT Unavailable[/COLOR]: ' + title
				url = ''
		elif v[3]:
			id = v[3]
			print id
			if '/embed-' in id:
				continue
			try:
				url = cloudyvideos.get_quality_video_link(id,None,CVHeader) + '|User-Agent=%s&Referer=%s' % (CVUA,CVRef)

			except:
				title = '[COLOR red]Unavailable[/COLOR]: ' + title
				url = ''
		else:
			continue
		li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
		li.setProperty('IsPlayable', 'true')
		if url is None:
			url = ''
		log(url)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'next_page':
	after_post = args['after_post'][0]
	to_filter = args['to_filter'][0]
	reddit_base_url = args['reddit_base_url'][0]
	json_data = get_reddit_json(reddit_base_url + after_post)
	display_posts(json_data, to_filter, reddit_base_url)
	

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)


if mode==1:allvideos()
elif mode==2:cats()
elif mode==3:news()
elif mode==4:getrss(url)
elif mode==5:docs()
elif mode==6:playlink(url,name)
elif mode==7:upcoming(url)
elif mode==8:results(url)
elif mode==9:leagues(url)

       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

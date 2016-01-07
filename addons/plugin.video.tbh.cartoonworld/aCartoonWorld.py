### ############################################################################################################
###	#	
### # Site: 				#		Cartoon World - http://www.cartoon-world.tv/
### # Author: 			#		The Highway
### # Description: 	#		
### # Credits: 			#		Originally ported from the addon project known as Cartoon World - by the-one.
###	#	
### ############################################################################################################
### ############################################################################################################
### Imports ###
import urllib,urllib2,re,cookielib,os,sys,re
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
#from resources.libs import main
from common import *
from common import (_addon,addon,_plugin,net,_artIcon,_artFanart,spAfterSplit,spBeforeSplit,set_view,addst,tfalse)
selfAddon=_plugin
#from universal import watchhistory
#wh=watchhistory.WatchHistory(ps('_addon_id'))
### ############################################################################################################
### ############################################################################################################
SiteName='[COLOR cornflowerblue]Cartoon [COLOR orange]World[/COLOR][/COLOR]  [v0.1.7]  [Cartoons]'
SiteTag='cartoon-world.tv'
mainSite='http://www.cartoon-world.tv/'
iconSite='http://i.imgur.com/z2ZOc0T.png' #'http://i.imgur.com/Xa6TdPD.png' #_artIcon
fanartSite=_artFanart #'http://i.imgur.com/BGBQeKJ.png' #'http://i.imgur.com/aUl3frq.png' #'http://i.imgur.com/wfHtoI3.png' #_artFanart
colors={'0':'white','1':'red','2':'blue','3':'green','4':'yellow','5':'orange','6':'lime','7':'','8':'cornflowerblue','9':'blueviolet','10':'hotpink','11':'pink','12':'tan'}

CR='[CR]'
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
### ############################################################################################################
site=addpr('site','')
section=addpr('section','')
url=addpr('url','')
sections={'series':'series','movies':'movies'}
thumbnail=addpr('img','')
fanart=addpr('fanart','')
page=addpr('page','')
### ############################################################################################################
### ############################################################################################################
def About(head=''+cFL(SiteName,'blueviolet')+'',m=''):
	m=''
	if len(m)==0:
		# m+='IRC Chat:  '+cFL('#XBMCHUB','blueviolet')+' @ '+cFL('irc.Freenode.net','blueviolet')
		m+=CR+'Site Name:  '+SiteName+CR+'Site Tag:  '+SiteTag+CR+'Site Domain:  '+mainSite+CR+'Site Icon:  '+iconSite+CR+'Site Fanart:  '+fanartSite
		m+=CR+'Age:  Please make sure you are of a valid age to watch the material shown.'
		m+=CR+CR+'Known Hosts for Videos:  '
		m+=CR+'VidCrazy.net | UploadCrazy.net'
		m+=CR+CR+'Features:  '
		m+=CR+'* Browse Latest Episodes.'
		m+=CR+'* Uses urlResolver().'
		m+=CR+'* Play Videos via Handled Hosts.'
		m+=CR+'* Browse Ongoing Anime and Cartoons.'
		m+=CR+'* Browse Lists:  Anime | Cartoon | Movie'
		m+=CR+'* Browse Episodes'
		m+=CR+'* Search Features:  Search | Repeat Last Search | Browse Search Results'
		m+=CR+CR+'Notes:  '
		m+=CR+'* Originally ported from the-one\'s plugin.video.cartoonworld.'
		m+=CR+'* This Project has been given a major overhaul and been reworked to work with my own project\'s functions and methods.'
		m+=CR+'* Videos might have to be clicked more than once to get them to play.  It\'s a bit touchy.'
		m+=CR+'* If you want to read the plot description for a show, just click on the show and then check the plot description on any episode.  It\'s possible for there to be quite a longer number of results at times so I\'m not going to parse each and every page.  I want a quick display of results.'
		#m+=CR+'* '
		m+=''
		m+=''
		m+=CR+''
		# m+=CR+ps('ReferalMsg')
		m+=CR+''
		m+=CR+''
		m+=CR+''
	String2TextBox(message=cFL(m,'cornflowerblue'),HeaderMessage=head)
	#RefreshList()

### ############################################################################################################
### ############################################################################################################
def spAfterSplit(t,ss):
	if ss in t: t=t.split(ss)[1]
	return t
def spBeforeSplit(t,ss):
	if ss in t: t=t.split(ss)[0]
	return t
def escape(text):
	try:
		rep={" ": "%20"}
		for s, r in rep.items(): text = text.replace(s, r)
	except TypeError: pass
	return text
def unescape(text):
	try:
		rep={"&nbsp;": " ","\n": "","\t": "", }
		for s, r in rep.items(): text = text.replace(s, r)
		# remove html comments
		text = re.sub(r"<!--.+?-->", "", text)
	except TypeError: pass
	return text
### ############################################################################################################
### ############################################################################################################

def VidPlay(mname,murl,thumb):
	myNote('Please Wait!','Opening Stream',3000); stream_url=False; link=nURL(murl)
	if link:
		link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
		match=re.compile('<script type="text/javascript">\s*id="(.+?)";\s*ew="(.+?)";\s*eh="(.+?)";\s*</script>').findall(link)
		debob(match)
		for fid,wid,hei in match: pageUrl='http://castalba.tv/embed.php?cid='+fid+'&wh='+wid+'&ht='+hei; debob(pageUrl)
		link2=nURL(pageUrl)
		rtmp=re.compile("'streamer\':\s*\'(.+?)\',").findall(link2)
		swfUrl=re.compile('flashplayer\':\s*"(.+?)"').findall(link2)
		playPath=re.compile("'file\':\s*\'(.+?)\',\r\n\r\n\t\t\t\'streamer\'").findall(link2)
		stream_url=rtmp[0]+' playpath='+playPath[0]+' swfUrl='+swfUrl[0]+' live=true timeout=15 swfVfy=true pageUrl='+pageUrl
		debob(stream_url)
		PlayItCustom(url=murl,stream_url=stream_url,img=thumb,title=mname)

def Browse_Hosts(url, title, img):
	url_content=nolines(unescape(_addon.unescape(nURL(url)))); 
	try: videoop_content=re.compile('<ul class="videoop">\s*<li class="active-vid">(.+?)</ul').findall(url_content.replace('</ul>','</ul\n\r>'))[0]
	except: videoop_content=''
	debob(['videoop_content',videoop_content])
	try: video_hosts=re.compile('<li(?: class="active-vid")?><a href="(\D+://.+?)">\s*(.+?)(?: Video)?\s*</a></li').findall(videoop_content.replace('</li>','</li\n\r>'))
	except: video_hosts=[]
	for (vh_url,vh_name) in video_hosts:
		if vh_url.startswith('http://www.cartoon-world.tv/'):
			debob([vh_name,vh_url])
			if '"' in vh_url: vh_url=vh_url.split('"')[0]
			if (vh_url==url) or (vh_url+'/'==url) or (vh_url==url+'/'): pass; debob(['first page'])
			else:
				url_content+=nolines(unescape(_addon.unescape(nURL(vh_url)))); debob(['loaded new page',vh_url])
	if re.search(r'<div id="vid', url_content):
				#for vid in re.finditer(r'<div id="vid([0-9]{1,2})"(.+?)</div>', url_content):
				for vid in re.finditer(r'<div (?:id="video" )?class="([^"]*)" itemprop="video"[^>]+>(.+?)</div>', url_content):
					#vid_part=str(int(vid.group(1)) + 1); 
					vid_lnks=vid.group(2)
					debob(vid_lnks)
					#for vid_lnk in re.finditer(r'<h5.+?>(.+?)</h5><iframe.+?src="(.+?)"', vid_lnks):
					for vid_lnk in re.finditer(r'<iframe.+?src="(\D+://(?:www\.)?([^/]+)/[^"]+)"', vid_lnks):
						#vid_lnk_ttl=title+' - video-'+vid_part+' - '+vid_lnk.group(1); vid_lnk_url=vid_lnk.group(2)
						#vid_lnk_ttl=title+' - video-'+vid_part+' - '+vid_lnk.group(2); vid_lnk_url=vid_lnk.group(1)
						
						vid_lnk_ttl=title+' - '+vid_lnk.group(2); 
						vid_lnk_url=vid_lnk.group(1)
						
						debob(vid_lnk_ttl); debob(vid_lnk_url)
						contextLabs={'title':addpr('title',''),'year':'0000','url':url,'img':img,'fanart':img,'hostname':title,'hostdomain':title}; contextMenuItems=ContextMenu_Hosts(labs=contextLabs)
						#addon.add_directory({'mode' : 'play', 'title' : vid_lnk_ttl, 'img' : img, 'url' : vid_lnk_url}, {'title':  vid_lnk_ttl}, img= img)
						try: _addon.add_directory({'mode':'PlayFromHost','site':site,'section':section,'title':vid_lnk_ttl,'url':vid_lnk_url,'fanart':img,'img':img},{'title':cFL_(vid_lnk_ttl,colors['6'])},is_folder=False,fanart=img,img=img,contextmenu_items=contextMenuItems)
						except: t=''
	else:
				for vid_lnk in re.finditer(r'<h5.+?>(.+?)</h5>(?:<img .+?><noscript>)?<iframe.+?src="(.+?)"', url_content):
					vid_lnk_ttl=title+' - '+vid_lnk.group(1); vid_lnk_url=vid_lnk.group(2)
					debob(['*host found',vid_lnk_ttl,vid_lnk_url])
					contextLabs={'title':addpr('title',''),'year':'0000','url':url,'img':img,'fanart':img,'hostname':title,'hostdomain':title}; contextMenuItems=ContextMenu_Hosts(labs=contextLabs)
					#addon.add_directory({'mode' : 'play', 'title' : vid_lnk_ttl, 'img' : img, 'url' : vid_lnk_url}, {'title':  vid_lnk_ttl}, img= img)
					try: _addon.add_directory({'mode':'PlayFromHost','site':site,'section':section,'title':vid_lnk_ttl,'url':vid_lnk_url,'fanart':img,'img':img},{'title':cFL_(vid_lnk_ttl,colors['6'])},is_folder=False,fanart=img,img=img,contextmenu_items=contextMenuItems)
					except: t=''
	set_view('list',view_mode=addst('default-view')); eod()

def Browse_Episodes(url,page=''):
	html=nURL(url); html=messupText(html,True,True); htmlA=''+html
	html=spAfterSplit(html,'<div class="clearboth"></div>'); 
	html=spAfterSplit(html,'<ul'); 
	html=spBeforeSplit(html,'</ul>'); 
	try: _simg=re.compile('<div class=".*?-row">\s*\n*\s*<img.*?src="(.+?)".*?>\s*\n*\s*<table class=".*?-table">').findall(htmlA)[0]
	except: _simg=thumbnail
	try: _plot=re.compile('</tbody>\s*\n*\s*</table>\s*\n*\s*\n*\s*(.*?)\s*\n*\s*</div>\s*\n*\s*<div class="clearboth"></div>\s*\n*\s*<div class="ani-eps">').findall(htmlA)[0]
	except: _plot=''
	try: _type=re.compile('<tr><td.*?>Type</td><td.*?>\s*(.*?)\s*</td></tr>').findall(htmlA)[0]
	except: _type=''
	try: _year=re.compile('<tr><td.*?>Aired</td><td.*?>\s*(.*?)\s*</td></tr>').findall(htmlA)[0]
	except: _year=''
	try: _stitle=re.compile('<tr><td.*?>Title</td><td.*?>\s*(.*?)\s*</td></tr>').findall(htmlA)[0]
	except: _stitle=''
	debob([_stitle,_year,_type,_plot,_simg])
	s='<li.*?><a.*?href="(http://www.cartoon-world.tv/(.+?)/)".*?><i.*?></i>\s*(.+?)\s*</a></li>'
	matches=re.compile(s).findall(html); ItemCount=len(matches)
	if ItemCount==0: return
	if '/anime' in url.lower(): color_z=colors['8']
	elif '/cartoon' in url.lower(): color_z=colors['5']
	elif '/movie' in url.lower(): color_z=colors['1']
	else: color_z=colors['0']
	for _url,_folder,_name in matches:
		fimg=_simg; img=_simg #fimg=fanart; img=thumbnail
		
		_title=cFL_(''+_name+'',color_z)
		contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg}; contextMenuItems=ContextMenu_Episodes(contextLabs)
		labs={'title':_title,'plot':cFL('Year:  ',colors['11'])+cFL(_year,colors['10'])+cFL('    |    ','black')+cFL('Type:  ',colors['11'])+cFL(_type,colors['10'])+CR+cFL(_plot,colors['12']),'year':_year,'type':_type,'showtitle':_stitle,'fanart':fimg,'img':img}
		try: _addon.add_directory({'mode':'Hosts','site':site,'section':section,'title':_name,'url':_url,'fanart':fimg,'img':img},labs,is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
		except: t=''
	set_view('episodes',view_mode=addst('episode-view')); eod()
	#

def Browse_LatestEpisodes(mmurl):
	url_content=nolines(nURL(mainSite)).replace('</li>','</li\n\r>'); 
	#les=re.search(r"(?s)<h\d>Latest Episodes</h\d>(.+?)<h\d", url_content).group(1); 
	les=url_content.split('>Latest Episodes</h')[-1].split('</ul>')[0] #.split('>Site News</h')[0]
	les=_addon.unescape(les); les=unescape(les)
	# from universal import _common
	# les=_common.str_conv(les)
	les = les.encode('ascii', 'ignore')
	deb('Length of html',str(len(les))); 
	s='<li class="(.*?)">\s*<a href="(.+?)">\s*<span class=".*?rib">.*?</span>\s*'; 
	s+='(?:<noscript>\s*)?<img .*?src="(.+?)".*?/>\s*(?:</noscript>\s*)?'; 
	s+='<div class="ftitle">\s*(.+?)\s*</div>\s*</a>\s*</li'
	#<li class="Anime"><a href="http://www.cartoon-world.tv/future-card-buddyfight-episode-49/"><span class="Animerib">Anime</span> 
	#<img width="210" height="90" src="data:image/gif;base64,R0lGODdhAQABAPAAAP///wAAACwAAAAAAQABAEACAkQBADs=" data-lazy-type="image" data-lazy-src="http://www.cartoon-world.tv/static/future-card-buddyfight-episode-49-210x90.jpg" class="lazy lazy-hidden latest-ep wp-post-image" alt="Future Card Buddyfight Episode 49" /><noscript><img width="210" height="90" src="http://www.cartoon-world.tv/static/future-card-buddyfight-episode-49-210x90.jpg" class="latest-ep wp-post-image" alt="Future Card Buddyfight Episode 49" /></noscript><div class="ftitle">Future Card Buddyfight Episode 49</div></a></li>
	leS=re.compile(s).findall(les)
	#print les
	#for le in re.finditer(r'<li .*?class="(.+?)".*?>\s*<a .*?href="(.+?)".*?>\s*(?:<span>\s*\D*\s*</span>\s*)?<img.+? src="(.+?)".*?>\s*<div class=".*?">\s*(.+?)\s*</div></a></li', les):
	#print leS
	for (le_typ,le_url,le_img,le_ttl) in leS:
		#print le
		#le_typ=le.group(1); le_url=le.group(2); le_img=le.group(3); le_ttl=le.group(4)
		contextLabs={'title':le_ttl,'year':'0000','url':le_url,'img':le_img,'fanart':le_img,'DateAdded':'','type':le_typ}; contextMenuItems=ContextMenu_Episodes(labs=contextLabs)
		try: _addon.add_directory({'mode':'Hosts','site':site,'section':section,'title':le_ttl,'url':le_url,'fanart':le_img,'img':le_img},{'title':cFL_(le_ttl,colors['6'])},is_folder=True,fanart=le_img,img=le_img,contextmenu_items=contextMenuItems)
		except: t=''
	set_view('episodes',int(addst('episode-view'))); eod()

def Browse_Ongoing():
	html=nURL(mainSite); html=messupText(html,True,True); html=spAfterSplit(html,'>Ongoing Anime and Cartoons</h'); html=spAfterSplit(html,'<div class="ani-popbox">'); html=spAfterSplit(html,'<ul class="nav nav-list">'); html=spBeforeSplit(html,'</div>'); html=spBeforeSplit(html,'</ul>')
	html=nolines(html).replace('</li>','</li\n\r>'); deb('Length of html',str(len(html))); 
	#print html; 
	#s='<li><a href="(http://www.cartoon-world.tv/watch/(.+?)/)">\s*<i class="icon-chevron-right"></i>\s*(.+?)\s*<span class="text-\D+">\s*(\D+)\s*</span></a></li'
	s='<li><a href="(http://www.cartoon-world.tv/watch/(.+?)/)">\s*<i class="icon-chevron-right"></i>\s*(.+?)\s*<span class="text-(?:Anime|Cartoon)?">((?:Anime|Cartoon)?)<'
	matches=re.compile(s).findall(html); ItemCount=len(matches); deb('Number of Matches Found',str(ItemCount)); 
	#print matches; 
	color_c=colors['5']; color_a=colors['8']
	if ItemCount==0: return
	for _url,_folder,_name,_type in matches:
		fimg='http://www.dubbednetwork.net/static/'+_folder+'.jpg'
		img='http://www.dubbednetwork.net/static/'+_folder+'.jpg'
		fimg='%simages/%s.jpg'%(mainSite,_folder)
		img='%simages/%s.jpg'%(mainSite,_folder)
		if 'anime' in _type.lower(): color_z=color_a
		else: color_z=color_c
		_title=cFL_(''+_name+'  '+cFL('['+_type+']',color_z),color_z)
		pars={'mode':'Episodes','site':site,'section':section,'title':_name,'url':_url,'fanart':fimg,'img':img}
		contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section,'plot':''}; contextMenuItems=ContextMenu_Series(contextLabs)
		try: _addon.add_directory(pars,{'title':_title},is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
		except: t=''
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()
	#

def Browse_List(url):
	html=nURL(url); html=messupText(html,True,True); 
	html=spAfterSplit(html,'<div class="ani-post">'); 
	html=spAfterSplit(html,'<div id="ddmcc_container">'); 
	html=spAfterSplit(html,'<div class="ddmcc">'); 
	html=spBeforeSplit(html,'</div>'); 
	#s='<li.*?><a href="(http://www.cartoon-world.tv/watch/(.+?)/)"><i class="icon-\D*-\D*"></i>\s*(.+?)\s*</a></li>'
	s='<li.*?><a.*?href="(http://www.cartoon-world.tv/watch/(.+?)/)".*?><i.*?></i>\s*(.+?)\s*</a></li>'
	matches=re.compile(s).findall(html); ItemCount=len(matches)
	if ItemCount==0: return
	if '/anime' in url.lower(): color_z=colors['8']
	elif '/cartoon' in url.lower(): color_z=colors['5']
	elif '/movie' in url.lower(): color_z=colors['1']
	else: color_z=colors['0']
	for _url,_folder,_name in matches:
		#fimg='http://www.dubbednetwork.net/static/'+_folder+'.jpg'
		#img='http://www.dubbednetwork.net/static/'+_folder+'.jpg'
		fimg='%simages/%s.jpg'%(mainSite,_folder)
		img='%simages/%s.jpg'%(mainSite,_folder)
		_title=cFL_(''+_name+'',color_z)
		pars={'mode':'Episodes','site':site,'section':section,'title':_name,'url':_url,'fanart':fimg,'img':img}
		contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section,'plot':''}; 
		if 'movie' in url.lower(): contextMenuItems=ContextMenu_Movies(contextLabs)
		else: contextMenuItems=ContextMenu_Series(contextLabs)
		try: _addon.add_directory(pars,{'title':_title},is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
		except: t=''
	set_view('tvshows',view_mode=addst('tvshows-view')); eod()
	#

def Browse_Search(html,metamethod=''):
	#html=nURL(url); 
	html=messupText(html,True,True); 
	#s='<li.*?><a href="(http://www.cartoon-world.tv/watch/(.+?)/)"><i class="icon-\D*-\D*"></i>\s*(.+?)\s*</a></li>'
	s='<a.*?href="(http://www.cartoon-world.tv/(.+?))".*?>\s*\n*\s*<div id="image-spot">\s*\n*\s*\n*\s*<img src=".*?(http://.+?\.[jpg|png].*?)".*?>\s*\n*\s*\n*\s*</div>\s*\n*\s<div id="series-box">\s*\n*\s<div class="series-info-box">\s*\n*\s<div class="main-title">\s*\n*\s(.*?)\s*\n*\s</div>\s*\n*\s<div class=".*?">\s*\n*\s(.*?)\s*\n*\s</div>\s*\n*\s<span class=".*?">\s*\n*\s(.*?)\s*\n*\s</div>\s*\n*\s</div>\s*\n*\s</a>'
	s='<a href="(http://www.cartoon-world.tv/watch/(.+?)/)" class="box-link"><div id="image-spot">\s*\n*\s*\n*\s*<img src=".*?(http://.+?\.jpg).*?".*?></div><div id="series-box"><div class="series-info-box"><div class="main-title">\s*(.+?)\s*</div><div.*?>\s*(.*?)\s*</div><span.*?>\s*(.*?)\s*</div></div></a>'
	s='<li class="list-group-item"><a href="(http://www.cartoon-world.tv/watch/(.+?)/)">\s*([^<]+)</a'
	matches=re.compile(s).findall(html); ItemCount=len(matches); deb('# of items found',str(ItemCount))
	if ItemCount==0: return
	#for _url,_folder,_img,_name,_type,_status in matches:
	for _url,_folder,_name in matches:
		_img='%simages/%s.jpg'%(mainSite,_folder)
		_type=''
		_status=''
		
		if 'anime' in _type.lower(): color_z=colors['8']
		elif 'cartoon' in _type.lower(): color_z=colors['5']
		elif 'movie' in _type.lower(): color_z=colors['1']
		else: color_z=colors['0']
		fimg=_img; img=_img
		if len(_type) > 0: _title=cFL_(''+_name+'  '+cFL('['+_type+']',color_z),color_z)
		else: _title=cFL_(''+_name+'',color_z)
		
		pars={'mode':'Episodes','site':site,'section':section,'title':_name,'url':_url,'fanart':fimg,'img':img}
		contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'todoparams':_addon.build_plugin_url(pars),'site':site,'section':section,'plot':''}; 
		if ('movie' in _type.lower()) or ('movie'==_type.lower()) or (color_z==colors['0']): contextMenuItems=ContextMenu_Movies(contextLabs)
		else: contextMenuItems=ContextMenu_Series(contextLabs)
		try: _addon.add_directory(pars,{'title':_title},is_folder=True,fanart=fimg,img=img,contextmenu_items=contextMenuItems,total_items=ItemCount)
		except: t=''
	#set_view('tvshows',view_mode=addst('tvshows-view')); #eod()

def Search_Site(title='',url='',page='',metamethod='',endit=True):
	#if url=='': url=mainSite+'wp-content/themes/blackv2/anime_search.php?q='
	if url=='': url=mainSite+'?s='
	if not '?' in url: url+='?s='
	#if len(page) > 0: page='1'
	deb('url',url)
	if (title==''): title=showkeyboard(txtMessage=title,txtHeader="Search:  ("+site+")")
	if (title=='') or (title=='none') or (title==None) or (title==False): return
	deb('Searching for',title)
	_title=''+title
	title=title.replace(' ','+')
	##if len(page) > 0: p='/'+page; npage=str(int(page)+1)
	##else: p=''; npage='2'
	deb('url search',url+title)
	html=nURL(url+title)
	#html=nURL(url,method='post',form_data={'search':title,'page':page},headers={'Referer':mainSite})
	if (len(html)==0): myNote('Search:  '+title,'No page found.'); return
	##if '">Next</a></li>' in html: _addon.add_directory({'mode':'Page','site':site,'section':section,'url':url,'page':npage},{'title':cFL_('  .Next Page > '+npage,colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	addstv('LastSearchTitle'+SiteTag,_title) ## Save Setting ##
	
	
	Browse_Search(html,metamethod)
	if endit==True: set_view('tvshows',view_mode=addst('tvshows-view')); eod()

def Fav_List(site='',section='',subfav=''):
	debob(['test1',site,section,subfav])
	favs=fav__COMMON__list_fetcher(site=site,section=section,subfav=subfav)
	ItemCount=len(favs)
	debob('test2 - '+str(ItemCount))
	if len(favs)==0: myNote('Favorites','None Found'); eod(); return
	debob(favs)
	for (_name,_year,_img,_fanart,_Country,_Url,_plot,_Genres,_site,_subfav,_section,_ToDoParams,_commonID,_commonID2) in favs:
		if _img > 0: img=_img
		else: img=iconSite
		if _fanart > 0: fimg=_fanart
		else: fimg=fanartSite
		debob('_ToDoParams'); debob(_ToDoParams)
		pars=_addon.parse_query(_ToDoParams)
		debob('pars'); debob(pars)
		_title=cFL_(_name,'white')
		if (len(_year) > 0) and (not _year=='0000'): _title+=cFL('  ('+cFL(_year,'deeppink')+')','pink')
		if len(_Country) > 0: _title+=cFL('  ['+cFL(_Country,'deeppink')+']','pink')
		
		contextLabs={'title':_name,'year':_year,'img':_img,'fanart':_fanart,'country':_Country,'url':_Url,'plot':_plot,'genres':_Genres,'site':_site,'subfav':_subfav,'section':_section,'todoparams':_ToDoParams,'commonid':_commonID,'commonid2':_commonID2}
		##contextLabs={'title':_name,'year':'0000','url':_url,'img':img,'fanart':fimg,'DateAdded':'','todoparams':_addon.build_plugin_url(pars),'site':site,'section':section}
		contextMenuItems=ContextMenu_Favorites(contextLabs)
		#contextMenuItems=[]
		_addon.add_directory(pars,{'title':_title,'plot':_plot},is_folder=True,fanart=fimg,img=img,total_items=ItemCount,contextmenu_items=contextMenuItems)
		#
	#
	if 'movie' in section.lower(): content='movies'
	else: content='tvshows'
	set_view(content,view_mode=int(addst('tvshows-view'))); eod()

### ############################################################################################################
### ############################################################################################################
def SubMenu(): #(site,section=''):
	if section=='movies':
		scolor=colors['1']
		_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/movie-list/','site':site,'section':section},{'title':cFL_('Movie List',colors['1'])},is_folder=True,fanart='http://i.imgur.com/FMFwKVA.jpg',img='http://i.imgur.com/yOybwxS.png') #'http://i.imgur.com/MIzYiow.jpg'
		### Favorites
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.movies.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		### Advanced Users - used to clean-up Favorites folders.
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'' },{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'2'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'3'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'4'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'5'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'6'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'7'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.movies.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
	if section=='series':
		scolor=colors['2']
		_addon.add_directory({'mode':'BrowseLatestEpisodes','site':site,'section':section,'title':'latest'},{'title':cFL_('Latest Episodes',colors['6'])},is_folder=True,fanart='http://i.imgur.com/SlHh50W.jpg',img='http://i.imgur.com/hpAspdq.png') #http://i.imgur.com/ucfTrbM.jpg
		_addon.add_directory({'mode':'BrowseOngoing','site':site,'section':section,'title':'onging'},{'title':cFL_('Ongoing Anime and Cartoons',colors['6'])},is_folder=True,fanart='http://i.imgur.com/2HTKZ8L.jpg',img='http://i.imgur.com/4VQrSlK.png') #http://i.imgur.com/CDPVR4n.jpg
		_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/anime-list/','site':site,'section':section},{'title':cFL_('Anime List',colors['8'])},is_folder=True,fanart='http://i.imgur.com/m7yy4uc.jpg',img='http://i.imgur.com/t9v4ipl.png') #http://i.imgur.com/VsCJqxt.jpg
		_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/cartoon-list/','site':site,'section':section},{'title':cFL_('Cartoon List',colors['5'])},is_folder=True,fanart='http://i.imgur.com/DrAaCF3.jpg',img='http://i.imgur.com/nyNg4pW.png') #http://i.imgur.com/KIt5eDj.jpg
		### Favorites
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section             },{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'2'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'3'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'4'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'5'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'6'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		_addon.add_directory({'mode':'FavoritesList','site':site,'section':section,'subfav':'7'},{'title':cFL_(ps('WhatRFavsCalled')+addst('fav.tv.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		### Advanced Users - used to clean-up Favorites folders.
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'' },{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.1.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'2'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.2.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'3'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.3.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'4'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.4.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'5'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.5.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'6'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.6.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
		#_addon.add_directory({'mode':'cFavoritesEmpty','site':site,'section':section,'subfav':'7'},{'title':cFL_('Clear '+ps('WhatRFavsCalled')+addst('fav.tv.7.name'),ps('cFL_color3'))},fanart=fanartSite,img=iconSite)
	set_view('list',view_mode=addst('default-view')); eod()
	#



def SectionMenu(): #(site):
	iLL='BrowseList'; fS=fanartSite; iS=iconSite
	_addon.add_directory({'mode':'SubMenu','site':site,'section':'movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img='http://i.imgur.com/yOybwxS.png')
	_addon.add_directory({'mode':'SubMenu','site':site,'section':'series'},{'title':cFL_('Anime Series',colors['2'])},is_folder=True,fanart=fanartSite,img='http://i.imgur.com/t9v4ipl.png')
	#
	#_addon.add_directory({'mode':'BrowseLatestEpisodes','site':site,'section':section,'title':'latest'},{'title':cFL_('Latest Episodes',colors['6'])},is_folder=True,fanart='http://i.imgur.com/SlHh50W.jpg',img='http://i.imgur.com/ucfTrbM.jpg')
	#_addon.add_directory({'mode':'BrowseOngoing','site':site,'section':section,'title':'onging'},{'title':cFL_('Ongoing Anime and Cartoons',colors['6'])},is_folder=True,fanart='http://i.imgur.com/2HTKZ8L.jpg',img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/anime-list/','site':site,'section':section},{'title':cFL_('Anime List',colors['8'])},is_folder=True,fanart='http://i.imgur.com/m7yy4uc.jpg',img='http://i.imgur.com/VsCJqxt.jpg')
	#_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/cartoon-list/','site':site,'section':section},{'title':cFL_('Cartoon List',colors['5'])},is_folder=True,fanart='http://i.imgur.com/DrAaCF3.jpg',img='http://i.imgur.com/KIt5eDj.jpg')
	#_addon.add_directory({'mode':'Listings','url':'http://www.cartoon-world.tv/movie-list/','site':site,'section':section},{'title':cFL_('Movie List',colors['1'])},is_folder=True,fanart='http://i.imgur.com/FMFwKVA.jpg',img='http://i.imgur.com/MIzYiow.jpg')
	#
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	#_addon.add_directory({'mode':'Listings','url':'','site':site,'section':section},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img='http://i.imgur.com/CDPVR4n.jpg')
	# http://i.imgur.com/MIzYiow.jpg
	# http://i.imgur.com/Sq85RrU.jpg
	# http://i.imgur.com/ucfTrbM.jpg
	# http://i.imgur.com/CDPVR4n.jpg
	# http://i.imgur.com/2yKtwBk.jpg
	# http://i.imgur.com/1m2OScV.jpg *
	
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':''},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img=iS)
	#_addon.add_directory({'mode':iLL,'site':site,sC1:sC2,'title':''},{'title':cFL_('',colors['6'])},is_folder=True,fanart=fS,img=iS)
	
	#_addon.add_directory({'mode':'SubMenu','site':site,'section':'movies'},{'title':cFL_('Anime Movies',colors['1'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'SubMenu','site':site,'section':'series'},{'title':cFL_('Anime Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'ongoing-anime'},{'title':cFL_('Ongoing Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Page','site':site,'section':'series','url':mainSite+'new-anime'},{'title':cFL_('New Series',colors['2'])},is_folder=True,fanart=fanartSite,img=iconSite)
	#_addon.add_directory({'mode':'Episodes','site':site,'section':'series','url':mainSite+'surprise'},{'title':cFL_('Suprise Me',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'Search','site':site},{'title':cFL_('Search',colors['0'])},is_folder=True,fanart='http://i.imgur.com/7cgXesz.jpg',img='http://i.imgur.com/4o80H98.png') #'http://i.imgur.com/Sq85RrU.jpg'
	if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart='http://i.imgur.com/FMFwKVA.jpg',img='http://i.imgur.com/oSNRZ7V.png') #'http://i.imgur.com/2yKtwBk.jpg'
	###if (len(addst('LastSearchTitle'+SiteTag)) > 0): _addon.add_directory({'mode':'SearchLast','site':site,'endit':'false'},{'title':cFL_('Repeat Last Search',colors['0'])},is_folder=True,fanart=fanartSite,img=iconSite)
	_addon.add_directory({'mode':'About','site':site},{'title':cFL_('About',colors['9'])},is_folder=False,fanart=fanartSite,img='http://i.imgur.com/0h78x5V.png') # iconSite
	#
	set_view('list',view_mode=addst('default-view')); eod()


### ############################################################################################################
### ############################################################################################################
def mode_subcheck(mode='',site='',section='',url=''):
	debob([mode,site,section,url]); 
	#if (mode=='SectionMenu'): 		SectionMenu() #(site)
	deb('mode',mode); 
	if (mode=='SectionMenu'): 		SectionMenu()
	elif (mode=='') or (mode=='main') or (mode=='MainMenu'): SectionMenu()
	elif (mode=='SubMenu'): 			SubMenu()
	elif (mode=='VidPlay'): 			VidPlay(addpr('title',''),url,thumbnail)
	elif (mode=='Hosts'): 				Browse_Hosts(url,addpr('title',''),thumbnail)
	#
	elif (mode=='BrowseLatestEpisodes'): 		Browse_LatestEpisodes(addpr('title',''))
	elif (mode=='BrowseOngoing'): 		Browse_Ongoing()
	elif (mode=='Listings'): 			Browse_List(url)
	#
	elif (mode=='Page'): 					Browse_Page(url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	elif (mode=='Episodes'): 			Browse_Episodes(url,page)
	elif (mode=='AZ'): 						Browse_AZ()
	elif (mode=='Genres'): 				Browse_Genres()
	elif (mode=='PlayFromHost'): 	PlayFromHost(url)
	elif (mode=='Search'): 				Search_Site(title=addpr('title',''),url=url,page=page,metamethod=addpr('metamethod','')) #(site,section)
	### \/ Testing \/
	#elif (mode=='SearchLast'): 		
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	#	Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=True) #(site,section)
	elif (mode=='SearchLast'): 		Search_Site(title=addst('LastSearchTitle'+SiteTag),url=url,page=page,metamethod=addpr('metamethod',''),endit=tfalse(addpr('endit','true'))) #(site,section)
	elif (mode=='About'): 				About()
	elif (mode=='FavoritesList'): Fav_List(site=site,section=section,subfav=addpr('subfav',''))
	#else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
	##
	elif (mode=='PlayURL'): 						PlayURL(url)
	elif (mode=='PlayURLs'): 						PlayURLs(url)
	elif (mode=='PlayURLstrm'): 				PlayURLstrm(url)
	elif (mode=='PlayFromHost'): 				PlayFromHost(url)
	elif (mode=='PlayVideo'): 					PlayVideo(url)
	elif (mode=='PlayItCustom'): 				PlayItCustom(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='PlayItCustomL2A'): 		PlayItCustomL2A(url,addpr('streamurl',''),addpr('img',''),addpr('title',''))
	elif (mode=='Settings'): 						_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='ResolverSettings'): 		import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='ResolverUpdateHostFiles'):	import urlresolver; urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='TextBoxFile'): 				TextBox2().load_file(url,addpr('title','')); #eod()
	elif (mode=='TextBoxUrl'):  				TextBox2().load_url(url,addpr('title','')); #eod()
	elif (mode=='Download'): 						
		try: _addon.resolve_url(url)
		except: pass
		debob([url,addpr('destfile',''),addpr('destpath',''),str(tfalse(addpr('useResolver','true')))])
		DownloadThis(url,addpr('destfile',''),addpr('destpath',''),tfalse(addpr('useResolver','true')))
	elif (mode=='toJDownloader'): 			SendTo_JDownloader(url,tfalse(addpr('useResolver','true')))
	elif (mode=='cFavoritesEmpty'):  	fav__COMMON__empty( site=site,section=section,subfav=addpr('subfav','') ); xbmc.executebuiltin("XBMC.Container.Refresh"); 
	elif (mode=='cFavoritesRemove'):  fav__COMMON__remove( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year','') )
	elif (mode=='cFavoritesAdd'):  		fav__COMMON__add( site=site,section=section,subfav=addpr('subfav',''),name=addpr('title',''),year=addpr('year',''),img=addpr('img',''),fanart=addpr('fanart',''),plot=addpr('plot',''),commonID=addpr('commonID',''),commonID2=addpr('commonID2',''),ToDoParams=addpr('todoparams',''),Country=addpr('country',''),Genres=addpr('genres',''),Url=url ) #,=addpr('',''),=addpr('','')
	elif (mode=='AddVisit'):							
		try: visited_add(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='RemoveVisit'):							
		try: visited_remove(addpr('title')); RefreshList(); 
		except: pass
	elif (mode=='EmptyVisit'):						
		try: visited_empty(); RefreshList(); 
		except: pass
	elif (mode=='refresh_meta'):			refresh_meta(addpr('video_type',''),TagAnimeName(addpr('title','')),addpr('imdb_id',''),addpr('alt_id',''),addpr('year',''))
	else: myNote(header='Site:  "'+site+'"',msg=mode+' (mode) not found.'); import mMain
	#

mode_subcheck(addpr('mode',''),addpr('site',''),addpr('section',''),addpr('url',''))
### ############################################################################################################
### ############################################################################################################

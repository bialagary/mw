#2Movies - Blazetamer

#import requests
#from bs4 import BeautifulSoup
from tm_libs import dom_parser

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
from resources.modules import status
import downloader
import extract
import time,re
import datetime
import shutil
from resources.modules import tvshow
from metahandler import metahandlers
from resources.modules import main
from resources.utils import autoupdate

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.twomovies'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.twomovies')



from t0mm0.common.net import Net

net = Net()
newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
net.set_user_agent(newagent)


#PATHS
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))

settings = xbmcaddon.Addon(id='plugin.video.twomovies')
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
domain = settings.getSetting('tmovies_domain')
base_url = 'http://www.'+domain+''
#========================DLStuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
header_dict = addon.queries.get('header_dict', '')
totalItems = addon.queries.get('totalItems', '')
debug = 'false'
if debug == 'true':
		print 'Mode is: ' + mode
		print 'Url is: ' + url
		print 'Name is: ' + name
		print 'Thumb is: ' + thumb
		print 'Extension is: ' + ext
		print 'Filetype is: ' + console
		print 'DL Folder is: ' + dlfoldername
		print 'Favtype is: ' + favtype
		print 'Main Image is: ' + mainimg
		print 'Header_Dicts are ' + header_dict
		print 'Logged In Status is ' +loggedin
#================DL END==================================
#########################Blazetamer's Log Module Params########################################
#artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','cookies/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')
#Username and Password Setup############
username = settings.getSetting('tmovies_user')
password = settings.getSetting('tmovies_pass')
form_data = {'login':username, 'password':password,'remember_me':'on','submit_login':'Login', 'submit_login':''}

#END PARAMS##############################

#==========NEW AUTOUPDATE FUNCTION START===============
#********************AutoUpdate******************
from autoupdate import autoupdates
#Author Info Variable

autoupdates.provider_name = "Blazetamer"

#add-on variables

autoupdates.addon_id_name ='plugin.video.twomovies'
autoupdates.addon_xml_loca = "https://offshoregit.com/Blazetamer/repo/raw/master/plugin.video.twomovies/addon.xml"
autoupdates.addon_name ="2 Movies Evolved"
autoupdates.addon_zip_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/plugin.video.twomovies"


#repo variables

autoupdates.repo_name = "repository.BlazeRepo"
autoupdates.repo_xml_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo/addon.xml"
autoupdates.repo_zip_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo"
autoupdates.repo_entry_version="3.0"


#********************AutoUpdate END******************


def LogNotify(title,message,times,icon):
		xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def OPEN_URL(url):
		req=urllib2.Request(url)

		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
		req.add_header('Content-Type','application/x-www-form-urlencoded')
		req.add_header('Host',domain)
		req.add_header('Referer','')
		req.add_header('Connection','keep-alive')
		req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

def OPEN_CHECK(url):
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link





def COOKIELOADER(url):
		#Get UPDATED COOKIE AND STORE
		#Create an opener to open pages using the http protocol and to process cookies.
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		request = urllib2.Request('http://'+domain+'/go_login')
		#print 'Request method before data:', request.get_method()

		request.add_data(urllib.urlencode(form_data))
		#print 'Request method after data :', request.get_method()


		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
		request.add_header('Content-Type','application/x-www-form-urlencoded')
		request.add_header('Host',domain)
		request.add_header('Referer','http://www.'+domain+'/login')
		request.add_header('Connection','keep-alive')
		request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')


		urllib2.urlopen(request).read()
		response = urllib2.urlopen(request)
		cj.save(cookie_file, ignore_discard=True)
		response.close()



		#LOAD UPDATED COOKIE AND GET NEW URL
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		request = urllib2.Request(url)
		request.add_data(urllib.urlencode(form_data))

		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
		request.add_header('Content-Type','application/x-www-form-urlencoded')
		request.add_header('Host',domain)
		request.add_header('Referer','')
		request.add_header('Connection','keep-alive')
		request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		link = urllib2.urlopen(request).read()
		print ' RETURNING COOKED DATA'

		return link

#NEW LOGIN #######
def LOGIN():
	#Create an opener to open pages using the http protocol and to process cookies.
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	request = urllib2.Request('http://'+domain+'/go_login')
	#print 'Request method before data:', request.get_method()

	request.add_data(urllib.urlencode(form_data))
	#print 'Request method after data :', request.get_method()
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
	request.add_header('Content-Type','application/x-www-form-urlencoded')
	request.add_header('Host',domain)
	request.add_header('Referer','http://www.'+domain+'/login')
	request.add_header('Connection','keep-alive')
	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	urllib2.urlopen(request).read()
	response = urllib2.urlopen(request)
	cj.save(cookie_file, ignore_discard=True)
	response.close()
	#Start Log Check
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	request = urllib2.Request('http://'+domain+'/login')
	request.add_data(urllib.urlencode(form_data))

	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
	request.add_header('Content-Type','application/x-www-form-urlencoded')
	request.add_header('Host',domain)
	request.add_header('Referer','http://www.'+domain+'/login')
	request.add_header('Connection','keep-alive')
	request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	print

	newdata = urllib2.urlopen(request).read()
	match=re.compile('href="http://'+domain+'/playlist/(.+?)/watch_list/">').findall(newdata)
	if len(match) > 0:
		if len(match) > 0:
			if username in match :
				print 'YOU ARE LOGGED IN'
				LogNotify('Welcome Back ' + username, 'Enjoy your stay!', '5000', artwork+'2movies.png')
				cj.save(cookie_file, ignore_discard=True)
				CATEGORIES('true')
				return False
			else:
				print 'YOU ARE LOGGED OUT'
				LogNotify('Login Failed at '+domain, 'Check settings', '5000', artwork+'2movies.png')
				CATEGORIES('false')
				return True
	else:
		print 'YOU ARE LOGGED OUT'
		LogNotify('Login Failed at '+domain, 'Check settings', '5000', artwork+'2movies.png')
		CATEGORIES('false')
		return True








def RELOGIN():
		if settings.getSetting('tmovies_account') == 'false':
				dialog = xbmcgui.Dialog()
				ok = dialog.ok('Account Login Not Enabled', '            Please Choose 2Movies Account Tab and Enable')
				if ok:
						LogNotify('2Movies Account Tab ', 'Please Enable Account', '5000', artwork+'2movies.png')
						print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
						addon.show_settings()

		else:
			STARTUP()

def STARTUP():
		autoupdates.STARTUP()
		username = settings.getSetting('tmovies_user')
		password = settings.getSetting('tmovies_pass')
		cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','cookies/'))
		cookiejar = os.path.join(cookiepath,'cookies.lwp')
		if settings.getSetting('tmovies_account') == 'true':
				if username is '' or password is '':
						dialog = xbmcgui.Dialog()
						ok = dialog.ok('Username or Password Not Set', '            Please Choose 2Movies Account Tab and Set')
						if ok:
								LogNotify('2Movies Account Tab ', 'Please set Username & Password!', '5000', )
								print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
								addon.show_settings()



				LOGIN()

		else:
			CATEGORIES('false')
#************************End Login****************************************************************************
#Main Links
def CATEGORIES(loggedin):
		main.addDir('[COLOR gold][B]TwoMovies - watch movies online[/COLOR][/B]',messages+'visittwomovies.txt','addonstatus',artwork +'mainlogo.png','','dir',1)
		if loggedin == 'true':
				main.addDir('[COLOR red][B]YOU ARE LOGGED IN[/COLOR][/B]',messages+'loggedintrue.txt','addonstatus',artwork +'loggedin.png','','dir',1)
				main.addDir('[COLOR red]Larger numbers of sources will take longer to load[/COLOR]',messages+'loggedintrue.txt','addonstatus',artwork +'loggedin.png','','dir',1)
		if loggedin == 'false':
				main.addDir('[COLOR white][B]Login/Re-Attempt Login[/COLOR][/B]','none','relogin',artwork +'relogin.png','','dir',1)
				main.addDir('[COLOR white][B]How to Login[/COLOR][/B]',messages+'loggedinfalse.txt','addonstatus',artwork +'howtologin.png','','dir',1)
		main.addDir('[COLOR white]Movies[/COLOR]','none','moviecat',artwork +'Icon_Menu_Movies_Menu.png','','dir',1)

		if settings.getSetting('tvshows') == 'true':
				main.addDir('[COLOR white]TV Shows[/COLOR]','none','tvcats',artwork +'Icon_Menu_TVShows_Menu.png','','dir',1)
		if settings.getSetting('adult') == 'true':
				text_file = None
				if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/")):
						os.makedirs(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/"))

				if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24")):
						pin = ''
						notice = xbmcgui.Dialog().yesno('Would You Like To Set an Adult Passcode','Would you like to set a passcode for the adult movies section?','','')
						if notice:
								keyboard = xbmc.Keyboard(pin,'Choose A New Adult Movie Passcode')
								keyboard.doModal()
								if keyboard.isConfirmed():
										pin = keyboard.getText()
								text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "w")
								text_file.write(pin)
								text_file.close()
						else:
								text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "w")
								text_file.write(pin)
								text_file.close()
				main.addDir('[COLOR white]Two Movies Adults Only Section[/COLOR]','none','adultallow',artwork +'Icon_Menu_Adult.png'  ,'','dir',1)


		if settings.getSetting('resolver') == 'true':
				main.addDir('[COLOR white]Resolver Settings[/COLOR]','none','resolverSettings',artwork +'Icon_Menu_Settings_ResolverSettings.png','','dir',1)
		#main.addDir('[COLOR gold]Changelog/Info[/COLOR]',messages+'loggedinfalse.txt','addonstatus',artwork +'changelog.png','','dir',1)
		main.addDir('[COLOR gold]Manage Downloads[/COLOR]','none','viewQueue',artwork +'downloads/Downloads_Manage.png','','',8)
		main.AUTO_VIEW('')




def MOVIECAT():
		main.addDir('Movies by Popularity','http://'+domain+'/browse_movies/all/byViews/all/','playyear',artwork +'moviespopularity.png','','dir',1)
		main.addDir('Movies by Rating','http://'+domain+'/browse_movies/all/byRating/all/','playyear',artwork +'moviesrating.png','','dir',1)
		main.addDir('Trending Movies','http://'+domain+'/','movieindex1',artwork +'Icon_Menu_Movies_Popularandtrending.png','','dir',1)
		main.addDir('Newly Added Movies','http://'+domain+'/new_release/','movieindex1',artwork +'moviesnewlyadded.png','','dir',1)
		main.addDir('Movies by Year ','none','byyear',artwork +'Icon_Menu_Movies_Byyear.png','','dir',1)
		main.addDir('Movie Genres ','http://'+domain+'/','genres',artwork +'Icon_Menu_Movies_Genre.png','','dir',1)
		main.addDir('A-Z Index','none','mazindex',artwork +'moviesa-z.png','','dir',1)
		main.addDir('[COLOR gold]Search by Movie Name[/COLOR] ','http://'+domain+'/search/?search_query=','searchm',artwork +'Icon_Menu_Movies_SearchName.png','','dir',1)
		if settings.getSetting('movietags') == 'true':
				main.addDir('[COLOR gold]Search by Custom Tag[/COLOR] ','http://'+domain+'/search/?search_query=','searcht',artwork +'Icon_Menu_Movies_SearchCustomTag.png','','dir',1)
		main.AUTO_VIEW('')

def MAZINDEX():
	 main.addDir('#','http://'+domain+'/letter/0/','azindex',artwork +'/movieaz/hash.png','','dir',1)
	 main.addDir('A','http://'+domain+'/letter/A/','azindex',artwork +'/movieaz/a.png','','dir',1)
	 main.addDir('B','http://'+domain+'/letter/B/','azindex',artwork +'/movieaz/b.png','','dir',1)
	 main.addDir('C','http://'+domain+'/letter/C/','azindex',artwork +'/movieaz/c.png','','dir',1)
	 main.addDir('D','http://'+domain+'/letter/D/','azindex',artwork +'/movieaz/d.png','','dir',1)
	 main.addDir('E','http://'+domain+'/letter/E/','azindex',artwork +'/movieaz/e.png','','dir',1)
	 main.addDir('F','http://'+domain+'/letter/F/','azindex',artwork +'/movieaz/f.png','','dir',1)
	 main.addDir('G','http://'+domain+'/letter/G/','azindex',artwork +'/movieaz/g.png','','dir',1)
	 main.addDir('H','http://'+domain+'/letter/H/','azindex',artwork +'/movieaz/h.png','','dir',1)
	 main.addDir('I','http://'+domain+'/letter/I/','azindex',artwork +'/movieaz/i.png','','dir',1)
	 main.addDir('J','http://'+domain+'/letter/J/','azindex',artwork +'/movieaz/j.png','','dir',1)
	 main.addDir('K','http://'+domain+'/letter/K/','azindex',artwork +'/movieaz/k.png','','dir',1)
	 main.addDir('L','http://'+domain+'/letter/L/','azindex',artwork +'/movieaz/l.png','','dir',1)
	 main.addDir('M','http://'+domain+'/letter/M/','azindex',artwork +'/movieaz/m.png','','dir',1)
	 main.addDir('N','http://'+domain+'/letter/N/','azindex',artwork +'/movieaz/n.png','','dir',1)
	 main.addDir('O','http://'+domain+'/letter/O/','azindex',artwork +'/movieaz/o.png','','dir',1)
	 main.addDir('P','http://'+domain+'/letter/P/','azindex',artwork +'/movieaz/p.png','','dir',1)
	 main.addDir('Q','http://'+domain+'/letter/Q/','azindex',artwork +'/movieaz/q.png','','dir',1)
	 main.addDir('R','http://'+domain+'/letter/R/','azindex',artwork +'/movieaz/r.png','','dir',1)
	 main.addDir('S','http://'+domain+'/letter/S/','azindex',artwork +'/movieaz/s.png','','dir',1)
	 main.addDir('T','http://'+domain+'/letter/T/','azindex',artwork +'/movieaz/t.png','','dir',1)
	 main.addDir('U','http://'+domain+'/letter/U/','azindex',artwork +'/movieaz/u.png','','dir',1)
	 main.addDir('V','http://'+domain+'/letter/V/','azindex',artwork +'/movieaz/v.png','','dir',1)
	 main.addDir('W','http://'+domain+'/letter/W/','azindex',artwork +'/movieaz/w.png','','dir',1)
	 main.addDir('X','http://'+domain+'/letter/X/','azindex',artwork +'/movieaz/x.png','','dir',1)
	 main.addDir('Y','http://'+domain+'/letter/Y/','azindex',artwork +'/movieaz/y.png','','dir',1)
	 main.addDir('Z','http://'+domain+'/letter/Z/','azindex',artwork +'/movieaz/z.png','','dir',1)
	 main.AUTO_VIEW('')


def ADULTALLOW():
		text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.twomovies/apc.24"), "r")
		line = file.readline(text_file)
		pin = ''
		if not line == '':
				keyboard = xbmc.Keyboard(pin,'Enter Your Passcode')
				keyboard.doModal()
				if keyboard.isConfirmed():
						pin = keyboard.getText()

		if pin == line:

				main.addDir('View Adult Movies','http://'+domain+'/browse_movies/Adult/byViews/all/','adultmovieindex',artwork +'Icon_Menu_Adult.png','','dir',1)
		else:
				notice = xbmcgui.Dialog().ok('Wrong Passcode','The passcode you entered is incorrect')

def BYYEAR():
		yearurl = 'http://'+domain+'/browse_movies/all/byViews/'
		#main.addDir('All ',yearurl+'all','playyear',artwork +'Icon_Menu_all.png','','dir',1)
		main.addDir('2015 ',yearurl+'2015','playyear',artwork +'Icon_Menu_2015.png','','dir',1)
		main.addDir('2014 ',yearurl+'2014','playyear',artwork +'Icon_Menu_2014.png','','dir',1)
		main.addDir('2013 ',yearurl+'2013','playyear',artwork +'Icon_Menu_2013.png','','dir',1)
		main.addDir('2012 ',yearurl+'2012','playyear',artwork +'Icon_Menu_2012.png','','dir',1)
		main.addDir('2011 ',yearurl+'2011','playyear',artwork +'Icon_Menu_2011.png','','dir',1)
		main.addDir('2010 ',yearurl+'2010','playyear',artwork +'Icon_Menu_2010.png','','dir',1)
		main.addDir('2009 ',yearurl+'2009','playyear',artwork +'Icon_Menu_2009.png','','dir',1)
		main.addDir('2008 ',yearurl+'2008','playyear',artwork +'Icon_Menu_2008.png','','dir',1)
		main.addDir('2007 ',yearurl+'2007','playyear',artwork +'Icon_Menu_2007.png','','dir',1)
		main.addDir('2006 ',yearurl+'2006','playyear',artwork +'Icon_Menu_2006.png','','dir',1)
		main.addDir('2005 ',yearurl+'2005','playyear',artwork +'Icon_Menu_2005.png','','dir',1)
		main.addDir('2004 ',yearurl+'2004','playyear',artwork +'Icon_Menu_2004.png','','dir',1)
		main.addDir('2003 ',yearurl+'2003','playyear',artwork +'Icon_Menu_2003.png','','dir',1)
		main.addDir('2002 ',yearurl+'2002','playyear',artwork +'Icon_Menu_2002.png','','dir',1)
		main.addDir('2001 ',yearurl+'2001','playyear',artwork +'Icon_Menu_2001.png','','dir',1)
		main.addDir('2000 ',yearurl+'2000','playyear',artwork +'Icon_Menu_2000.png','','dir',1)
		main.addDir('1999 ',yearurl+'1999','playyear',artwork +'Icon_Menu_1999.png','','dir',1)
		main.addDir('1998 ',yearurl+'1998','playyear',artwork +'Icon_Menu_1998.png','','dir',1)



def GENRES():

		main.addDir('Action','http://'+domain+'/browse_movies/Action/byViews/all/','movieindex',artwork +'Icon_Menu_action.png','','dir',1)
		main.addDir('Adventure','http://'+domain+'/browse_movies/Adventure/byViews/all/','movieindex',artwork +'Icon_Menu_adventure.png','','dir',1)
		main.addDir('Animation','http://'+domain+'/browse_movies/Animation/byViews/all/','movieindex',artwork +'Icon_Menu_animation.png','','dir',1)
		main.addDir('Biography','http://'+domain+'/browse_movies/Biography/byViews/all/','movieindex',artwork +'Icon_Menu_biography.png','','dir',1)
		main.addDir('Comedy','http://'+domain+'/browse_movies/Comedy/byViews/all/','movieindex',artwork +'Icon_Menu_comedy.png','','dir',1)
		main.addDir('Crime','http://'+domain+'/browse_movies/Crime/byViews/all/','movieindex',artwork +'Icon_Menu_crime.png','','dir',1)
		main.addDir('Documentary','http://'+domain+'/browse_movies/Documentary/byViews/all/','movieindex',artwork +'Icon_Menu_documentary.png','','dir',1)
		main.addDir('Drama','http://'+domain+'/browse_movies/Drama/byViews/all/','movieindex',artwork +'Icon_Menu_drama.png','','dir',1)
		main.addDir('Family','http://'+domain+'/browse_movies/Family/byViews/all/','movieindex',artwork +'Icon_Menu_family.png','','dir',1)
		main.addDir('Fantastic','http://'+domain+'/browse_movies/Fantastic/byViews/all/','movieindex',artwork +'Icon_Menu_fantastic.png','','dir',1)
		main.addDir('Fantasy','http://'+domain+'/browse_movies/Fantasy/byViews/all/','movieindex',artwork +'Icon_Menu_fantasy.png','','dir',1)
		main.addDir('Film-Noir','http://'+domain+'/browse_movies/Film-Noir/byViews/all/','movieindex',artwork +'Icon_Menu_film-noir.png','','dir',1)
		main.addDir('History','http://'+domain+'/browse_movies/History/byViews/all/','movieindex',artwork +'Icon_Menu_history.png','','dir',1)
		main.addDir('Horror','http://'+domain+'/browse_movies/Horror/byViews/all/','movieindex',artwork +'Icon_Menu_horror.png','','dir',1)
		main.addDir('Music','http://'+domain+'/browse_movies/Music/byViews/all/','movieindex',artwork +'Icon_Menu_music.png','','dir',1)
		main.addDir('Mystery','http://'+domain+'/browse_movies/Mystery/byViews/all/','movieindex',artwork +'Icon_Menu_mystery.png','','dir',1)
		main.addDir('Reality-TV','http://'+domain+'/browse_movies/Reality-TV/byViews/all/','movieindex',artwork +'Icon_Menu_reality-tv.png','','dir',1)
		main.addDir('Romance','http://'+domain+'/browse_movies/Romance/byViews/all/','movieindex',artwork +'Icon_Menu_romance.png','','dir',1)
		main.addDir('Sci-Fi','http://'+domain+'/browse_movies/Sci-Fi/byViews/all/','movieindex',artwork +'Icon_Menu_sci-fi.png','','dir',1)
		main.addDir('Thriller','http://'+domain+'/browse_movies/Thriller/byViews/all/','movieindex',artwork +'Icon_Menu_thriller.png','','dir',1)
		main.addDir('Western','http://'+domain+'/browse_movies/Western/byViews/all/','movieindex',artwork +'Icon_Menu_western.png','','dir',1)

		main.AUTO_VIEW('')

def AZINDEX(url):
		if settings.getSetting('tmovies_account') == 'true':
				try:
					cj.load(cookie_file, ignore_discard=True)
				except:
					print "Could not load cookie jar file."
		#link = net.http_GET(url).content
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		#if len(match) > 0:
		for url,sitethumb,name in match:
			matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
			for year in matchyear:
				data = main.GRABMETA(name,year)
				thumb = data['cover_url']
				yeargrab = data['year']
				year = str(yeargrab)
			favtype = 'movie'
			if 'watch_movie' in url:

				main.addDir(name+ ' (' + year +')',url,'linkpage',thumb,data,favtype,8)

		nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
		if len(nmatch) > 0:
				main.addDir('Next Page',(nmatch[0]),'azindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)

		main.AUTO_VIEW('movies')


def PLAYYEAR (url):
		if settings.getSetting('tmovies_account') == 'true':
				try:
					cj.load(cookie_file, ignore_discard=True)
				except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		#nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
		if len(match) > 0:
		 for url,sitethumb,name in match:
		   matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_movies/all/byViews/(.+?)/">').findall(link)
		   if len(matchyear) > 0:
			 for year in matchyear:
				 data = main.GRABMETA(name,year)
				 thumb = data['cover_url']
				 yeargrab = data['year']
				 year = str(yeargrab)

			 favtype = 'movie'
			 main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype,len(url))
			 nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
		if len(nmatch) > 0:
			 main.addDir('Next Page',(nmatch[0]),'playyear',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)

		main.AUTO_VIEW('movies')

def MOVIETAGS(url):
		if settings.getSetting('tmovies_account') == 'true':
			  #net.set_cookies(cookiejar)
			  try:
					cj.load(cookie_file, ignore_discard=True)
			  except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)" style=".+?; font-style: .+?; font-variant: .+?; font-size-adjust: .+?; font-stretch:.+?; -x-system-font: .+?; color: .+?; font-weight:.+?; line-height: .+?; word-spacing: .+?; letter-spacing:.+?;font-size:.+?;margin:.+?;">(.+?)</a>').findall(link)
		for url,name in match:

				main.addDir(name,url,'movietagindex',artwork +'Icon_Menu_Movies_ByTag.png','','dir',len(url))
		main.AUTO_VIEW('')

def MOVIETAGINDEX(url):
		if settings.getSetting('tmovies_account') == 'true':
			  #net.set_cookies(cookiejar)
			  try:
					cj.load(cookie_file, ignore_discard=True)
			  except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		if len(match) > 0:
		 for url,sitethumb,name in match:
		  matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_movies/all/byViews/(.+?)/">').findall(link)
		  if len(matchyear) > 0:
			 for year in matchyear:
				 data = main.GRABMETA(name,year)
				 thumb = data['cover_url']
				 yeargrab = data['year']
				 year = str(yeargrab)


			 favtype = 'movie'
			 main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype,len(url))

		main.AUTO_VIEW('movies')

def ADULTMOVIEINDEX(url):
		if settings.getSetting('tmovies_account') == 'true':
			  #net.set_cookies(cookiejar)
			  try:
					cj.load(cookie_file, ignore_discard=True)
			  except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		if len(match) > 0:
		 for url,sitethumb,name in match:
		   matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_movies/all/byViews/(.+?)/">').findall(link)
		   if len(matchyear) > 0:
			 for year in matchyear:
				 data = main.GRABMETA(name,year)
				 thumb = data['cover_url']
				 yeargrab = data['year']
				 year = str(yeargrab)
			 favtype = 'movie'
			 main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype,len(url))
			 nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
		if len(nmatch) > 0:

				 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)

		main.AUTO_VIEW('movies')


def MOVIEINDEX(url):
		if settings.getSetting('tmovies_account') == 'true':
			  #net.set_cookies(cookiejar)
			  try:
					cj.load(cookie_file, ignore_discard=True)
			  except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height="147px" width="102px" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		if len(match) > 0:
		 for url,sitethumb,name in match:
		   matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_movies/all/byViews/(.+?)/">').findall(link)
		   if len(matchyear) > 0:
			 for year in matchyear:
				 data = main.GRABMETA(name,year)
				 thumb = data['cover_url']
				 yeargrab = data['year']
				 year = str(yeargrab)
			 favtype = 'movie'
			 main.addDir(name+' ('+ year +')',url,'linkpage',thumb,data,favtype,len(url))
			 nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
		if len(nmatch) > 0:

				 main.addDir('Next Page',(nmatch[0]),'movieindex',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)

		main.AUTO_VIEW('movies')


def MOVIEINDEX1(url):
		if settings.getSetting('tmovies_account') == 'true':
			  #net.set_cookies(cookiejar)
			  try:
					cj.load(cookie_file, ignore_discard=True)
			  except:
					print "Could not load cookie jar file."
		link = OPEN_URL(url)
		match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
		if len(match) > 0:
		 print "I AM LOOKING"
		 for url,sitethumb,name in match:
		   matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
		   #matchview=re.compile('<span class="filmtime">(.+?)</span></div><br>').findall(link)
		   if len(matchyear) > 0:
			  for year in matchyear:
				 try:
						 data = main.GRABMETA(name,year)
						 thumb = data['cover_url']
						 yeargrab = data['year']
						 year = str(yeargrab)
				 except:
						 data = ''
						 thumb = sitethumb
						 year = year
			  favtype = 'movie'
			  if 'watch_movie' in url:
					  try:
						   main.addDir(name+ ' (' + year +')',url,'linkpage',thumb,data,favtype,len(url))
					  except:
						   pass
					  nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
					  if len(nmatch) > 0:
							 main.addDir('Next Page',(nmatch[0]),'movieindex1',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)

		main.AUTO_VIEW('movies')


def LINKPAGE(url,name):
		movie_name = name[:-6]
		year = name[-6:]
		movie_name = movie_name.decode('UTF-8','ignore')
		dlfoldername = name
		if settings.getSetting('tmovies_account') == 'true':
								COOKIELOADER(url)
		link = OPEN_URL(url)
		names = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"})
		urls = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"}, ret='href')
		for name, url in zip(names, urls):
				main.addDir(name,url,'linkpageb','','','',len(urls))

def LINKPAGEORIG(url,name):
				movie_name = name[:-6]
				year = name[-6:]
				movie_name = movie_name.decode('UTF-8','ignore')
				dlfoldername = name
				if settings.getSetting('tmovies_account') == 'true':
								COOKIELOADER(url)
				link = OPEN_URL(url)
				match=re.compile('<a href="(.+?)" title="Watch Movie!"').findall(link)
				for url in match:
						#START QUICK GRAB
						main.addDir(name,url,'linkpageb','','','',len(url))

def LINKPAGEB(url,name):
				if  "full" in url:
						link = OPEN_URL(url)
						if 'Before you start watching' in link:
														print 'Confirmation Button '
														url = url
														header_dict = {}
														header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
														header_dict['Connection'] = 'keep-alive'
														header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
														header_dict['Origin'] = ''+domain+''
														header_dict['Referer'] = url
														header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
														form_data = {'confirm':'I understand, Let me watch the movie now!'}
														net.set_cookies(cookiejar)
														conbutton = net.http_POST(url, form_data=form_data,headers=header_dict)

						link=OPEN_URL(url)
						link=link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
						matchurl=re.compile('Sourcelink:<arel="nofollow"onlicktarget="_blank">(.+?)</').findall(link)
						for urls in matchurl:
							print "LINK URL IS =" +urls
							urls = str(urls)
							urls = urls.replace('&rel=nofollow','')
							hmf = urlresolver.HostedMediaFile(urls)
							if hmf:
											print "WE HAVE A MATCH"
											LogNotify('Please be pateint!', 'Attempting to Resolve Link', '5000', artwork+'2movies.png')
											VIDPAGE(urls,name)
							else:
									LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', artwork+'2movies.png')
									print "NO MATCH"


def VIDPAGE(url,name):
		params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
		url = url
		name = name
		thumb=mainimg
		main.RESOLVE2(name,url,thumb)


def DLVIDPAGE(url,name):
		params = {'url':url, 'mode':mode, 'name':dlfoldername, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
		main.RESOLVEDL(name,url,thumb)









#Start Ketboard Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHM(url):
	searchUrl = url
	vq = _get_keyboard( heading="Searching for Movies" )
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title'
	print "Searching URL: " + searchUrl
	MOVIEINDEX1(searchUrl)

	main.AUTO_VIEW('movies')




def SEARCHT(url):
	searchUrl = url
	vq = _get_keyboard( heading="TIME INTENSIVE!! Be Patient!!" )
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=tag'
	print "Searching URL: " + searchUrl
	MOVIEINDEX1(searchUrl)

	main.AUTO_VIEW('movies')


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







params=get_params()
url=None
name=None
mode=None
year=None
imdb_id=None
nmatch = 1

#------added for Help Section
try:
		iconimage=urllib.unquote_plus(params["iconimage"])
except:
		pass

try:
		thumb=urllib.unquote_plus(params["thumb"])
except:
		pass

try:
		fanart=urllib.unquote_plus(params["fanart"])
except:
		pass
try:
		description=urllib.unquote_plus(params["description"])
except:
		pass

try:
		filetype=urllib.unquote_plus(params["filetype"])
except:
		pass

# END OF HelpSection addition ===========================================

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass

try:
		nmatch=urllib.unquote_plus(params["nmatch"])
except:
		pass

try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
#May need toremove
#try:
 #       mode=int(params["mode"])
#except:
 #       pass

try:
		mode=urllib.unquote_plus(params["mode"])
except:
		pass

try:
		year=urllib.unquote_plus(params["year"])
except:
		pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Year: "+str(year)


if mode==None or url==None or len(url)<1:
		print ""
		STARTUP()


elif mode=='categories':
		print ""+loggedin
		CATEGORIES(loggedin)

elif mode=='login':
		print ""+url
		LOGIN(url)

elif mode=='relogin':
		print ""
		RELOGIN()


elif mode=='helpmenu':
		print ""
		HELPMENU()

elif mode == "help list menu":
		items = HELP(name)

elif mode == "wizardstatus":
		print""+url
		items = WIZARDSTATUS(url)



elif mode=='moviecat':
		print ""
		MOVIECAT()

elif mode=='tvcats':
		print ""
		tvshow.TVCATS()



elif mode=='adultallow':
		print ""
		ADULTALLOW()

elif mode=='byyear':
		print ""
		BYYEAR()

elif mode=='tvbyyear':
		print ""
		tvshow.TVBYYEAR()



elif mode=='genres':
		print ""
		GENRES()

elif mode=='tvgenres':
		print ""
		tvshow.TVGENRES()




elif mode=='mazindex':
		print ""
		MAZINDEX()



elif mode=='playyear':
		print ""+url
		PLAYYEAR(url)


elif mode=='tvplayyear':
		print ""+url
		tvshow.TVPLAYYEAR(url)



elif mode=='tvplaygenre':
		print ""+url
		tvshow.TVPLAYGENRE(url)


elif mode=='adultmovieindex':
		print ""+url
		ADULTMOVIEINDEX(url)


elif mode=='movieindex':
		print ""+url
		MOVIEINDEX(url)

elif mode=='lateshow':
		print ""+url
		tvshow.LATESHOW(url)

elif mode=='searchshow':
		print ""+url
		tvshow.SEARCHSHOW(url)

elif mode=='movietagindex':
		print ""+url
		MOVIETAGINDEX(url)

elif mode=='movieindex1':
		print ""+url
		MOVIEINDEX1(url)

elif mode=='azindex':
		print ""+url
		AZINDEX(url)

elif mode=='movietags':
		print ""+url
		MOVIETAGS(url)

elif mode=='vidpage':
		print ""+url
		VIDPAGE(url,name)


elif mode=='dlvidpage':
		print ""+url
		DLVIDPAGE(url,name)

elif mode=='dltvvidpage':
		print ""+url
		tvshow.DLTVVIDPAGE(url,name)


elif mode=='tvvidpage':
		print ""+url
		tvshow.TVVIDPAGE(url,name)




elif mode=='linkpage':
		print ""+url
		LINKPAGE(url,name)

elif mode=='linkpageb':
		print ""+url
		LINKPAGEB(url,name)

elif mode=='azlinkpage':
		print ""+url
		tvshow.AZLINKPAGE(url,name)

elif mode=='tvlinkpage':
		print ""+url
		tvshow.TVLINKPAGE(url,name)


elif mode=='tvlinkpageb':
		print ""+url
		tvshow.TVLINKPAGEB(url,name,thumb,mainimg)


elif mode=='episodes':
		print ""+url
		tvshow.EPISODES(url,name,thumb)



elif mode=='resolve':
		print ""+url
		main.RESOLVE(url,name,iconimage)



elif mode=='videoresolve':
		print ""+url
		status.VIDEORESOLVE(url,name,iconimage)

elif mode=='ytvideoresolve':
		print ""+url
		status.YTVIDEORESOLVE(url,name,iconimage)

elif mode=='resolve2':
		print ""+url
		main.RESOLVE2(name,url,thumb)

elif mode=='resolvedl':
		print ""+url
		main.RESOLVEDL(url,name,thumb,favtype)

elif mode=='resolvetvdl':
		print ""+url
		main.RESOLVETVDL(name,url,thumb,favtype)



elif mode=='searchm':
		print ""+url
		SEARCHM(url)




elif mode=='searchtv':
		print ""+url
		tvshow.SEARCHTV(url)

elif mode=='downloadFile':
		print ""+url
		main.downloadFile(url)


elif mode=='helpcatagories':
		print ""+url
		HELPCATEGORIES(url)

elif mode=='helpstat':
		HELPSTAT(name,url,description)



elif mode=='searcht':
		print ""+url
		SEARCHT(url)

elif mode=='resolverSettings':
		print ""+url
		urlresolver.display_settings()

elif mode=='loginSettings':
		print ""+url
		addon.show_settings('tmovies_account')

elif mode == "dev message":
	ADDON.setSetting('dev_message', value='run')
	dev_message()

elif mode=='helpwizard':
		HELPWIZARD(name,url,description,filetype)

#=================ForDL===========================
elif mode=='viewQueue':
		print ""+url
		main.viewQueue()

elif mode=='download':
		print ""+url
		main.download()

elif mode=='removeFromQueue':
		print ""+url
		main.removeFromQueue(name,url,thumb,ext,console)

elif mode=='killsleep':
		print ""+url
		main.KILLSLEEP()


elif mode=='cookieloader':
		print ""+url
		COOKIELOADER()



#==================END DL=====================================

#==================Start Status/Help==========================

elif mode == "statuscategories": print""+url; items=status.STATUSCATEGORIES(url)
elif mode == "addonstatus": print""+url; items=status.ADDONSTATUS(url)
elif mode=='getrepolink': print""+url; items=status.GETREPOLINK(url)
elif mode=='getshorts': print""+url; items=status.GETSHORTS(url)
elif mode=='getrepo': status.GETREPO(name,url,description,filetype)
elif mode=='getvideolink': print""+url; items=status.GETVIDEOLINK(url)
elif mode=='getvideo': status.GETVIDEO(name,url,iconimage,description,filetype)
elif mode=='addoninstall': status.ADDONINSTALL(name,url,description,filetype)
elif mode=='addshortcuts': status.ADDSHORTCUTS(name,url,description,filetype)
elif mode=='addsource': status.ADDSOURCE(name,url,description,filetype)
elif mode=='playstream': status.PLAYSTREAM(name,url,iconimage,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))



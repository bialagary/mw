
# 2Movies TV SHOW Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main
from metahandler import metahandlers
from resources.modules import main
from t0mm0.common.addon import Addon
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
from tm_libs import dom_parser

addon_id = 'plugin.video.twomovies'
addon = main.addon

  
from t0mm0.common.net import Net

net = Net()

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer

# Cache  
cache = StorageServer.StorageServer("Two Movies", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
nmatch = addon.queries.get('nmatch', '')


debug = 'false'
if debug =='true':
        print 'Mode is: ' + mode
        print 'Url is: ' + url
        print 'Name is: ' + name
        print 'Thumb is: ' + thumb
        print 'Extension is: ' + ext
        print 'File Type is: ' + console
        print 'DL Folder is: ' + dlfoldername
        print 'Favtype is: ' + favtype
        print 'Main Image is: ' + mainimg

# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
grab=metahandlers.MetaData()
net = Net()
domain = settings.getSetting('tmovies_domain')
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','cookies/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')
#Username and Password Setup############
username = settings.getSetting('tmovies_user')
password = settings.getSetting('tmovies_pass')
form_data = {'login':username, 'password':password,'remember_me':'on','submit_login':'Login', 'submit_login':''}

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


def TVCATS():

          main.addDir('[COLOR gold]TwoMovies - watch movies online[/COLOR]',messages+'visittwomovies.txt','addonstatus',artwork +'mainlogo.png','','dir',1)
          main.addDir('TV Shows by Year','none','tvbyyear',artwork +'Icon_Menu_TVShows_ByYear.png','','dir',1)
          main.addDir('TV Shows by Genre','none','tvgenres',artwork + '/tvshows/tvshowsgenre.png','','dir',1)
          main.addDir('TV Shows by Rating','http://'+domain+'/browse_tv_shows/all/byRating/all/','tvplayyear',artwork + '/tvshows/tvshowsrating.png','','dir',1)
          main.addDir('TV Shows by Popularity','http://'+domain+'/browse_tv_shows/all/byViews/all/','tvplayyear',artwork + '/tvshows/tvshowspopularity.png','','dir',1)
          #main.addDir('[COLOR gold]Search TV Shows[/COLOR]','http://'+domain+'/search/?search_query=','searchtv',artwork + 'Icon_Menu_TVShows_Search.png','','dir',1)
          
          main.AUTO_VIEW('')    


def TVBYYEAR():
        yearurl = 'http://'+domain+'/browse_tv_shows/all/byViews/'
        main.addDir('2015 ',yearurl+'2015','tvplayyear',artwork +'Icon_Menu_TVShows_2015.png','','dir',1)
        main.addDir('2014 ',yearurl+'2014','tvplayyear',artwork +'Icon_Menu_TVShows_2014.png','','dir',1)
        main.addDir('2013 ',yearurl+'2013','tvplayyear',artwork +'Icon_Menu_TVShows_2013.png','','dir',1)
        main.addDir('2012 ',yearurl+'2012','tvplayyear',artwork +'Icon_Menu_TVShows_2012.png','','dir',1)
        main.addDir('2011 ',yearurl+'2011','tvplayyear',artwork +'Icon_Menu_TVShows_2011.png','','dir',1)
        main.addDir('2010 ',yearurl+'2010','tvplayyear',artwork +'Icon_Menu_TVShows_2010.png','','dir',1)
        main.addDir('2009 ',yearurl+'2009','tvplayyear',artwork +'Icon_Menu_TVShows_2009.png','','dir',1)
        main.addDir('2008 ',yearurl+'2008','tvplayyear',artwork +'Icon_Menu_TVShows_2008.png','','dir',1)
        main.addDir('2007 ',yearurl+'2007','tvplayyear',artwork +'Icon_Menu_TVShows_2007.png','','dir',1)
        main.addDir('2006 ',yearurl+'2006','tvplayyear',artwork +'Icon_Menu_TVShows_2006.png','','dir',1)
        main.addDir('2005 ',yearurl+'2005','tvplayyear',artwork +'Icon_Menu_TVShows_2005.png','','dir',1)
        main.addDir('2004 ',yearurl+'2004','tvplayyear',artwork +'Icon_Menu_TVShows_2004.png','','dir',1)
        main.addDir('2003 ',yearurl+'2003','tvplayyear',artwork +'Icon_Menu_TVShows_2003.png','','dir',1)
        main.addDir('2002 ',yearurl+'2002','tvplayyear',artwork +'Icon_Menu_TVShows_2002.png','','dir',1)
        main.addDir('2001 ',yearurl+'2001','tvplayyear',artwork +'Icon_Menu_TVShows_2001.png','','dir',1)
        main.addDir('2000 ',yearurl+'2000','tvplayyear',artwork +'Icon_Menu_TVShows_2000.png','','dir',1)
        
        main.AUTO_VIEW('')


def TVGENRES():
        
        main.addDir('Action','http://'+domain+'/browse_tv_shows/Action/byViews/all/','tvplaygenre',artwork +'/tvshows/action.png','','dir',1)
        main.addDir('Adventure','http://'+domain+'/browse_tv_shows/Adventure/byViews/all/','tvplaygenre',artwork +'/tvshows/adventure.png','','dir',1)
        main.addDir('Animation','http://'+domain+'/browse_tv_shows/Animation/byViews/all/','tvplaygenre',artwork +'/tvshows/animation.png','','dir',1)
        main.addDir('Biography','http://'+domain+'/browse_tv_shows/Biography/byViews/all/','tvplaygenre',artwork +'/tvshows/biography.png','','dir',1)
        main.addDir('Comedy','http://'+domain+'/browse_tv_shows/Comedy/byViews/all/','tvplaygenre',artwork +'/tvshows/comedy.png','','dir',1)
        main.addDir('Crime','http://'+domain+'/browse_tv_shows/Crime/byViews/all/','tvplaygenre',artwork +'/tvshows/crime.png','','dir',1)
        main.addDir('Documentary','http://'+domain+'/browse_tv_shows/Documentary/byViews/all/','tvplaygenre',artwork +'/tvshows/documentary.png','','dir',1)
        main.addDir('Drama','http://'+domain+'/browse_tv_shows/Drama/byViews/all/','tvplaygenre',artwork +'/tvshows/drama.png','','dir',1)
        main.addDir('Family','http://'+domain+'/browse_tv_shows/Family/byViews/all/','tvplaygenre',artwork +'/tvshows/family.png','','dir',1)
        main.addDir('Fantastic','http://'+domain+'/browse_tv_shows/Fantastic/byViews/all/','tvplaygenre',artwork +'/tvshows/fantastic.png','','dir',1)
        main.addDir('Fantasy','http://'+domain+'/browse_tv_shows/Fantasy/byViews/all/','tvplaygenre',artwork +'/tvshows/fantasy.png','','dir',1)
        main.addDir('Film-Noir','http://'+domain+'/browse_tv_shows/Film-Noir/byViews/all/','tvplaygenre',artwork +'/tvshows/film-noir.png','','dir',1)
        main.addDir('History','http://'+domain+'/browse_tv_shows/History/byViews/all/','tvplaygenre',artwork +'/tvshows/history.png','','dir',1)
        main.addDir('Horror','http://'+domain+'/browse_tv_shows/Horror/byViews/all/','tvplaygenre',artwork +'/tvshows/horror.png','','dir',1)
        main.addDir('Music','http://'+domain+'/browse_tv_shows/Music/byViews/all/','tvplaygenre',artwork +'/tvshows/music.png','','dir',1)
        main.addDir('Mystery','http://'+domain+'/browse_tv_shows/Mystery/byViews/all/','tvplaygenre',artwork +'/tvshows/mystery.png','','dir',1)
        main.addDir('Reality-TV','http://'+domain+'/browse_tv_shows/Reality-TV/byViews/all/','tvplaygenre',artwork +'/tvshows/reality-tv.png','','dir',1)
        main.addDir('Romance','http://'+domain+'/browse_tv_shows/Romance/byViews/all/','tvplaygenre',artwork +'/tvshows/romance.png','','dir',1)
        main.addDir('Sci-Fi','http://'+domain+'/browse_tv_shows/Sci-Fi/byViews/all/','tvplaygenre',artwork +'/tvshows/sci-fi.png','','dir',1)
        main.addDir('Thriller','http://'+domain+'/browse_tv_shows/Thriller/byViews/all/','tvplaygenre',artwork +'/tvshows/thriller.png','','dir',1)
        main.addDir('Western','http://'+domain+'/browse_tv_shows/Western/byViews/all/','tvplaygenre',artwork +'/tvshows/western.png','','dir',1)
        
        main.AUTO_VIEW('')

               

        

        
def TVPLAYYEAR (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = OPEN_URL(url)
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
           for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                   
           types = 'tvshow'
           main.addSDir(name+'('+year+')',url,'episodes',thumb,'',types,data)
           nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplayyear',artwork + '/tvshows/nextpage.png','','dir',1)
             
        main.AUTO_VIEW('tvshow')        
def TVPLAYGENRE (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = OPEN_URL(url)
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://'+domain+'/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                
                   
             types = 'tvshow'
             main.addSDir(name+'('+year+')',url,'episodes',thumb,'',types,data)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplaygenre',artwork + '/tvshows/nextpage.png','','dir',1)
             
        main.AUTO_VIEW('tvshow')



def SEARCHSHOWOLD(url):
             if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
             link = OPEN_URL(url)
             match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
             if len(match) > 0:
              for url,sitethumb,name in match:
               matchyear=re.compile('<div class="filmyar"><a class="filmyar" href="http://'+domain+'/browse_tv_shows/all/byViews/.+?/">(.+?)</a>').findall(link)
               if len(match) > 0:
                    for year in matchyear:        
                         data = main.GRABTVMETA(name,year)
                         thumb = data['cover_url']
                    types = 'tvshow'
                    if 'watch_tv_show' in url:
                              main.addTVDir(name+'('+year+')',url,'episodes',thumb,data,types,'')
                              main.AUTO_VIEW('tvshows')

def SEARCHSHOW(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = OPEN_URL(url)
        match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         print "I AM LOOKING"       
         for url,sitethumb,name in match: 
           matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
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
              if  'watch_movie' in url:
                      try:        
                           main.addDir(name+ ' (' + year +')',url,'episodes',thumb,data,favtype,len(url))
                      except:
                           pass
                      nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>\n').findall(link)
                      if len(nmatch) > 0:
                             main.addDir('Next Page',(nmatch[0]),'searchshow',artwork +'Icon_Menu_Movies_nextpage.png','','dir',1)
                     
        main.AUTO_VIEW('movies')

        

def SEARCHSHOWOLD(url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = OPEN_URL(url)
        match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match: 
           matchyear=re.compile('<a class="filmyar" href=".+?">(.+?)</a>').findall(link)
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
              if 'watch_tv_show' in url:
                              main.addTVDir(name+'('+year+')',url,'episodes',thumb,data,types,'')
                              main.AUTO_VIEW('tvshows')
                                                        
def EPISODES(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,} 
    dlfoldername = name
    mainimg = thumb
    show = name
    if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
    link = OPEN_URL(url)
    matchurl=re.compile('<a class="linkname" href="(.+?)">.+? - (.+?)</a>').findall(link)             
    for url,epname in matchurl:
         matchse=re.compile('http://'+domain+'/watch_episode/(.+?)/(.+?)/(.+?)/').findall(url)
         for showname,season, episode in matchse:
              s = 'S' + season
              e = 'E' + episode
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPDir(name,url,thumb,'tvlinkpage',show,dlfoldername,mainimg,season,episode)
             
              main.AUTO_VIEW('tvshow')



def TVLINKPAGE(url,name):
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
				main.addDir(name,url,'tvlinkpageb','','','',len(url))



def TVLINKPAGEB(url,name,thumb,mainimg):
            showname = name
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
                    urls = str(urls)
                    urls = urls.replace('&rel=nofollow','')
                    hmf = urlresolver.HostedMediaFile(urls)
                    if hmf:
                                print "WE HAVE A MATCH"
                                LogNotify('Please be pateint!', 'Attempting to Resolve Link', '5000', artwork+'2movies.png')
                                TVVIDPAGE(urls,name)
                    else:
                                LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', artwork+'2movies.png')
                                print "NO MATCH"


                                   
def DLTVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}        
        main.RESOLVETVDL(name,url,thumb)

def TVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,} 
        url = url
        name =name        
        main.RESOLVE2(name,url,thumb)

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	SEARCHSHOW(searchUrl)

	main.AUTO_VIEW('tvshow')




#NAME METHOD*****************************


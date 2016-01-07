import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmcaddon,os
from metahandler import metahandlers
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer

addon_id = 'plugin.video.filmikz'
addon = Addon(addon_id, sys.argv)

cache = StorageServer.StorageServer("Filmikz", 0)

base_url = 'http://filmikz.ch'
artwork = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.filmikz/art/', ''))

settings = xbmcaddon.Addon(id=addon_id)
adult_content = settings.getSetting('adult_content')

grab=metahandlers.MetaData()
net = Net()

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
year = addon.queries.get('year', '')
season = addon.queries.get('season', '')
episodes = addon.queries.get('episodes', '')
types = addon.queries.get('types', '')
fanart = addon.queries.get('fanart', '')
imdb_id = addon.queries.get('imdb_id', '')
host = addon.queries.get('host', '')

print "Mode is: "+str(mode)
print "URL is: "+str(url)
print "Name is: "+str(name)
print "Thumb is: "+str(thumb)
print "Season is: "+str(season)
print "episodes is: "+str(episodes)
print "Type is: "+str(types)
print "IMDB ID is: "+str(imdb_id)
print "Host: "+str(host)

def addDir(name,url,mode,thumb,types,fav):
        fanart = ''
        scraped_thumb = thumb
        scraped_name = name
        addon_fanart = artwork + 'fanart.jpg'
        meta = None
        try:
             meta = getMeta(name,types)
        except:
             pass

        try:
                meta['title'] = scraped_name
                thumb = meta['cover_url']
                fanart = meta['backdrop_url']
        except:
                name = scraped_name
                
        if thumb == '':
                thumb = scraped_thumb
        if fanart == '':
             fanart = addon_fanart
                     
        params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types}
        if meta:
                addon.add_directory(params, meta, img=thumb, fanart=fanart)
        else:
                addon.add_directory(params, {'title':name}, img=thumb ,fanart=fanart)

def addADir(name,url,mode,thumb,plot,fav):
     fanart = artwork + 'fanart.jpg'
     params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':'adult'}
     meta = {'title':name, 'cover_url':thumb, 'plot':plot}
     addon.add_directory(params, meta, img= thumb, fanart=fanart)

def addHost(host,name,url,mode,thumb):
     fanart = artwork + 'fanart.jpg'
     thumb = artwork + host +'.jpg'
     params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types, 'host':host}
     addon.add_directory(params, {'title':host}, img= thumb, fanart=fanart)

def getMeta(name,types):
        meta = 0
        imdb_id = None
        season = None
        episodes = None
        if types=='movies':
                head,sep,tail = name.partition('(')
                name = head
                year = tail.replace(')','')
                meta = grab.get_meta('movie',name,year)
        elif types=='episodes':
                show = None
                show_meta = None
                S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',name)
                SXE = re.findall('\d[Xx]\d',name)
                SXEE = re.findall('\d[Xx]\d\d',name)
                if S00E00:
                        split = re.split('[Ss]\d\d[Ee]\d\d',name)
                        show = str(split[0])

                        S00E00 = str(S00E00)
                        S00E00.strip('[Ss][Ee]')
                        S00E00 = S00E00.replace("u","")

                        episodes = S00E00[-4:]
                        episodes = episodes[:-2]

                        season = S00E00[:5]
                        season = season[-2:]
                        
                if SXE:
                      split = re.split('\d[Xx]\d',name)
                      show = str(split[0])
                      SXE = str(SXE)
                      SXE = SXE.replace("u","")
                      season = SXE[2]
                      episodes = SXE[4]

                if SXEE:
                      split = re.split('\d[Xx]\d\d',name)
                      show = str(split[0])
                      SXEE = str(SXEE)
                      SXEE = SXEE.replace("u","")
                      sesaon = SXEE[2]
                      episodes = SXEE[4] + SXEE[5]
                      
                if 'Once Upon a Time' in show:
                         show = 'Once Upon a Time (2011)'
                if 'Dracula 2013' in show:
                         show = 'Dracula'
                if 'Castle' in show:
                         show = 'Castle (2009)'
                if 'Eastbound and Down' in show:
                         show = 'Eastbound & Down'
                if 'Marvels Agents of' in show:
                     show  = "Marvel's Agents of S.H.I.E.L.D."
                      
                show_meta = grab.get_meta('tvshow',show)
                imdb_id = show_meta['imdb_id']
                
                meta = grab.get_episode_meta(show,imdb_id,int(season),int(episodes))
     
        return(meta)

def resolvable(url):
     status = None
     hmf = urlresolver.HostedMediaFile(url)
     if hmf:
          status = True

     elif 'epornik' in url:
          status = True

     else:
          status = False
          
     return(status)

def AUTOVIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view'))
                        elif content == 'episodes':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episodes-view'))      
                        else:
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view'))
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view'))
          
def CATEGORIES():
        if adult_content == 'true':
                addDir('Adult Movies',base_url + '/index.php?genre=14','adultIndex',artwork + 'Icon_menu_Adults.png','dir',False)  
        addDir('Recently Added Movies',base_url + '/index.php','index',artwork + 'Icon_menu_Moviesrecentlyadded.jpg','dir',False)
        addDir('Recently Added Episodes',base_url + '/index.php?genre=15','index',artwork + 'Icon_menu_TVShowsrecentlyadded.jpg','dir',False)
        addDir('Movie Genres',base_url,'genres',artwork + 'Icon_menu_Moviesgenres.jpg','dir',False)
        #addDir('Favorites','none','favorites', artwork + 'Icon_menu_Favorites.jpg','dir',False)
        addDir('Search','none','search',artwork + 'Icon_menu_Search.jpg','dir',False)
        addDir('Resolver Settings','none','resolverSettings',artwork + 'Icon_menu_resolversettings.jpg','dir',False)

def INDEX(url):
        types = ''
        sending_url = url
        link = net.http_GET(url).content
        pages=re.compile("<a style=\'color:red;\' href=\'(.+?)'>(.+?)</a>").findall(link)

        if len(pages) > 0:
                  if url == base_url + '/index.php':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=15':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=3':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=2':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=11':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=12':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=1':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=5':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=6':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=13':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=4':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  elif url == base_url + '/index.php?genre=14':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                  else:
                       try:
                          next_page = str(pages[11][0])
                          addDir('Next Page',base_url + '/' + next_page,'index',artwork + 'Icon_Next.jpg','dir',False)
                       except:
                            pass

        match=re.compile('<a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?" border=".+?" /></a></div></td>\n                           \n                            <td width=".+?" valign=".+?" class=".+?"  align=".+?"><p><strong>(.+?): </strong>').findall(link)
        for url,thumb,name in match:
             show=''
             if 'XXX' in url:
                  continue
             else:
                  if re.search('[Ss]\d\d[Ee]\d\d',name) or  re.search('\d[Xx]\d',name):
                       if 'genre=15' in sending_url:
                              types = 'episodes'
                              addDir(name,base_url + url,'videoLinks',base_url + '/' + thumb,'episodes',False)
                  else:
                     types = 'movies'
                     addDir(name,base_url + url,'videoLinks',base_url + '/' + thumb,'movies',False)
        AUTOVIEW(types)

def ADULTINDEX(url):
        link = net.http_GET(url).content
        pages=re.compile("<a style=\'color:red;\' href=\'(.+?)'>(.+?)</a>").findall(link)
        
        for url,name in pages:
             if '&rsaquo' in name:
                  addDir('Next Page',base_url +'/' + url,'adultIndex',artwork + 'Icon_Next.jpg','dir',False)
        
        match=re.compile('<img src="(.+?)" width=".+?" height=".+?" border=".+?" /></a></div></td>\n                           \n                            <td width=".+?" valign=".+?" class=".+?"  align=".+?"><p><strong>(.+?): </strong></p>\n                                <p>(.+?)</p>\n                              <p><span class=".+?"><a href="/(.+?)">').findall(link)
        for thumbnail,name,plot,url in match:
             url = base_url + '/' + url
             addADir(name,url,'videoLinks',base_url + '/' + thumbnail,plot,False)
        AUTOVIEW('movies')

def VIDEOLINKS(url,name):       
        link = net.http_GET(url).content
        links1=re.compile('<input type=button value="(.+?)" onClick="javascript:popUp((.+?))">').findall(link)
        for host, url,url2 in links1:
             url = base_url + url
             url = url.replace("('","")
             link = net.http_GET(url).content
             links2=re.compile('<frameset  cols=".+?">\n  <frame src="(.+?)" />\n  <frame src=".+?" />').findall(link)
             try:
                  url = links2[0]
             except:
                  pass
             if resolvable(url):
                  try:
                       addHost(host,name,url,'resolve','')
                  except:
                       pass

def RESOLVE(name,host,url):
        if 'epornik' in url:
                link = net.http_GET(url).content
                elink=re.compile('s1.addVariable(.+?);').findall(link)
                dirty = re.sub("[',)(]", '', (elink[5]))
                clean =   dirty[7:-1]
                url = clean
        else:
                url = urlresolver.resolve(url)
        meta = 0
        try:
             meta = getMeta(name,types)
        except:
             pass
        
        params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types, 'host':host}
        if meta == 0:
             addon.add_video_item(params, {'title':name}, img=thumb)
             liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.jpg", thumbnailImage=thumb)
        else:
             addon.add_video_item(params, meta, fanart=meta['backdrop_url'], img=meta['cover_url'])
             liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.jpg", thumbnailImage=meta['cover_url'])
             liz.setInfo('video',infoLabels=meta)
        
        xbmc.sleep(1000)
        
        xbmc.Player ().play(url, liz, False)
                

def GENRES():
        addDir('Action',base_url +'/index.php?genre=3','index',artwork + 'Icon_genre_Action.jpg','dir',False)
        addDir('Adventure',base_url +'/index.php?genre=13','index',artwork + 'Icon_genre_Adventure.jpg','dir',False)
        addDir('Animation',base_url +'/index.php?genre=6','index',artwork + 'Icon_genre_Animation.jpg','dir',False)
        addDir('Comedy',base_url +'/index.php?genre=1','index',artwork + 'Icon_genre_Comedy.jpg','dir',False)
        addDir('Drama',base_url +'/index.php?genre=2','index',artwork + 'Icon_genre_Drama.jpg','dir',False)
        addDir('Horror',base_url +'/index.php?genre=5','index',artwork + 'Icon_genre_Horror.jpg','dir',False)
        addDir('Sci-Fi',base_url +'/index.php?genre=4','index',artwork + 'Icon_genre_Sci-fi.jpg','dir',False)
        addDir('Thriller',base_url +'/index.php?genre=11','index',artwork + 'Icon_genre_Thriller.jpg','dir',False)
        addDir('Western',base_url +'/index.php?genre=12','index',artwork + 'Icon_genre_Western.jpg','dir',False)

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                
                url = base_url + '/index.php?search=' + search
                
                link = net.http_GET(url).content
                match=re.compile('<img src="(.+?)" width=".+?" height=".+?" border=".+?" /></a></div></td>\n                           \n                            <td width=".+?" valign=".+?" class=".+?"  align=".+?"><p><strong>(.+?): </strong></p>\n                                <p>(.+?)</p>\n                              <p><span class=".+?"><a href="/(.+?)">').findall(link)
                if len(match) > 0:
                        INDEX(url)
                else:
                        match=re.compile('<!--\nwindow.location = "(.+?)"\n//-->').findall(link)
                        if len(match) > 0:
                              if 'XXX' in str(match[0]):
                                   return
                                                
                              else:
                                   VIDEOLINKS(base_url + match[0],'')
                        else:
                                return
                        
def COLLECTIVESEARCH(name):
     search = name
     search = re.sub(' ','+', search)    
     url = base_url + '/index.php?search=' + search
     link = net.http_GET(url).content
     match=re.compile('<img src="(.+?)" width=".+?" height=".+?" border=".+?" /></a></div></td>\n                           \n                            <td width=".+?" valign=".+?" class=".+?"  align=".+?"><p><strong>(.+?): </strong></p>\n                                <p>(.+?)</p>\n                              <p><span class=".+?"><a href="/(.+?)">').findall(link)
     if len(match) > 0:
          INDEX(url)
     else:
          match=re.compile('<!--\nwindow.location = "(.+?)"\n//-->').findall(link)
          if len(match) > 0:
               if 'XXX' in str(match[0]):
                    return
                                                
               else:
                    VIDEOLINKS(base_url + match[0],'')
          else:
               return
                        
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()
elif mode=='index':
        print ""+url
        INDEX(url)   
elif mode=='videoLinks':
        print ""+url
        VIDEOLINKS(url,name)
elif mode=='genres':
        print ""+url
        GENRES()
elif mode=='resolve':
        print ""+url
        RESOLVE(name,host,url)
elif mode=='search':
        print ""+url
        SEARCH()
elif mode=='adultIndex':
        print ""+url
        ADULTINDEX(url)
elif mode=='collectiveSearch':
        print ""+url
        COLLECTIVESEARCH(name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

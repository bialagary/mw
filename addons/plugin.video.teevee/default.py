import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import sqlite3
import re
import os
import json,time
from BeautifulSoup import BeautifulSoup as bs
from resources.modules.teevee import *
import xbmcvfs

try:
    from addon.common.addon import Addon
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("TeeVee Import Failure", "Failed to import addon.common", "A component needed by TeeVee is missing on your system", "Please visit www.tvaddons.ag for support")

try:
    from metahandler import metahandlers
except:
    print 'Failed to import script.module.metahandler'
    xbmcgui.Dialog().ok("TeeVee Import Failure", "Failed to import addon.common", "A component needed by TeeVee is missing on your system", "Please visit www.tvaddons.ag for support")


# from dudehere.routines.scrapers import CommonScraper
# from dudehere.routines.plugin import Plugin
# Scraper = CommonScraper()
# resolved_url = Scraper.search_tvshow('The Walking Dead',1,1,year='2015')
# xbmc.Player().play(resolved_url)
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
my_addon = xbmcaddon.Addon()
params=urlparse.parse_qs(sys.argv[2][1:])


addonID=xbmcaddon.Addon().getAddonInfo("id")
db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)
db_path = os.path.join(db_dir, 'favourites.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db=sqlite3.connect(db_path)

addon = Addon('plugin.video.teevee', sys.argv)
AddonPath = addon.get_path()

  
IconPath = AddonPath + "/resources/icons/new/"


downloadPath = addon.get_setting('download_folder')

def icon_path(filename):
    return IconPath + filename


###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################



    



def get_links(url):
    domain='http://tvonline.tw'
    my_addon = xbmcaddon.Addon()
    black = unicode(my_addon.getSetting('source_blacklist'))
    if black!='':
        blacklist=black.split(',')
    else:
        blacklist=[] 
    if domain not in url:   
        url=domain + url

    html=read_url(url)
    soup=bs(html)

    tag=str(soup.find('div',{'id':'linkname'}))

    reg=re.compile("go_to\(\d+,'(.+?)'\)")

    links=list(re.findall(reg,tag))
    out=[]
    ind=0
    for link in links:
        for black in blacklist:
            if black in link :
                ind+=1
        if ind==0:
            out+=[link]
        ind=0
    return out

    
def get_month():
    import datetime
    now = datetime.datetime.now()
    out=[]
    for i in range(30):
        date=now - datetime.timedelta(hours=i*24)
        year=date.year
        day=date.day
        month=date.month
        name=date.strftime("%A")
        mnth=date.strftime("%B")
        out+=[[name,day,month,year,mnth]]
    return out

def sort_links(links):
    my_addon = xbmcaddon.Addon()
    sort=my_addon.getSetting('enable_sorting')
    black = unicode(my_addon.getSetting('source_blacklist'))
    blacklist=black.split(',')
    listout=[]
    if sort!='false':
        sorting=unicode(my_addon.getSetting('sort'))
        sort_list=sorting.split(',')

        for i in range(len(sort_list)):
            for j in range(len(links)):
                if sort_list[i] in links[j] and links[j] not in blacklist:
                    listout.append(links[j])
        for k in range(len(links)):
            
            if links[k] not in listout and links[k] not in blacklist:
                listout.append(links[k])
        return listout

    else:
        return links

#borrowed from 1Channel by tknorris and modified
def get_dbid(title, season='', episode='', year=''):
    video_type='episode'
    dbid = 0
    filter = ''
    # variable used to match title with closest len, if there is more than one match, the one with the closest title length is the winner,
    # The Middle and Malcolm in the Middle in the same library would still match the corret title. Starts at high value and lowers
    max_title_len_diff = 1000
    titleComp2 = re.sub('[^a-zA-Z0-9]+', '', title).lower()
    
    # if it'a a tvshow episode filter out all tvshows which contain said season and episode, then match tvshow title
    if video_type == 'episode':
        filter = '"filter": {"and":['
        if year: filter += '{"field": "year", "operator": "is", "value": "%s"},' % year
        filter += '{"field": "season", "operator": "is", "value": "%s"},' % season
        filter += '{"field": "episode", "operator": "is", "value": "%s"}]},' % episode
        json_string = '{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.GetEpisodes", "params": {%s "properties": ["showtitle"], "limits": {"end": 10000}}}' % (filter)
        result_key = "episodes"
        id_key = "episodeid"
        title_key = "showtitle"
    result = xbmc.executeJSONRPC(json_string)
    resultObj = json.loads(result)
    if not ('result' in resultObj and result_key in resultObj['result']): return None
    for item in resultObj['result'][result_key]:
        # converts titles to only alpha numeric, then compares smallest title to largest title, for example
        # 'Adventure Time' would match to 'Adventure tIME with FiNn and Jake_ (en) (4214)'
        titleComp1 = re.sub('[^a-zA-Z0-9]+', '', item[title_key]).lower()
        found_match = 0
        if len(titleComp1) > len(titleComp2):
            if titleComp2 in titleComp1: found_match = 1
        else:
            if titleComp1 in titleComp2: found_match = 1
        if found_match:
            title_len_diff = abs(len(titleComp1) - len(titleComp2))
            if title_len_diff <= max_title_len_diff:
                max_title_len_diff = title_len_diff
                if video_type == 'movie':
                    dbid = item[id_key]
                if video_type == 'episode':
                    dbid = item[id_key]
    if dbid:
        return dbid
    else:
        utils.log('Failed to recover dbid, type: %s, title: %s, season: %s, episode: %s' % (video_type, title, season, episode), xbmc.LOGDEBUG)
        return None

def sort_iw(links,sources):
    my_addon = xbmcaddon.Addon()
    sort=my_addon.getSetting('enable_sorting')
    black = unicode(my_addon.getSetting('source_blacklist'))
    blacklist=black.split(',')
    listout=[]
    hostout=[]
    listout2=[]
    hostout2=[]
    if sort!='false':
        sorting=unicode(my_addon.getSetting('sort'))
        sort_list=sorting.split(',')
        br=1
        b2=0
        for i in range(len(sort_list)):
            for j in range(len(links)):
                if sort_list[i] in sources[j] and links[j] not in blacklist:
                    listout.append(links[j])
                    hostout.append('%s. '%(br)+sources[j])
                    br+=1
        for k in range(len(links)):
            
            if links[k] not in listout and links[k] not in blacklist:
                listout.append(links[k])
                hostout.append('%s. '%(b2+br)+sources[k])
                b2+=1
        return listout,hostout

        
        

    else:
        return links,sources


#Notify function from Eldorado's PFTV
def Notify(typeq, box_title, message, times='', line2='', line3=''):
     if box_title == '':
          box_title='TeeVee Notification'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= icon_path('icon.png')
          addon.show_small_popup(title=box_title, msg=message, delay=int(times), image=smallicon)
     elif typeq == 'big':
          addon.show_ok_dialog(message, title=box_title)
     else:
          addon.show_ok_dialog(message, title=box_title)
def add_favourite_show(name, link, thumb):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_shows (Link TEXT,Title TEXT, Thumb TEXT )")    
        db.commit()
        cur.execute("SELECT Title,Link,Thumb from Favourite_shows WHERE Title = ? AND Link=? and Thumb=?", (name,link,thumb))
        data=cur.fetchall()
        if len(data)!=0:
            Notify('small', 'Favourite Already Exists', name + ' already exists in your TeeVee favourites','')
            return
        
        cur.execute("INSERT INTO Favourite_shows(Link,Title, Thumb) VALUES (?,?, ?);",(link,name,thumb))
        db.commit()
        cur.close()
    Notify('small', 'Added to favourites', name + ' added to your TeeVee favourites','')
    return



def get_favourite_shows():
    with db:
        cur = db.cursor()
        cur.execute("begin")   
        cur.execute("create table if not exists Favourite_shows (Title TEXT, Link TEXT, Thumb TEXT)")    
        db.commit()  
        cur.execute("SELECT Title,Link,Thumb FROM Favourite_shows")
        rows = cur.fetchall()
        cur.close()
        favs=[]
        for i in range (len(rows)):
            folder=rows[i]
            favs+=[folder]
    return favs


def add_search_query(query,type):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit()
        cur.execute("INSERT INTO Search_history(type,query) VALUES (?,?);",(type,query))
        db.commit()
        cur.close()
    return
def get_search_history(type):
    with db:
        cur = db.cursor()
        cur.execute("begin")    
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit() 
        cur.execute("SELECT query FROM Search_history WHERE type = ?",(type,))
        rows = cur.fetchall()
        cur.close()
        his=[]
        for i in range (len(rows)):
            folder=rows[i][0]
            his+=[folder]
    return his
def delete_history(type):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Search_history WHERE type = ?",(type,))
    db.commit()
    cur.close()

def delete_all_tv_favs():
    with db:
        cur = db.cursor()
        cur.execute("drop table if exists Favourite_shows")
        cur.close()
    return


def remove_tv_fav(title,link):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_shows WHERE Title = ? AND Link = ?",(title,link))
    db.commit()
    cur.close()



def add_tv_item(type,link,show_title,season,episode,meta=None,totalitems=0,iwatch=None):
    seas=str(season.zfill(2))
    ep=str(episode.zfill(2))
    title='%s S%sE%s'%(show_title,seas,ep)
    try:
        down_uri = build_url({'mode': 'download', 'title':title,'url':link, 'type':type, 'thumb':meta['cover_url']})

    except:
        down_uri = build_url({'mode': 'download', 'title':title.encode('ascii','ignore'),'url':link, 'type':type, 'thumb':meta['cover_url']})

    title='%s %sx%s'%(show_title,season,episode)
    if type=='season':
        
        meta['title']='%sx%s .  %s'%(season,episode,meta['title'])
    elif 'new' in type:
        meta['title']='%s %sx%s'%(show_title,season,episode)
    contextMenuItems=[('Episode Information', 'XBMC.Action(Info)'),
                        ('Download','RunPlugin(%s)'%down_uri)]
    if type!='new_iw':type='ep'

    addon.add_video_item({'type': type,'url': link,'title': title, 'season':season, 'episode':episode,'iwatch':iwatch}, meta,contextmenu_items=contextMenuItems, context_replace=False,img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=totalitems)

def make_art(meta):
    # default fanart to theme fanart
    art_dict = {'thumb': '', 'poster': '', 'fanart': '', 'banner': ''}

    # set the thumb & cover to the poster if it exists
    if 'cover_url' in meta:
        art_dict['thumb'] = meta['cover_url']
        art_dict['poster'] = meta['cover_url']

    

    # override the fanart with metadata if fanart is on and it exists and isn't blank
    if 'backdrop_url' in meta and meta['backdrop_url']: art_dict['fanart'] = meta['backdrop_url']
    if 'banner_url' in meta: art_dict['banner'] = meta['banner_url']
    return art_dict




###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
addon = Addon('plugin.video.teevee', sys.argv)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

play = addon.queries.get('play', '')






if play:
    resolved=None
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['url'][0]
    type=dicti['type'][0]
    title=dicti['title'][0]
    season=dicti['season'][0]
    episode=dicti['episode'][0]
    if type=='ep':
            links=get_links(link)
            links=sort_links(links)
            sources=get_sources(links)


    elif type=='new_iw':
        links,sources=get_iwatch_links(link)
        links,sources=sort_iw(links,sources)

    
        # if type=='ep':
        #     links=get_links(link)
        #     links=sort_links(links)
        #     sources=get_sources(links)


        # elif type=='new_iw':
        #     links,sources=get_iwatch_links(link)
        #     links,sources=sort_iw(links,sources)


    autoplay = my_addon.getSetting('autoplay')
    if autoplay=='false':

        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a source:', sources)
        
        if index>-1:
            url=links[index]
            if 'iwatch'in url:
                url=resolve_iwatch(url)
            
            
            import urlresolver
            resolved=urlresolver.resolve(url)

            if resolved:
                if my_addon.getSetting('axel') != 'false':
                    download_name = title
                    import axelproxy as proxy
                    axelhelper = proxy.ProxyHelper()
                    resolved, download_id = axelhelper.create_proxy_url(resolved, name=download_name)
                
                addon.resolve_url(resolved)
            else:
                Notify('small', 'No stream', "Couldn't resolve item",'')

    else:
        import urlresolver
        for i in range(len(links)):
            url=links[i]
            if 'iwatch'in links[i]:
                url=resolve_iwatch(links[i])
            
            resolved=urlresolver.resolve(url)

            if resolved:
                if my_addon.getSetting('axel') != 'false':
                    download_name = title
                    import axelproxy as proxy
                    axelhelper = proxy.ProxyHelper()
                    resolved, download_id = axelhelper.create_proxy_url(resolved, name=download_name)
                
                addon.resolve_url(resolved)
                break
        if not resolved:
            Notify('small', 'No stream', "Couldn't resolve item",'')

           


    



###########################################################################################################################################################
###########################################################################################################################################################
#TV
###########################################################################################################################################################


elif mode is None :
    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'new_tv', 'foldername': 'shows', 'page':'1'})
    li = xbmcgui.ListItem('New Episodes', iconImage=icon_path('Latest_Added.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    my_addon = xbmcaddon.Addon()
    calendar = my_addon.getSetting('enable_calendar')

    if calendar!='false':
        url = build_url({'mode': 'open_calendar', 'foldername': 'shows'})
        li = xbmcgui.ListItem('TV Schedule', iconImage=icon_path('Calendar.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)


    url = build_url({'mode': 'latest_tv', 'foldername': 'shows' , 'page':'1'})
    li = xbmcgui.ListItem('Lastest Added', iconImage=icon_path('Latest_Added.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'popular_today', 'foldername': 'shows','page': 1})
    li = xbmcgui.ListItem('Popular today', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'most_popular', 'foldername': 'shows', 'page': 1})
    li = xbmcgui.ListItem('Most popular', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'az_shows', 'foldername': 'shows'})
    li = xbmcgui.ListItem('A-Z', iconImage=icon_path('AZ.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'genres_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Genres', iconImage=icon_path('Genre.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'downloader'})
    li = xbmcgui.ListItem('Downloads', iconImage=icon_path('Downloads.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    


    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='open_calendar':
    days=get_month()
    for day in days:
        d=day[1]
        m=day[2]
        y=day[3]
        mnth=day[4]
        name=day[0]+', %s %s '%(d,mnth)

        url = build_url({'mode': 'open_day', 'day':d, 'month':m, 'year':y,'page':'1'})
        li = xbmcgui.ListItem(name, iconImage=icon_path('Calendar.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_day':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    day=dicti['day'][0]
    month=dicti['month'][0]
    year=dicti['year'][0]
    page=int(params['page'][0])
    meta_setting = my_addon.getSetting('tv_metadata')
    eps=get_episodes_calendar(day,month,year)
    shows=eps
    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        item=shows[i]
        show_title=item[3]
        season=item[1]
        episode=item[2]
        url=item[0]+'s%se%s/'%(season,episode)
            
        
        if url!='0':
            meta=None
            if meta_setting!='false':
                imdb_id=''
                metaget=metahandlers.MetaData()             
                meta=metaget.get_episode_meta(show_title, imdb_id, season.lstrip("0"), episode.lstrip("0"))
                
                meta['title']='%s %sx%s %s'%(show_title,season,episode,meta['title'].encode('ascii','ignore'))
                
            if meta==None:
                meta={}
                title='%s: %sx%s'%(show_title,season,episode)
                meta['title']=title
                meta['name']=title
                meta['tvshowtitle']=show_title
                meta['season']=season
                meta['episode']=episode
                meta['cover_url']=icon_path('TV_Shows.png')
                meta['backdrop_url']=None

            if meta['cover_url']=='':
                meta['cover_url']=icon_path('TV_Shows.png')

            add_tv_item('new_iw',url,show_title,season,episode,meta=meta,totalitems=total)

    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_day', 'day':day,'month':month,'year':year, 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='new_tv':
    eps=new_episodes()
    shows=eps
    page=int(params['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)

    for i in range(first,total):
        item=eps[i]
        url=item[0]
        show_title=item[1]
        season=item[2]
        episode=item[3]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_episode_meta(show_title, imdb_id, season.lstrip("0"), episode.lstrip("0"))
            
            meta['title']='%s %sx%s %s'%(show_title,season,episode,meta['title'].encode('ascii','ignore'))
            
        if meta==None:
            meta={}
            title='%s: %sx%s'%(show_title,season,episode)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['season']=season
            meta['episode']=episode
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        add_tv_item('new',url,show_title,season,episode,meta=meta,totalitems=total)

    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'new_tv', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



    

elif mode[0]=='latest_tv':
    shows=latest_added()
    page=int(params['page'][0])

    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})

        
        context=[('Show Information', 'XBMC.Action(Info)'), ('Add to TeeVee favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title, }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'latest_tv', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='popular_today':
    shows=popular_today()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })

        
        context=[('Show Information', 'XBMC.Action(Info)'), ('Add to TeeVee favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None


        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title,  }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'popular_today', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='most_popular':
    shows=most_popular()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})

        
        context=[('Show Information', 'XBMC.Action(Info)'), ('Add to TeeVee favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'most_popular', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


    
  


elif mode[0]=='az_shows':
    letter=get_letters()

    for i in range(len(letter)):
        url = build_url({'mode': 'open_letter', 'letter':letter[i][0],'page':'1'})
        li = xbmcgui.ListItem(letter[i][1], iconImage=icon_path('%s.png'%(letter[i][1])))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

    
elif mode[0]=='genres_tv':
    genre=get_genres()
    for i in range(len(genre)):
        url = build_url({'mode': 'open_letter', 'letter':genre[i][0],'page':'1'})
        li = xbmcgui.ListItem(genre[i][1], iconImage=icon_path('Genre.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    show=dicti['title'][0]

    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    imdb_id,seasons=get_seasons(url)

    total=len(seasons)
    if meta_setting!='false':
        ses=[]
        for item in seasons:
            
            ses+=[int(item[1])]
        
        metaget=metahandlers.MetaData()             
        meta=metaget.get_seasons(show, imdb_id,ses)
    else:
        meta=[]
        for i in range(total):
            meta.append({})
            meta[i]['season']=seasons[i][1]
            meta[i]['backdrop_url']=''
            meta[i]['cover_url']=''

    for i in range(len(meta)):
        metas=meta[i]
        metas['title'] = 'Season ' + str(metas['season'])
        addon.add_directory({'mode': 'open_season', 'url': seasons[i][0],'num':seasons[i][1], 'show': show }, metas, img=metas['cover_url'], fanart=metas['backdrop_url'], total_items=total)
    xbmcplugin.endOfDirectory(addon_handle)

            
        


    
elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    show=dicti['show'][0]
    num=dicti['num'][0]
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    imdb_id,episodes=get_episodes(url,num)
    total=len(episodes)
    for item in episodes:
        show_title=show
        url=item[0]
        ep_title=item[1]
        season=item[2]
        episode=item[3]
        meta=None
        if meta_setting!='false':
            
            metaget=metahandlers.MetaData()             
            meta=metaget.get_episode_meta(show_title, imdb_id, season.lstrip("0"), episode.lstrip("0"))
            
            meta['title']=meta['title'].encode('ascii','ignore')
            if meta['title']=='':
                meta['title']=ep_title
            
        if meta==None:
            meta={}
            meta['imdb_id']=imdb_id
            meta['title']=ep_title
            meta['name']=''
            meta['tvshowtitle']=show_title
            meta['season']=season
            meta['episode']=episode
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        add_tv_item('season',url,show_title,season,episode,meta=meta,totalitems=total)
    xbmcplugin.endOfDirectory(addon_handle)


    

elif mode[0]=='open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=get_shows_letter(letter)

    page=int(params['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)

    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })

        
        context=[('Show Information', 'XBMC.Action(Info)'), ('Add to TeeVee favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_letter','letter':letter, 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

    


elif mode[0]=='add_tv_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    name=dicti['show'][0]
    link=dicti['link'][0]
    thumb=dicti['year'][0]

    add_favourite_show(name,link,thumb)















elif mode[0]=='search_tv_history':
    url = build_url({'mode': 'search_tv', 'foldername': 'search'})
    li = xbmcgui.ListItem('[COLOR green]New Search[/COLOR]', iconImage=icon_path('Search.png'))
    
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    his=get_search_history('tv')
    for i in range(len(his)):
        url = build_url({'mode': 'open_tv_search', 'query': his[i]})
        li = xbmcgui.ListItem(his[i], iconImage=icon_path('Search.png'))
        del_url = build_url({'mode': 'del_his_tv'})
        li.addContextMenuItems([('Erase search history','RunPlugin(%s)'%del_url)])
    
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='search_tv':
    keyboard = xbmc.Keyboard('', 'Search TV Shows', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        add_search_query(query,'tv')
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(1.3)

        url = build_url({'mode': 'open_tv_search', 'query':query})
        builtin = 'Container.Update(%s)' % (url)
        xbmc.executebuiltin(builtin)




elif mode[0]=='open_tv_search':
        dicti=urlparse.parse_qs(sys.argv[2][1:])
        query=dicti['query'][0]
        shows=search(query)
        total=len(shows)
        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('tv_metadata')

        for i in range(total):
            show=shows[i]
            url=show[0]
            show_title=show[1]
            show_year=show[2]
            try:
                fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
            except:
                fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })

        
            context=[('Show Information', 'XBMC.Action(Info)'), ('Add to TeeVee favourites','RunPlugin(%s)'%fav_uri)]
            meta=None
            if meta_setting!='false':
                imdb_id=get_imdb(url)
                metaget=metahandlers.MetaData()             
                meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
                
                meta['title']=meta['title'].encode('ascii','ignore')
                title='%s (%s)'%(show_title,show_year)
                meta['title']=title
                
            if meta==None:
                meta={}
                title='%s (%s)'%(show_title,show_year)
                meta['title']=title
                meta['name']=title
                meta['tvshowtitle']=show_title
                meta['cover_url']=icon_path('TV_Shows.png')
                meta['backdrop_url']=None

            if meta['cover_url']=='':
                meta['cover_url']=icon_path('TV_Shows.png')

            addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
        xbmcplugin.endOfDirectory(addon_handle)

###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


    
elif mode[0]=='fav_tv':
    shows=get_favourite_shows()

    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    total=len(shows)
    for i in range(total):
        show=shows[i]
        url=show[1]
        show_title=show[0]
        show_year=show[2]
        try:
            del_uri = build_url({'mode': 'del_show_fav', 'title':show_title,  'link':url})

        except:
            del_uri = build_url({'mode': 'del_show_fav', 'title':show_title.encode('ascii','ignore'),'link':url})

        del_all = build_url({'mode': 'del_tv_all'})

    
        
        context=[('Show Information', 'XBMC.Action(Info)'),
                    ('Remove from TeeVee favourites','RunPlugin(%s)'%del_uri),
                    ('Remove all TeeVee favourites','RunPlugin(%s)'%del_all)]
        meta=None
        if meta_setting!='false':
            if url[0]!='/' and 'http' not in url:
                url='/'+url
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title, }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='del_show_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    link=dicti['link'][0] 
    remove_tv_fav(title,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_tv_all':
    delete_all_tv_favs()
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_his_tv':
    delete_history('tv')
    xbmc.executebuiltin("Container.Refresh")


elif mode[0]=='download':

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['url'][0]
    type=dicti['type'][0]
    title=dicti['title'][0]
    sort = my_addon.getSetting('down_sort')

    if type!='new_iw':
            links=get_links(link)
            if sort !='false':
                links=sort_links(links)
            sources=get_sources(links)


    elif type=='new_iw':
        links,sources=get_iwatch_links(link)
        if sort !='false':
            links,sources=sort_iw(links,sources)

    image=params['thumb'][0]    

   

    dialog = xbmcgui.Dialog()
    index = dialog.select('Choose a download source:', sources)
    
    if index>-1:
        import resources.modules.downloader as downloader
        linky=links[index]
        if 'iwatch' in linky:
            linky=resolve_iwatch(linky)
        downloader.addDownload(title,linky,image)
            
        
    



elif mode[0] == 'downloader':
    import resources.modules.downloader as downloader
    downloader.downloader()

elif mode[0] == 'addDownload':
    name,url,image=params['name'][0],params['url'][0],params['thumb'][0]
    import resources.modules.downloader as downloader
    downloader.addDownload(name,url,image)

elif mode[0] == 'removeDownload':
    url=params['url'][0]
    import resources.modules.downloader as downloader
    downloader.removeDownload(url)

elif mode[0] == 'startDownload':
    import resources.modules.downloader as downloader
    downloader.startDownload()

elif mode[0] == 'startDownloadThread':
    import resources.modules.downloader as downloader
    downloader.startDownloadThread()

elif mode[0] == 'stopDownload':
    import resources.modules.downloader as downloader
    downloader.stopDownload()

elif mode[0] == 'statusDownload':
    import resources.modules.downloader as downloader
    downloader.statusDownload()
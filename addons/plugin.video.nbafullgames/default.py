from __future__ import unicode_literals
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon, xbmcvfs, os
from addon.common.addon import Addon
from resources.lib.nbahd import *
from resources.lib.nbacom import *
from resources.lib.nbayt import *

settings = xbmcaddon.Addon( id = 'plugin.video.nbafullgames' )
addonfolder=settings.getAddonInfo( 'path' )
artfolder=addonfolder + '/resources/media/'


full_thumb= artfolder + 'nba_full_games.jpg'

fanartt= addonfolder + '/fanart.jpg'

addon = Addon('plugin.video.nbafullgames', sys.argv)
AddonPath = addon.get_path()

  



def icon_path(filename):
    return artfolder + filename


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])



xbmcplugin.setContent(addon_handle, 'movies')
xbmcplugin.setPluginFanart(addon_handle, fanartt)


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)



if mode is None:


    url = build_url({'mode': 'games', 'foldername': 'Most Recent', 'page':'first','date':'http://nbahd.com/'})
    li = xbmcgui.ListItem('Games', iconImage=icon_path('nba_games.jpg'))
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'teams', 'foldername': 'Teams'})
    li = xbmcgui.ListItem('Teams', iconImage=icon_path('nba_teams.jpg'))
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'nbacom'})
    li = xbmcgui.ListItem('NBA.com', iconImage=icon_path('nba_nbacom.jpg'))
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'yt_channels'})
    li = xbmcgui.ListItem('NBA on Youtube', iconImage=icon_path('nba_youtube.jpg'))
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    
   
    url = build_url({'mode': 'live_games'})
    li = xbmcgui.ListItem('Live Games ([COLOR orange]BETA[/COLOR])', iconImage=icon_path('nba_games.jpg'))
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    for i in range(20):
        try:
            if (addon.get_setting('enable_favourite')!='false'):
                team_list=get_teams()
                ind=int(addon.get_setting('favourite_team'))
                fav = team_list[ind][1]
                game,np = get_games(fav)
                game=game[0]

                title=game[0].encode('ascii','ignore')

                url = build_url({'mode': 'game', 'foldername': '%s'%title, 'link' : '%s'%game[1], 'img': '%s'%(game[2])})
                li = xbmcgui.ListItem('%s'%game[0], iconImage='%s'%game[2])
                li.setArt({ 'fanart':'%s'%fanartt})

                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li,isFolder=True)
                break
        except:
            continue


    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='games':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    date=dicti['date'][0]
    
    try:
        page=dicti['page'][0]
    except:
        page=0
    
    game_list,next_page=get_games(date)
    
    for i in range(len(game_list)):
        title=game_list[i][0].encode('ascii','ignore')
        try:
            thumb = urllib.quote(game_list[i][2])
        except:
            thumb = ''
        url = build_url({'mode': 'game', 'foldername': '%s'%title, 'link' : '%s'%game_list[i][1].encode('ascii','ignore'), 'img': '%s'%thumb})
        li = xbmcgui.ListItem('%s'%game_list[i][0], iconImage='%s'%game_list[i][2])
        li.setArt({ 'fanart':'%s'%fanartt})

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
        

    
    if next_page!='0':    
        url = build_url({'mode': 'games', 'foldername': 'Next Page >', 'date' : '%s'%next_page})
        li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='game':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    game=dicti['foldername'][0]
    img=dicti['img'][0]
    
    parts=get_parts(link)
    i=0
    for part in parts:
        i+=1
        url = build_url({'mode': 'open_part','url': part[1], 'img':img, 'help':link})
        download_url = build_url({'mode': 'download_part','url': part[1], 'img':part[2], 'help':link, 'part':i})

        li = xbmcgui.ListItem(part[0], iconImage=part[2])
        li.addContextMenuItems([('Download video','RunPlugin(%s)'%download_url)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

   
    xbmcplugin.endOfDirectory(addon_handle)

    

elif mode[0]=='open_part':
    url=args['url'][0]
    img=args['img'][0]
    help=args['help'][0]
    title=get_title(help)
    try:
        link,resolved=get_link_hd(url)
        if not resolved:
            link=resolve_nbahd(link)
        li = xbmcgui.ListItem(title, iconImage=img)
        li.setThumbnailImage(img)
        xbmc.Player().play(listitem=li,item=link)
    except:
        pass

elif mode[0]=='download_part':
    url=args['url'][0]
    img=args['img'][0]
    part=args['part'][0]
    help=args['help'][0]
    name=get_title(help)
    url,resolved=get_link_hd(url)
    if not resolved:
        url=resolve_nbahd(url)
    desty = addon.get_setting('download_folder')
    if not xbmcvfs.exists(desty):
        xbmcvfs.mkdir(desty)
    name = name + ' Part %s '%(part)
    title=name 
    name=re.sub('[^-a-zA-Z0-9_.() ]+', '', name)
    name=name.rstrip('.')
    ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:]
    if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg', 'mp3']: ext = 'mp4'
    filename = name + '.' + ext

    dest = os.path.join(desty, filename)
    content = int(urllib.urlopen(url).info()['Content-Length'])
    size = 1024 * 1024
    mb   = content / (1024 * 1024)
    if xbmcgui.Dialog().yesno('NBA Full Games - Confirm Download', filename, 'Total file size is %dMB' % mb, 'Continue with download?', 'Continue',  'Cancel') == 0:
      
        import SimpleDownloader as downloader
        downloader = downloader.SimpleDownloader()
        params = { "url": url, "download_path": desty, "Title": title }
        downloader.download(filename, params)



    
elif mode[0]=='open_option':
    url=args['url'][0]
    img=args['img'][0]
    help=args['help'][0]
    title=get_title(help)
    url=url.replace('temporarylink.net','moevideo.net')
    link,need=getlink_nbahd(url)
    if need:
        try:
            import urlresolver
            link=urlresolver.resolve(link)
        except:
            import YDStreamExtractor
            YDStreamExtractor.disableDASHVideo(True) 
            vid = YDStreamExtractor.getVideoInfo(link,quality=1) 
            link = vid.streamURL()

    li = xbmcgui.ListItem(title, iconImage=img)
    li.setThumbnailImage(img)
    xbmc.Player().play(listitem=li,item=link)
    


elif mode[0]=='teams':
    team_list=get_teams()
    for i in range(len(team_list)):
        link=team_list[i][1]
        name=team_list[i][0]
        img=team_list[i][2]

        url = build_url({'mode': 'games', 'foldername': '%s'%name, 'date' : '%s'%link})
        li = xbmcgui.ListItem('%s'%name, iconImage=img)
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='nbacom':
    categs=[['NBA Video (All feeds)','http://searchapp2.nba.com/nba-search/query.jsp?section=channels%2F*%7Cgames%2F*%7Cflip_video_diaries%7Cfiba&sort=recent&hide=true&type=advvideo&npp=15&start='],
            ['Top Plays','http://searchapp2.nba.com/nba-search/query.jsp?section=channels%2Ftop_plays&sort=recent&hide=true&type=advvideo&npp=15&start='],
            ['Highlights','http://searchapp2.nba.com/nba-search/query.jsp?section=games%2F*%7Cchannels%2Fplayoffs&sort=recent&hide=true&type=advvideo&npp=15&start='],
            
            ['Editors Picks','http://www.nba.com/rss/editorspick.rss'],
            ['NBA TV Top 10','http://www.nba.com/nbatvtop10/rss.xml'],
            ['Play Of The Day','http://www.nba.com/playoftheday/rss.xml'],
            ['Dunk of The Night','http://www.nba.com/dunkofthenight/rss.xml'],
            ['Assist Of The Night','http://www.nba.com/assistofthenight/rss.xml']]
    

    for i in range(len(categs)):
        a=categs[i][0]
        if a=='Top Plays' or a=='Highlights' or a=='NBA Video (All feeds)':
            url = build_url({'mode': 'nbacom2', 'link':'%s'%categs[i][1], 'page':1})
            li = xbmcgui.ListItem('%s'%categs[i][0], iconImage=icon_path('nba_nbacom.jpg'))
            li.setArt({ 'fanart':'%s'%fanartt})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
        
        else:
            url = build_url({'mode': 'tst', 'link':'%s'%categs[i][1]})
            li = xbmcgui.ListItem('%s'%categs[i][0], iconImage=icon_path('nba_nbacom.jpg'))
            li.setArt({ 'fanart':'%s'%fanartt})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='nbacom2':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    page=dicti['page'][0]

    get_videos_nbacom2(link,page)






elif mode[0]=='tst':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    list=get_nbacom_rss(link)

    for i in range(len(list)):
        
        url = build_url({'mode': 'open_nbacom', 'link':'%s'%list[i][0] ,'foldername': 'nbacom','title':'%s'%list[i][1]})
        li = xbmcgui.ListItem('%s'%list[i][1], iconImage=icon_path('nba_nbacom.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_nbacom':
    #        url = build_url({'mode': 'open_nbacom', 'link':'%s'%link ,'foldername': 'nbacom2','title':'%s'%title,'thumb':'%s'%thumb, 'desc':'%s'%desc})

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    title=dicti['title'][0]
    fold=dicti['foldername'][0]

    if fold=='nbacom2':

        thumb=dicti['thumb'][0]
        desc=dicti['desc'][0]
        link=get_nbacom_video(link)
        li = xbmcgui.ListItem('%s'%title)
        li.setInfo('video', { 'title': '%s'%title, 'plot':'%s'%desc} )
        li.setArt({ 'fanart':'%s'%fanartt})
        li.setThumbnailImage(thumb)
        xbmc.Player().play(item=link, listitem=li)
    else:

        link=get_nbacom_video(link)
        li = xbmcgui.ListItem('%s'%title)
        li.setInfo('video', { 'title': '%s'%title} )
        li.setArt({ 'fanart':'%s'%fanartt})
        li.setThumbnailImage(icon_path('nba_nbacom.jpg'))
        xbmc.Player().play(item=link, listitem=li)


elif mode[0]=='yt_channels':
    channels=[['BBallBreakdown','UUSpvjDk06HLxBaw8sZw7SkA','https://yt3.ggpht.com/-VRcps3w2W1k/AAAAAAAAAAI/AAAAAAAAAAA/mTE7JwJv2K4/s100-c-k-no/photo.jpg']]

    reg1='name="(.+?)"'
    pat1=re.compile(reg1)
    reg2='id="(.+?)"'
    pat2=re.compile(reg2)

    reg3='img="(.+?)"'
    pat3=re.compile(reg3)


    urll='http://pastebin.com/raw.php?i=S2rrmeqN'
    


    a=urllib2.urlopen(urll)
    html=a.read().decode('utf-8')
    channels=html.split('#==#')

    url = build_url({'mode': 'yt', 'foldername': 'NBA.com', 'page':'1'})
    li = xbmcgui.ListItem('NBA on Youtube', iconImage='http://a448.phobos.apple.com/us/r30/Purple5/v4/63/b1/70/63b170c6-bb0d-a39c-62ae-c14d730206b3/mzl.hbbvswbw.png')
    li.setArt({ 'fanart':'%s'%fanartt})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    for i in range(len(channels)):
        try:

            name=re.findall(pat1,channels[i])[0]
            id=re.findall(pat2,channels[i])[0]
            img=re.findall(pat3,channels[i])[0]

            url = build_url({'mode': 'open_channel', 'foldername': 'channel', 'id':'%s'%id, 'page':'1'})
            li = xbmcgui.ListItem('%s'%name, iconImage='%s'%img)
            li.setArt({ 'fanart':'%s'%fanartt})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
        except:
            pass
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_channel':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    playy_id=dicti['id'][0]
    page=dicti['page'][0]


    try:
        playlist=dicti['playlist'][0]
        if playlist=='yes':
            playlista=True
    except:
        playlista=False

    
    if not playlista:

        url = build_url({'mode': 'open_playlists2', 'id':'%s'%playy_id, 'page':'1'})
        li = xbmcgui.ListItem('[COLOR yellow]Playlists [/COLOR]',iconImage=icon_path('nba_playlists.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    if playlista:
        play_id=dicti['id'][0]
    else:
        play_id=playy_id
    game_list=get_latest_from_youtube(play_id,page)
    next_page=game_list[0]
    for i in range(1,len(game_list)):
        title=game_list[i][0].encode('utf8').decode('ascii','ignore')
        video_id=game_list[i][1]
        thumb=game_list[i][2]
        desc=game_list[i][3]
        link='plugin://plugin.video.youtube/?action=play_video&videoid='+video_id
        
        uri = build_url({'mode': 'play_yt', 'foldername': '%s'%title, 'link' : '%s'%video_id})

        li = xbmcgui.ListItem('%s'%title, iconImage=thumb)
        li.setArt({ 'fanart':'%s'%fanartt})
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)

    if next_page!='1':
        uri = build_url({'mode': 'yt', 'foldername': 'Next Page', 'page' : '%s'%next_page})

        li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='yt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]


    try:
        playlist=dicti['playlist'][0]
        if playlist=='yes':
            playlista=True
    except:
        playlista=False

    
    if not playlista:

        url = build_url({'mode': 'open_playlists',  'page':'1'})
        li = xbmcgui.ListItem('[COLOR yellow]Playlists [/COLOR]',iconImage=icon_path('nba_playlists.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    if playlista:
        play_id=dicti['id'][0]
    else:
        play_id='UUWJ2lWNubArHWmf3FIHbfcQ'
    game_list=get_latest_from_youtube(play_id,page)
    next_page=game_list[0]
    for i in range(1,len(game_list)):
        title=game_list[i][0].encode('utf8').decode('ascii','ignore')
        video_id=game_list[i][1]
        thumb=game_list[i][2]
        desc=game_list[i][3]
        link='plugin://plugin.video.youtube/?action=play_video&videoid='+video_id
        
        uri = build_url({'mode': 'play_yt', 'foldername': '%s'%title, 'link' : '%s'%video_id})

        li = xbmcgui.ListItem('%s'%title, iconImage=thumb)
        li.setArt({ 'fanart':'%s'%fanartt})
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)

    if next_page!='1':
        uri = build_url({'mode': 'yt', 'foldername': 'Next Page', 'page' : '%s'%next_page})

        li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='play_yt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link='plugin://plugin.video.youtube/?action=play_video&videoid='+dicti['link'][0]
    xbmc.executebuiltin('PlayMedia(%s)'%link)

elif mode[0]=='open_playlists':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    
    page=dicti['page'][0]
    
    playlists=get_playlists(page)

    next_page=playlists[0]
    for i in range (1,len(playlists)):
        id=playlists[i][0]
        name=playlists[i][1]
        thumb=playlists[i][2]


        url = build_url({'mode': 'yt', 'id': '%s'%id, 'page':'1', 'playlist':'yes'})
        li = xbmcgui.ListItem('%s'%name, iconImage='%s'%thumb)
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,isFolder=True)


    if next_page!='1':
        
        uri = build_url({'mode': 'open_playlists', 'id': '%s'%id, 'page' : '%s'%next_page ,'playlist':'yes'})
      

        li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_playlists2':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    
    page=dicti['page'][0]
    id=dicti['id'][0]
    
    playlists=get_playlists2(id,page)

    next_page=playlists[0]
    for i in range (1,len(playlists)):
        id=playlists[i][0]
        name=playlists[i][1]
        thumb=playlists[i][2]


        url = build_url({'mode': 'yt', 'id': '%s'%id, 'page':'1', 'playlist':'yes'})
        li = xbmcgui.ListItem('%s'%name, iconImage='%s'%thumb)
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,isFolder=True)


    if next_page!='1':
        
        uri = build_url({'mode': 'open_playlists2', 'id': '%s'%id, 'page' : '%s'%next_page ,'playlist':'yes'})
      

        li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='live_games':
    if (addon.get_setting('live_source')=='1'):
        from resources.lib import atdhe
        events = atdhe.atdhe().get_basketball_events()
    else:
        from resources.lib import zunox
        events = zunox.zunox().get_basketball_events()
    for event in events:
        url = build_url({'mode': 'open_live', 'title': event[1], 'url' : event[0]})
        li = xbmcgui.ListItem(event[1])
        li.setArt({ 'fanart':'%s'%fanartt})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='open_live':
    title = args['title'][0]
    url = args['url'][0]
    li = xbmcgui.ListItem(title)
    import liveresolver
    resolved = liveresolver.resolve(url)
    xbmc.Player().play(item=resolved, listitem=li)


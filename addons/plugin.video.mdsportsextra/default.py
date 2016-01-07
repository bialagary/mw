import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,base64
import urlresolver
import datetime
import requests
from addon.common.addon import Addon
from addon.common.net import Net


#Baeble Music - By Mucky Duck (09/2015)

addon_id='plugin.video.mdsportsextra'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl = 'http://www.football.co.uk'
baseurl2 = 'http://www.football365.com'
baseurl3 = 'http://www.footytube.com'
baseurl4 = 'http://www.soccerbase.com'
baseurl5 = 'http://goal-best.com'
baseurl6 = 'http://openfootball.github.io'
baseurl7 = 'http://livescore.football-data.co.uk'  #http://football-data.mx-api.enetscores.com
baseurl8 = 'http://www.european-football-statistics.co.uk'
baseurl9 = 'https://github.com'
baseurl10 ='http://okgoals.com/'
baseurl11 = 'http://liveonsat.com'
baseurl12 = 'http://www.scorespro.com'
baseurl13 = 'http://www.xscores.com'
baseurl14 = 'http://feeds.thescore.com/'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
net = Net()
sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()
import utils




def CAT():
        addDir('[COLOR white]Live[/COLOR]','http://m.liveonlinetv247.info/sports-channels.php',99,icon,fanart,'')
        addDir('[COLOR white]Live Scores[/COLOR]',baseurl12+'/rss/live-soccer.xml',10,icon,fanart,'')
        addDir('[COLOR white]Highlights[/COLOR]',baseurl10,23,icon,fanart,'')
        addDir('[COLOR white]Results[/COLOR]',baseurl4+'/results/home.sd',5,art+'results.png',fanart,'')
        addDir('[COLOR white]Tables[/COLOR]',baseurl+'/league-tables/',2,art+'tables.png',fanart,'')
        addDir('[COLOR white]News Feed[/COLOR]',baseurl2+'/feed',6,art+'news.png',fanart,'')
        addDir('[COLOR white]News Vids[/COLOR]',baseurl3+'/widgets/fplayer.php?vwidth=300&pheight=185&hw=1',1,art+'news_videos.png',fanart,'')
        addDir('[COLOR white]Goals Of The Week[/COLOR]',baseurl5,7,art+'goals_week.png',fanart,'')
        #addDir('[COLOR white]Goal-Best.com[/COLOR]',baseurl5,7,art+'best_goals_com.png',fanart,'')
        #addDir('[COLOR white]The Score News Feeds[/COLOR]','url',11,art+'news.png',fanart,'')
        addDir('[COLOR white]OpenFootball Stat Central[/COLOR]','url',20,art+'stats.png',fanart,'')
        #addDir('[COLOR white]LiveOnSat[/COLOR]',baseurl11+'/los_soc_br_eng_ALL.php',26,art+'stats.png',fanart,'')
        




def INDEX(url):
        link = net.http_GET(url).content
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="fplayer_row">', '<div class="cb"></div>')
        for a in all_videos:
                name = regex_from_to(a, '<strong>', '<').replace('&amp;','&')
                url = regex_from_to(a, 'onclick="', '"').replace('&amp;','&')
                url = url[38:]
                url = url.replace("','1');","")
                url = base64.decodestring(url)
                url = url[35:46]
                url = 'plugin://plugin.video.youtube/play/?video_id='+url
                icon = regex_from_to(a, '<img src="', '"').replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')




############################################################################################################################
                                                #goal-best
############################################################################################################################




def GBINDEX(url):
        link = net.http_GET(url).content
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<span>Top</span>', '<div class="leftStateMsg">')
        for a in all_videos:
                name = regex_from_to(a, '</span>', '<').replace('&amp;','&')
                url = regex_from_to(a, 'src="', '"').replace('&amp;','&')
                video_id = url[30:]
                url = 'plugin://plugin.video.youtube/play/?video_id='+video_id
                icon = 'http://i.ytimg.com/vi/' + str(video_id) + '/mqdefault.jpg'
                addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')
        addDir('[COLOR white]Top Goals[/COLOR]',baseurl5+'/topgoals.html',8,art+'best_goals_com.png',fanart,'')
        addDir('[COLOR white]Top Assists[/COLOR]',baseurl5+'/topassists.html',8,art+'best_goals_com.png',fanart,'')
        addDir('[COLOR white]Top Saves[/COLOR]',baseurl5+'/topsaves.html',8,art+'best_goals_com.png',fanart,'')



def GBTOP(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<p><a href="(.*?)" target="_self" title="week">(.*?)</a></p>').findall(link)
        for url, name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl5+url,9,art+'best_goals_com.png',fanart,'')



def GBLINK(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        try:
                match=re.compile('<iframe .*?src="(.*?)" .*?>').findall(link)
                for url in match:
                        print url
                        #url = url.replace('http://','https://').replace('//www.youtube.com/','http://www.youtube.com/')
                        print url
                        video_id = url[30:]
                        url = url.replace('http://www.youtube.com/embed/','plugin://plugin.video.youtube/play/?video_id=')
                        icon = 'http://i.ytimg.com/vi/' + str(video_id) + '/mqdefault.jpg'
                        try:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')
                        except:
                                addDir('[COLOR white]%s[/COLOR]' %name,'http:'+url,100,icon,fanart,'')
        except:
                addDir('[COLOR white]%s[/COLOR]' %name,url,8,art+'best_goals_com.png',fanart,'')



############################################################################################################################

############################################################################################################################




class Window(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self.caption = kwargs.get('caption','')
        self.text = kwargs.get('text','')
        xbmcgui.WindowXMLDialog.__init__(self)

    def onInit(self):
        self.getControl(100).setLabel(self.caption)
        self.getControl(200).setText(self.text)


def showresfix(caption,text):
    path = xbmcaddon.Addon().getAddonInfo('path')
    win = Window('resfix.xml',path,'Default',caption=caption,text=text)
    win.doModal()
    del win


def resfix(url):
    text = utils.RESFIX(url)
    showresfix(None,text)
    CAT()



def showrss(caption,text):
    path = xbmcaddon.Addon().getAddonInfo('path')
    win = Window('rssnews.xml',path,'Default',caption=caption,text=text)
    win.doModal()
    del win


def newsrss(url):
    text = utils.NEWSRSS(url)
    showrss(None,text)
    CAT()



def tables(url):
    text = utils.LTABLES(url)
    caption = utils.CLTABLES(url)
    showtables(caption,text)
    CAT()



def showtables(caption,text):
    path = xbmcaddon.Addon().getAddonInfo('path')
    win = Window('tables.xml',path,'Default',caption=caption,text=text)
    win.doModal()
    del win




def TABLES(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.*?)" class="pull-right">(.*?)</a>').findall(link)
        for url, name in match:
                name = name.replace('Full ','')
                addLink2('[COLOR white]%s[/COLOR]' %name,baseurl+url,4,art+'tables.png',fanart)




def livescore(url):
    text = utils.LIVESCORE(url)
    caption = utils.LIVESHEAD(url)
    showscore(caption,text)
    CAT()



def showscore(caption,text):
    path = xbmcaddon.Addon().getAddonInfo('path')
    win = Window('livescore.xml',path,'Default',caption=caption,text=text)
    win.doModal()
    del win


############################################################################################################################
                                                #openfootball
############################################################################################################################




def OFINDEX():
        addDir('[COLOR white]World Cup[/COLOR]',baseurl9+'/openfootball/world-cup',21,art+'worldcup.png',fanart,'')
        addDir('[COLOR white]Euro Cup[/COLOR]',baseurl9+'/openfootball/euro-cup',21,art+'eurocup.png',fanart,'')
        addDir('[COLOR white]Europe Champions League[/COLOR]',baseurl9+'/openfootball/europe-champions-league',21,art+'champions_league.png',fanart,'')
        addDir('[COLOR white]England[/COLOR]',baseurl9+'/openfootball/eng-england',21,art+'england.png',fanart,'')
        addDir('[COLOR white]Espana[/COLOR]',baseurl9+'/openfootball/es-espana',21,art+'espana.png',fanart,'')
        addDir('[COLOR white]Italy[/COLOR]',baseurl9+'/openfootball/it-italy',21,art+'italy.png',fanart,'')
        addDir('[COLOR white]Deutschland[/COLOR]',baseurl9+'/openfootball/de-deutschland',21,art+'deutschland.png',fanart,'')
        addDir('[COLOR white]Major League Soccer[/COLOR]',baseurl9+'/openfootball/major-league-soccer',21,art+'mls.png',fanart,'')
        addDir('[COLOR white]Brazil[/COLOR]',baseurl9+'/openfootball/br-brazil',21,art+'brazil.png',fanart,'')
        addDir('[COLOR white]France[/COLOR]',baseurl9+'/openfootball/fr-france',21,art+'france.png',fanart,'')
        addDir('[COLOR white]Russia[/COLOR]',baseurl9+'/openfootball/ru-russia',21,art+'russia.png',fanart,'')
        addDir('[COLOR white]Mexico[/COLOR]',baseurl9+'/openfootball/mx-mexico',21,art+'mexico.png',fanart,'')
        addDir('[COLOR white]Austria[/COLOR]',baseurl9+'/openfootball/at-austria',21,art+'austria.png',fanart,'')
        addDir('[COLOR white]Official associations[/COLOR]',baseurl9+'/openfootball/assocs',21,art+'official_associations.png',fanart,'')
        addDir('[COLOR white]Players[/COLOR]',baseurl9+'/openfootball/players',21,art+'players.png',fanart,'')
        addDir('[COLOR white]Women World Cup[/COLOR]',baseurl9+'/openfootball/women-world-cup',21,art+'women_worldcup.png',fanart,'')
        addDir('[COLOR white]Confoederatio Helvetica[/COLOR]',baseurl9+'/openfootball/ch-confoederatio-helvetica',21,art+'confoederatio_helvetica.png',fanart,'')
        addDir('[COLOR white]Confed Cup[/COLOR]',baseurl9+'/openfootball/confed-cup',21,art+'confed_cup.png',fanart,'')
        addDir('[COLOR white]Copa-Sudamericana[/COLOR]',baseurl9+'/openfootball/copa-sudamericana',21,art+'copa-sudamericana.png',fanart,'')
        addDir('[COLOR white]North America Champions League[/COLOR]',baseurl9+'/openfootball/north-america-champions-league',21,art+'north_america_champions.png',fanart,'')
        addDir('[COLOR white]Africa Cup[/COLOR]',baseurl9+'/openfootball/africa-cup',21,art+'africa_cup.png',fanart,'')
        addDir('[COLOR white]North America Gold Cup[/COLOR]',baseurl9+'/openfootball/north-america-gold-cup',21,art+'stats.png',fanart,'')
        addDir('[COLOR white]Copa America[/COLOR]',baseurl9+'/openfootball/copa-america',21,art+'copa_america.png',fanart,'')
        addDir('[COLOR white]Copa Libertadores[/COLOR]',baseurl9+'/openfootball/copa-libertadores',21,art+'copa_libertadores.png',fanart,'')




def OFINDEX2(url,iconimage):
        link = OPEN_URL(url)
        match=re.compile('<td class="content">\n            <span class="css-truncate css-truncate-target"><a href="(.*?)" class=".*?" id=".*?" title="(.*?)">.*?</a></span>').findall(link)
        for url, name in match:
                nono = ['README.md','STATS.md','README.md','NOTES.md','1-premierleague.yml','Datafile','setups',
                        'leagues.txt', '1-names', 'seasons_history', 'LINKS.md', '2014_quali.checksum', 'cup.yml',
                        'euro.yml', 'cl.yml', 'el.yml', 'cl_quali.yml', 'mls.yml', 'liga.yml', 'seriea.yml', 'cb.yml',
                        '1-bundesliga.yml', '2-budesliga2.yml', '3-liga3.yml', '1-ligue1.yml', '2-ligue2.yml', 'rfpl.yml',
                        'clausura.yml', 'TODO.md', 'sandbox', 'script', '2-liga1.yml', 'confed.yml', 'sudamericana.yml',
                        'gold.yml', 'copa.yml', 'libertadores.yml', 'This path skips through empty directories']
                if name not in nono:
                        if '.txt' in name:
                                name = name.replace('.txt','')
                                url = url.replace('/blob/','/')
                                print url
                                addLink2('[COLOR white]%s[/COLOR]' %name,'https://raw.githubusercontent.com'+url,22,iconimage,fanart)
                        else:
                                addDir('[COLOR white]%s[/COLOR]' %name,baseurl9+url,21,iconimage,fanart,'')



def of(url):
        text = utils.OF(url)
        caption = utils.CLTABLES(url)
        showof(caption,text)
        OFINDEX2(url,iconimage)



def showof(caption,text):
        path = xbmcaddon.Addon().getAddonInfo('path')
        win = Window('of.xml',path,'Default',caption=caption,text=text)
        win.doModal()
        del win






############################################################################################################################
                                                        #OKGOALS#
############################################################################################################################




def OKG(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href=\'(.*?)\' class="menulinks"><span><img style="border: none;" alt=".*?" src=".*?">(.*?)</span></a></li>').findall(link)
        for url, name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl10+url,24,'',fanart,'')




def OKGTEAM(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.*?)"><img style="border: none;" alt=".*?" src=".*?" />(.*?)</a></div>').findall(link)
        for url, name in match:
                name = name.replace(' &nbsp; &nbsp;','')
                url = baseurl10+url
                try:
                        link = OPEN_URL(url)
                        url = re.compile('<script data-config="(.*?)".*?>').findall(link)[0]
                        url = 'http:'+url
                        link = OPEN_URL(url)
                        icon = re.compile('"poster":"(.*?)"').findall(link)[0]
                        url = url.replace('http://config.playwire.com/','https://cdn.phoenix.intergi.com/')
                        url = url.replace('zeus.json','video-sd.mp4').replace('/v2/','/')
                        print url
                        addLink('[COLOR white]%s[/COLOR]' %name,url,25,icon,fanart)
                except: pass



def OKGLINK(name,url):
        link = OPEN_URL(url)
        url = re.compile('<script data-config="(.*?)".*?>').findall(link)[0]
        url = 'http:'+url
        print url
        link = OPEN_URL(url)
        url = re.compile('{"f4m":"(.*?)"}').findall(link)[0]
        icon = re.compile('"poster":"(.*?)"').findall(link)[0]
        addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')





############################################################################################################################
                                                        #LIVEONSAT
############################################################################################################################




def LSINDEX(url):
        link = OPEN_URL(url)
        match = re.compile('<h2 class = time_head>(.*?)</h2></div>').findall(link)
        for name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')





############################################################################################################################
                                                  #THE SCORE RSS
############################################################################################################################




def TSRSSINDEX():
        addDir('[COLOR white]MLS[/COLOR]',baseurl14+'mls.rss',12,art+'mls.png',fanart,'')
        addDir('[COLOR white]EPL[/COLOR]',baseurl14+'epl.rss',12,art+'england.png',fanart,'')
        addDir('[COLOR white]Champions League[/COLOR]',baseurl14+'chlg.rss',12,art+'champions_league.png',fanart,'')
        addDir('[COLOR white]Bundesliga[/COLOR]',baseurl14+'bund.rss',12,art+'deutschland.png',fanart,'')
        addDir('[COLOR white]La Liga[/COLOR]',baseurl14+'liga.rss',12,art+'espana.png',fanart,'')
        addDir('[COLOR white]Serie A[/COLOR]',baseurl14+'seri.rss',12,art+'italy.png',fanart,'')
        addDir('[COLOR white]Other Sports News[/COLOR]',baseurl14+'chlg.rss',12,art+'news.png',fanart,'')




def showtsrss(caption,text):
    path = xbmcaddon.Addon().getAddonInfo('path')
    win = Window('rssnews.xml',path,'Default',caption=caption,text=text)
    win.doModal()
    del win


def tsrss(url):
    text = utils.NEWSRSS(url)
    showtsrss(None,text)
    TSRSSINDEX()

############################################################################################################################

############################################################################################################################




def LIVE(url):
        link = OPEN_URL(url)
        match = re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for url, name in match:
                if 'Schedule' not in name:
                        name = name.replace('[LQ/HQ]','').replace('[LQ]','').replace('[HQ]','')
                        addDir('[COLOR white]%s[/COLOR]' %name,url,98,icon,fanart,'')




def LIVEL(url):
        link = OPEN_URL(url)
        match = re.compile('<li><a target="_top" href="(.*?)">(.*?)</a></li>').findall(link)
        for url, name in match:
                if 'm3u' in url:
                        name = name.replace('[3G/HQ]','[HQ]').replace('[2G/LQ]','[LQ]').replace('- Android/iOS','')
                        addDir('[COLOR white]%s[/COLOR]' %name,url,100,icon,fanart,'')





############################################################################################################################

############################################################################################################################



def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r            




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




def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==100:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def addLink2(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)




def OPEN_URL(url):
        headers = {}
        name = ''
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers).text
        return link




def RESOLVE(name,url):
    url1 = urlresolver.resolve(url)
    if url1:
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':description})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url1)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
    else:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def setView(content, viewType):
        ''' Why recode whats allready written and works well,
        Thanks go to Eldrado for it '''

        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        #if addon.get_setting('auto-view') == 'true':

        #    print addon.get_setting(viewType)
        #    if addon.get_setting(viewType) == 'Info':
        #        VT = '515'
        #    elif addon.get_setting(viewType) == 'Wall':
        #        VT = '501'
        #    elif viewType == 'default-view':
        #        VT = addon.get_setting(viewType)

        #    print viewType
        #    print VT
        
        #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

           
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
site=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
   
        
if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(url)

elif mode==2:
        TABLES(url)

elif mode==3:
        LINKS(name,url)

elif mode==4:
        tables(url)

elif mode==5:
        resfix(url)

elif mode==6:
        newsrss(url)

elif mode==7:
        GBINDEX(url)

elif mode==8:
        GBTOP(url)

elif mode==9:
        GBLINK(url)

elif mode==10:
        livescore(url)

elif mode==11:
        TSRSSINDEX()

elif mode==12:
        tsrss(url)

elif mode==20:
        OFINDEX()

elif mode==21:
        OFINDEX2(url,iconimage)

elif mode==22:
        of(url)

elif mode==23:
        OKG(url)

elif mode==24:
        OKGTEAM(url)

elif mode==25:
        OKGLINK(name,url)

elif mode==26:
        LSINDEX(url)

elif mode==98:
        LIVEL(url)

elif mode==99:
        LIVE(url)

elif mode==100:
        RESOLVE(name,url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

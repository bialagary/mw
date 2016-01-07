from webutils import *
from addon.common.addon import Addon
import time,datetime
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
import sys,json,urllib,urlparse
import CommonFunctions
common = CommonFunctions

addon = Addon('plugin.video.nbafullgames', sys.argv)

settings = xbmcaddon.Addon( id = 'plugin.video.nbafullgames' )
addonfolder=settings.getAddonInfo( 'path' )
artfolder=addonfolder + '/resources/media/'


def icon_path(filename):
    return artfolder + filename



base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def get_nbacom_video(link):
    link=link.replace('/index.html','')#.replace('//','/')
    soup = get_soup(link)
    bitrate = addon.get_setting('bitrate')
    link=soup.find('file',{'bitrate':'%s'%bitrate}).getText()
    return link

def get_nbacom_rss(cat):
    soup=get_soup(cat)
    items=soup.find('rss').find('channel').findAll('item')
    links=[]
    for i in range(len(items)):
        
        title=items[i].find('title').getText()
        link=items[i].find('guid').getText().replace('/index.html','.xml')
        try:
            date=items[i].find('pubdate').getText()
            try:
                index=date.find('2015')
            except:
                try:index=date.find('2016')
                except:
                    try:index=date.find('2014')
                    except:
                        try:index=date.find('2013')
                        except:index=0
            date=date[:index+4]
            title=title+' ( %s )'%date
            
            desc=items[i].find('description').getText()
            links+=[[link,title,desc]]
        #FF00FF
        except:
            desc=' '
            links+=[[link,title,desc]]
            pass
    return links

def get_videos_nbacom2(linky,page):
    linkk=linky+str(1+(15*(int(page)-1)))
    
    html=read_url(linkk)
    soup=bs(html)

    textarea = common.parseDOM(html, "textarea", attrs = { "id": "jsCode" })[0]
    content = textarea.replace("\\'","\\\\'").replace('\\\\"','\\\\\\"').replace('\\n','').replace('\\t','').replace('\\x','')
    query = json.loads(content)
    results = query['results'][0]
    
    
    
    for i in range(len(results)):
        link='http://www.nba.com/video/' + results[i]['id'].replace('/video','')+'.xml'

        mediaDateUts = time.ctime(float(results[i]['mediaDateUts']))
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(mediaDateUts, '%a %b %d %H:%M:%S %Y'))).strftime('%d.%m.%Y')
        title=results[i]['title']
        thumb=results[i]['metadata']['media']['thumbnail']['url']
        length=results[i]['metadata']['video']['length']
        desc=results[i]['metadata']['media']['excerpt']

        title=title+' ( %s )'%date


        url = build_url({'mode': 'open_nbacom', 'link':'%s'%link ,'foldername': 'nbacom2','title':'%s'%title,'thumb':'%s'%thumb, 'desc':'%s'%desc})
        li = xbmcgui.ListItem('%s'%title, iconImage='%s'%thumb)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'nbacom2', 'link':'%s'%linky, 'page':str(int(page)+1)})
    li = xbmcgui.ListItem('Next Page >', iconImage=icon_path('nba_next.jpg'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
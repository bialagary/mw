'''
    WWE Online (wweo.net) XBMC Plugin
    Copyright (C) 2013 XUNITYTALK.COM

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.		
'''

import os
import string
import sys
import re
import urlresolver
import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

addon_id = 'plugin.video.watchwrestling'

net = Net(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
headers = {
    'Accept'    :   'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
addon = Addon(addon_id, sys.argv)

BASEURL = addon.get_setting("websrc")

#PATHS
AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath, 'icons')

from universal import _common as univ_common
from universal import watchhistory, playbackengine

mode = addon.queries['mode']
url = addon.queries.get('url', '')
title = addon.queries.get('title', 'Watch Wrestling ( watchwrestling.to )')
img = addon.queries.get('img', os.path.join(IconPath, 'icon.jpg'))
section = addon.queries.get('section', '')
page = addon.queries.get('page', '')
mediaid = addon.queries.get('mediaid', '')
tp = addon.queries.get('tp', '1')
type = addon.queries.get('type', 'subfolder')
sort = addon.queries.get('sort', 'date')
sortorder = addon.queries.get('sortorder', 'desc')
options = addon.queries.get('options', '')
historytitle = addon.queries.get('historytitle', '')
historylink = addon.queries.get('historylink', '')
iswatchhistory = addon.queries.get('watchhistory', '')
queued = addon.queries.get('queued', '')

def WatchedCallback():
    print 'Video completed successfully.'
    
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",                   
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text
        
def add_dir_title():
    addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR orange][B]* * * * * ' + title + ' * * * * *[/B][/COLOR]'}, img=img)
		
menu_items = [ 
    ('Categories', 'categories', '', '', 'categories.jpg', 'Browse'),
    #('Monthly Archives', 'archives', '', '', 'archives.jpg', 'Browse'),
    ]    
def MainMenu():  #home-page
    add_dir_title()
    
    image = os.path.join(IconPath, 'latest.jpg')
    addon.add_directory({'mode' : 'Latest', 'title' : 'Latest', 'img' : image}, {'title':  'Latest'}, img=image)
    
    for (title, section, sort, page, icon, mode) in menu_items:
        image = os.path.join(IconPath, icon)
        addon.add_directory({'mode': mode, 'title' : title, 'section' : section, 'img' : image, 'url' : BASEURL, 'sort' : sort, 'page' : page}, {'title': title}, img=image )
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def GetLatest():
    add_dir_title()
    
    url_content = net.http_GET(BASEURL + 'home', headers=headers).content
    try:
        url_content = univ_common.str_conv(url_content)
    except:
        url_content = net.http_GET(BASEURL, headers=headers).content
        url_content = univ_common.str_conv(url_content)        
    url_content = re.sub("<!--.+?-->", " ", url_content)
    
    for latest_headers in re.finditer(r"(?s)<span class=\"name\">(.+?)</span>.*?<a class=\"more-link\" href=\"(.+?)\">(.+?)</div> </div></div> </div>", url_content):
        latest_title = latest_headers.group(1)        
        more_url = latest_headers.group(2)
        latest_items = latest_headers.group(3)
        
        more_title = latest_title
        more_title = more_title.replace('Latest', '')
        more_title = more_title.replace('Shows', '')
        more_title = more_title.replace('Wrestling', '')        
        more_title = more_title.strip()        
        more_image =  os.path.join(IconPath, more_title.lower().replace(' ','-') + '.jpg')
        
        addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR blue]' + latest_title + '[/COLOR]'}, img=more_image)
        for item in re.finditer(r"(?s)<a class=\"clip-link\".+?title=\"(.+?)\".+?href=\"(.+?)\".+?<img src=\"(.+?)\"", latest_items):
            item_title = univ_common.str_conv(addon.decode(item.group(1)))
            item_url = item.group(2)
            item_image = item.group(3)
            
            addon.add_directory({'mode' : 'GetLinks', 'url' : item_url, 'title' : item_title, 'img':item_image}, {'title':  '.....' + item_title}, img=item_image)
        
        
        addon.add_directory({'mode' : 'Page', 'url' : more_url, 'page' : '1', 'sort': 'date', 'sortorder' : 'desc', 'title' : more_title, 'img' : more_image}, {'title':  '[COLOR yellow].....More >>[/COLOR]'}, img=more_image)
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def Browse(section):
    add_dir_title()
    
    url_content = net.http_GET(BASEURL + 'home', headers=headers).content
    try:
        url_content = univ_common.str_conv(url_content)
    except:
        url_content = net.http_GET(BASEURL, headers=headers).content
        url_content = univ_common.str_conv(url_content)        
    url_content = re.sub("<!--.+?-->", " ", url_content)
    
    cats = re.search("(?s)<div id=\"" + section + "\-2\".+?<ul>(.+?)</ul>", url_content)
    if cats:
        cats = cats.group(1)
        for cat in re.finditer("<li.*?><a href=[\"'](.+?)[\"'].*?>(.+?)</a>", cats):
            cat_url = cat.group(1)
            
            cat_title = cat.group(2)
            
            if 'tna/ppv-tna' in cat_url:
                cat_title = cat_title + ' ( TNA )'
            elif 'wwe/ppv' in cat_url:
                cat_title = cat_title + ' ( WWE )'
            
            image = os.path.join(IconPath, cat_url[cat_url[0:cat_url.rfind('/')].rfind('/')+1:cat_url.rfind('/')] + '.jpg')
            
            addon.add_directory({'mode' : 'Page', 'title':  cat_title, 'img' : image, 'url' : cat_url, 'page' : '1', 'sort': 'date', 'sortorder' : 'desc'}, {'title':  cat_title}, img=image)
            
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def GetPage(url, page, sort, sortorder, options):

    if options:
        xbmcdlg = xbmcgui.Dialog()
        dlg_title = ''
        select_list = None
        select_list_v = None
        if options == 'sortby':
            dlg_title = 'Sort By'
            select_list = ['Date', 'Views', 'Likes', 'Comments']
            select_list_v = ['date', 'views', 'likes', 'comments']
        elif options == 'sortorder':
            dlg_title = 'Sort Order'
            select_list = ['Ascending', 'Descending']
            select_list_v = ['asc', 'desc']
        elif options == 'gotopage':
            dlg_title = 'Goto Page'
            
        if select_list:
            ret = xbmcdlg.select(dlg_title, select_list)
            if options == 'sortby':
                sort = select_list_v[ret]
            elif options == 'sortby':
                sortorder = select_list_v[ret]
        else:
            ret = xbmcdlg.numeric(0, dlg_title, page)
            if ret != 'cancelled':
                ret_num = int(ret)
                if (ret_num > 0 and ret_num != int(page) and ret_num <= int(tp)):
                    page = str(ret_num)
                else:
                    return
                

    add_dir_title()
    
    order = '?orderby=' + sort + '&order=' + sortorder
        
    page_url = url + 'page/' + page + '/' + order
    url_content = net.http_GET(page_url, headers=headers).content
    try:
        url_content = univ_common.str_conv(url_content)
    except:
        url_content = net.http_GET(page_url, headers=headers).content
        url_content = univ_common.str_conv(url_content)        
    
    ''' Page, Goto Page, Sort options '''
    totl_page = '1'
    page_of = re.search("<span class='pages'>Page ([0-9]+?) of ([0-9]+?)</span>", url_content)
        
    if page_of:
        totl_page = page_of.group(2)
    addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : page, 'sort': sort, 'sortorder' : sortorder, 'options' : 'gotopage', 'tp' : totl_page}, {'title':  '[COLOR red]Page ' + page + ' of ' + totl_page + '[/COLOR]'})
    
    addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : page, 'sort': sort, 'sortorder' : sortorder, 'options' : 'sortby'}, {'title':  '[COLOR blue]Sort By: [/COLOR][COLOR white]' + sort.title() + '[/COLOR]'})
    
    sort_order = 'Descending'
    if sortorder == 'asc':
        sort_order = 'Ascending'
    addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : page, 'sort': sort, 'sortorder' : sortorder, 'options' : 'sortorder'}, {'title':  '[COLOR blue]Sort Order: [/COLOR][COLOR white]' + sort_order.title() + '[/COLOR]'})
    
    url_content = re.search("(?s)>(?:Category|Monthly Archives)(.+?)<div id=\"sidebar\" role=\"complementary\">", url_content).group(1)    
    
    first_page = re.search("class=('first'|\"prev\")", url_content)
    if first_page:
        addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : '1', 'sort': sort, 'sortorder' : sortorder, 'tp' : totl_page, 'type':'notsubfolder'}, {'title':  '[COLOR yellow]<< First Page[/COLOR]'})
        addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : int(page) - 1, 'sort': sort, 'sortorder' : sortorder, 'tp' : totl_page, 'type':'notsubfolder'}, {'title':  '[COLOR yellow]< Previous Page[/COLOR]'})
        
    for item in re.finditer(r"(?s)<a class=\"clip-link\".+?title=\"(.+?)\".+?href=\"(.+?)\".+?img src=\"(.+?)\"", url_content):        
        item_title = univ_common.str_conv(addon.decode(item.group(1)))
        item_url = item.group(2)
        item_image = item.group(3)
        
        addon.add_directory({'mode' : 'GetLinks', 'url' : item_url, 'title' : item_title, 'img':item_image}, {'title': item_title}, img=item_image)
    
    last_page = re.search("class=('last'|\"next\")", url_content)
    if last_page:
        addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : int(page) + 1, 'sort': sort, 'sortorder' : sortorder, 'tp' : totl_page, 'type':'notsubfolder'}, {'title':  '[COLOR yellow]Next Page > [/COLOR]'})
        addon.add_directory({'mode' : 'Page', 'title':  title, 'img' : img, 'url' : url, 'page' : totl_page, 'sort': sort, 'sortorder' : sortorder, 'tp' : totl_page, 'type':'notsubfolder'}, {'title':  '[COLOR yellow]Last Page >> [/COLOR]'})
    
    upd_list = False
    if (options) or (type != 'subfolder'):
        upd_list = True
    xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=upd_list)

def GetLinks(url):
    from universal import _common as univ_common
    
    add_dir_title()
    print url
    url_content = net.http_GET(url, headers=headers).content
    try:
        url_content = univ_common.str_conv(url_content)
    except:
        url_content = net.http_GET(url, headers=headers).content
        url_content = univ_common.str_conv(url_content)        
    url_content = re.sub("<!--.+?-->", " ", url_content)
    
    super_headers_re = '<h3><span.+?font-size: 40px;.+?>(.+?)</'
    if 'wwf-attitude-era' in url:
        if not re.search('<h3><span style="font-size: 30px;', url_content):
            super_headers_re = '(?s)<div style=\"text-align: center;\"><span.+?>(.+?)</.+?<p>.+?</(p|div)></'
    
    super_headers = re.compile(super_headers_re).findall(url_content)
    
    super_header_item = 0
    super_header_title = ''
    
    if super_headers:
        if len(super_headers) == 1:
            super_headers = None
    
    if super_headers:
        super_header_title = ' - ' + super_headers[super_header_item]
        addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR red]' + super_headers[super_header_item] + '[/COLOR]'})
        super_header_item = super_header_item + 1
    
    try:
        if re.search('"lockerId":', url_content):
            # page has hidden links
            ajax_url = BASEURL + 'wp-admin/admin-ajax.php'
            locker_id = re.compile("\"lockerId\":\"(.+?)\"").findall(url_content)[0]
            action = 'sociallocker_loader'
            hash = re.compile("\"contentHash\":\"(.+?)\"").findall(url_content)[0]
            
            hidden_items =  net.http_POST(ajax_url, {'lockerId': locker_id, 'action': action, 'hash': hash}, headers=headers).content
            
            for hidden_item in re.finditer("(?s)<p>.+?<div.+?><span.+?>(.+?)</.+?<p>(.+?)</p>",hidden_items):
                hi_title = hidden_item.group(1)
                hi_links = hidden_item.group(2)
                
                hi_title_super = hi_title
                if super_headers:
                    hi_title_super = '.....' + hi_title
                    
                addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR blue]' + hi_title_super + '[/COLOR]'})
                for hi_link in re.finditer("(?s)<a.+?href=\"(.+?)\".+?>(.+?)</", hi_links):
                    hi_link_title = hi_link.group(2)
                    hi_link_url = hi_link.group(1)
                    
                    hi_link_title_super = hi_link_title
                    if super_headers:
                        hi_link_title_super = '.....' + hi_link_title
                    
                    contextMenuItems = []
                    queries = {'mode' : 'GetMedia', 'url' : hi_link_url, 'title' : title + super_header_title + ' - ' + hi_link_title, 'historytitle' : title, 'historylink': sys.argv[0]+sys.argv[2], 'img':img}
                    contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title + super_header_title + ' - ' + hi_link_title, addon.build_plugin_url( queries ) ) ) )
                    addon.add_directory(queries, {'title':  '.....' + hi_link_title_super},contextMenuItems, context_replace=False, img=img)
    except:
        pass
    
    regular_item_re = "(?s)<div style=\"text-align: center;\"><span.+?>(.+?)</.+?<p>(.+?)</(p|div)>"
    if 'wwf-attitude-era' in url:
        if not re.search('<h3><span style="font-size: 30px;', url_content):
            regular_item_re = "(?s)<h3><span.+?font-size: 40px;.+?>(.+?)</.+?<p>(.+?)</(p|div)>"
        else:
            #<h3><span style="font-size: 40px; color: #2F4F4F;">Pay-Per-View 1999</span></h3>
            ppv_item = re.search("(<h3><span.+?font-size: 40px;.+?>Pay-Per-View.+?</)", url_content)
            if ppv_item:
                ppv_item = ppv_item.group(1)
                
                ppv_content = re.search("(?s)" + ppv_item + "(.+?)</div>", url_content).group(1)
                ppv_content = re.sub("</p>", "", ppv_content)
                
                ppv_new = ppv_item + '<h3><span style="font-size: 30px;">PPV Events</span></h3>' + ppv_content
                
                url_content = re.sub(ppv_item, ppv_new, url_content)
                
            regular_item_re = "(?s)<h3><span.+?font-size: 30px;.+?>(.+?)</.+?<p>(.+?)</(p|div)>"
    
    for regular_item in re.finditer(regular_item_re,url_content):
    
        ri_title = regular_item.group(1)
        ri_links = regular_item.group(2)
        
        ri_title_super = ri_title
        if super_headers:
            ri_title_super = '.....' + ri_title
        
        addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR blue]' + ri_title_super + '[/COLOR]'})
        for ri_link in re.finditer("(?s)<a.+?href=\"(.+?)\".+?>(.+?)</", ri_links):
            ri_link_title = ri_link.group(2)
                        
            ri_link_title = univ_common.str_conv(addon.unescape(ri_link_title))
            
            ri_link_url = ri_link.group(1)
            
            ri_link_title_super = ri_link_title
            if super_headers:
                ri_link_title_super = '.....' + ri_link_title
                
            contextMenuItems = []
            queries = {'mode' : 'GetMedia', 'url' : ri_link_url, 'title' : title + super_header_title + ' - ' + ri_link_title, 'historytitle' : title, 'historylink': sys.argv[0]+sys.argv[2], 'img':img}
            contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title + super_header_title + ' - ' + ri_link_title, addon.build_plugin_url( queries ) ) ) )                
            addon.add_directory(queries, {'title':  '.....' + ri_link_title_super},contextMenuItems, context_replace=False, img=img)
            
            if super_headers:
                end_item = "h3>"
                if 'Pay-Per-View' in super_header_title:
                    end_item = "dummy"
                elif 'wwf-attitude-era' in url:
                    if re.search('<h3><span style="font-size: 30px;', url_content):
                        end_item = "p"
                        
                if re.search('href="' + ri_link_url.replace('?', '\?') + '" target="_blank">' + ri_link_title + '</a></p>\n<' + end_item, url_content):
                    super_header_title = ' - ' + super_headers[super_header_item]
                    addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR red]' + super_headers[super_header_item] + '[/COLOR]'})
                    super_header_item = super_header_item + 1
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetMedia(url):    
    
    if queued == 'true':
    
        wh = watchhistory.WatchHistory(addon_id)    
        
        hosted_media_url = None
        if url.startswith("http://pwtalk.net"):
            # Try to scrape page for media url
            headers={'Referer':url,'Host': 'wrestlingreviews.net'}
            url=url.replace('pwtalk.net','wrestlingreviews.net')
            url_content = net.http_GET(url, headers=headers).content 
                   
            url_content = re.sub("<!--.+?-->", " ", url_content)
            
            check_for_hosted_media = re.search(r"(?s)<iframe.+?src=\"(.+?)\"", url_content, re.IGNORECASE)
            if check_for_hosted_media:
                hosted_media_url = check_for_hosted_media.group(1)
        else:
            hosted_media_url = url
        
        if hosted_media_url:        
            hosted_media = urlresolver.HostedMediaFile(url=hosted_media_url)
            if hosted_media:
                resolved_media_url = urlresolver.resolve(hosted_media_url)
                if resolved_media_url:
                    
                    player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type='wweonline', 
                            title=title,season='', episode='', year='', watchedCallback=WatchedCallback)
                    
                    # add watch history item                        
                    if historylink:
                        wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                        wh.add_directory(historytitle, historylink, img=img, level='1')
                    else:
                        wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
                        
                    player.KeepAlive()
    else:
        playbackengine.PlayInPL(title, img=img)
        
if mode == 'main': 
    MainMenu()
elif mode=='Latest':
    GetLatest()
elif mode=='Browse':
    Browse(section)
elif mode == 'Page':
    GetPage(url, page, sort, sortorder, options)
elif mode == 'Menu':
    Menu(section)
elif mode == 'GetLinks':
    GetLinks(url)
elif mode == 'GetMedia':
    GetMedia(url)

#
#      Copyright (C) 2015 Lee Randall (whufclee)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs
import extract
import extras
import shutil
import subprocess
import datetime
import extract
import downloader
import popularpacks
from addon.common.addon import Addon

ADDON_ID   = 'plugin.program.TotalRevolution'
BASEURL    = 'http://addons.totalxbmc.com/'
ADDON      =  xbmcaddon.Addon(id=ADDON_ID)
HOME       =  ADDON.getAddonInfo('path')
dialog     =  xbmcgui.Dialog()
dp         =  xbmcgui.DialogProgress()
USERDATA   =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS     =  xbmc.translatePath(os.path.join('special://home','addons'))
ytlink     = 'http://gdata.youtube.com/feeds/api/users/"+YT_ID+"/playlists?start-index=1&max-results=25'
addonfolder      = xbmc.translatePath(os.path.join('special://','home/addons'))
packages         = xbmc.translatePath(os.path.join('special://home/addons','packages'))
username     =  ADDON.getSetting('username')
password     =  ADDON.getSetting('password')

#---------------------------------------------------------------------------------------------------
#Build Categories Menu
def Addon_Categories():
    extras.addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Audio','&typex=audio','grab_addons','audio.png','','','')
    extras.addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Image (Picture)','&typex=image','grab_addons','pictures.png','','','')
    extras.addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Program','&typex=program','grab_addons','programs.png','','','')
    extras.addDir('folder','[COLOR=yellow][PLUGIN][/COLOR] Video','&typex=video','grab_addons','video.png','','','')
    extras.addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Movies (Used for library scanning)','&typex=movie%20scraper','grab_addons','movies.png','','','')
    extras.addDir('folder','[COLOR=lime][SCRAPER][/COLOR] TV Shows (Used for library scanning)','&typex=tv%20show%20scraper','grab_addons','tvshows.png','','','')
    extras.addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Music Artists (Used for library scanning)','&typex=artist%20scraper','grab_addons','artists.png','','','')
    extras.addDir('folder','[COLOR=lime][SCRAPER][/COLOR] Music Videos (Used for library scanning)','&typex=music%20video%20scraper','grab_addons','musicvideos.png','','','')
    extras.addDir('folder','[COLOR=orange][SERVICE][/COLOR] All Services','&typex=service','grab_addons','services.png','','','')
    extras.addDir('folder','[COLOR=orange][SERVICE][/COLOR] Weather Service','&typex=weather','grab_addons','weather.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Repositories','&typex=repository','grab_addons','repositories.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Scripts (Program Add-ons)','&typex=executable','grab_addons','scripts.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Screensavers','&typex=screensaver','grab_addons','screensaver.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Script Modules','&typex=script%20module','grab_addons','scriptmodules.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Skins','&typex=skin','grab_addons','skins.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Subtitles','&typex=subtitles','grab_addons','subtitles.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][OTHER][/COLOR] Web Interface','&typex=web%20interface','grab_addons','webinterface.png','','','')
#    extras.addDir('folder','Lyrics','&typex=lyrics','grab_addons','lyrics.png','','','')
#---------------------------------------------------------------------------------------------------
#Build Countries Menu   
def Addon_Countries():
    extras.addDir('folder','African','&genre=african','grab_addons','african.png','','','')
    extras.addDir('folder','Arabic','&genre=arabic','grab_addons','arabic.png','','','')
    extras.addDir('folder','Asian','&genre=asian','grab_addons','asian.png','','','')
    extras.addDir('folder','Australian','&genre=australian','grab_addons','australian.png','','','')
    extras.addDir('folder','Austrian','&genre=austrian','grab_addons','austrian.png','','','')
    extras.addDir('folder','Belgian','&genre=belgian','grab_addons','belgian.png','','','')
    extras.addDir('folder','Brazilian','&genre=brazilian','grab_addons','brazilian.png','','','')
    extras.addDir('folder','Canadian','&genre=canadian','grab_addons','canadian.png','','','')
    extras.addDir('folder','Columbian','&genre=columbian','grab_addons','columbian.png','','','')
    extras.addDir('folder','Czech','&genre=czech','grab_addons','czech.png','','','')
    extras.addDir('folder','Danish','&genre=danish','grab_addons','danish.png','','','')
    extras.addDir('folder','Dominican','&genre=dominican','grab_addons','dominican.png','','','')
    extras.addDir('folder','Dutch','&genre=dutch','grab_addons','dutch.png','','','')
    extras.addDir('folder','Egyptian','&genre=egyptian','grab_addons','egyptian.png','','','')
    extras.addDir('folder','Filipino','&genre=filipino','grab_addons','filipino.png','','','')
    extras.addDir('folder','Finnish','&genre=finnish','grab_addons','finnish.png','','','')
    extras.addDir('folder','French','&genre=french','grab_addons','french.png','','','')
    extras.addDir('folder','German','&genre=german','grab_addons','german.png','','','')
    extras.addDir('folder','Greek','&genre=greek','grab_addons','greek.png','','','')
    extras.addDir('folder','Hebrew','&genre=hebrew','grab_addons','hebrew.png','','','')
    extras.addDir('folder','Hungarian','&genre=hungarian','grab_addons','hungarian.png','','','')
    extras.addDir('folder','Icelandic','&genre=icelandic','grab_addons','icelandic.png','','','')
    extras.addDir('folder','Indian','&genre=indian','grab_addons','indian.png','','','')
    extras.addDir('folder','Irish','&genre=irish','grab_addons','irish.png','','','')
    extras.addDir('folder','Italian','&genre=italian','grab_addons','italian.png','','','')
    extras.addDir('folder','Japanese','&genre=japanese','grab_addons','japanese.png','','','')
    extras.addDir('folder','Korean','&genre=korean','grab_addons','korean.png','','','')
    extras.addDir('folder','Lebanese','&genre=lebanese','grab_addons','lebanese.png','','','')
    extras.addDir('folder','Mongolian','&genre=mongolian','grab_addons','mongolian.png','','','')
    extras.addDir('folder','Nepali','&genre=nepali','grab_addons','nepali.png','','','')
    extras.addDir('folder','New Zealand','&genre=newzealand','grab_addons','newzealand.png','','','')
    extras.addDir('folder','Norwegian','&genre=norwegian','grab_addons','norwegian.png','','','')
    extras.addDir('folder','Pakistani','&genre=pakistani','grab_addons','pakistani.png','','','')
    extras.addDir('folder','Polish','&genre=polish','grab_addons','polish.png','','','')
    extras.addDir('folder','Portuguese','&genre=portuguese','grab_addons','portuguese.png','','','')
    extras.addDir('folder','Romanian','&genre=romanian','grab_addons','romanian.png','','','')
    extras.addDir('folder','Russian','&genre=russian','grab_addons','russian.png','','','')
    extras.addDir('folder','Singapore','&genre=singapore','grab_addons','singapore.png','','','')
    extras.addDir('folder','Spanish','&genre=spanish','grab_addons','spanish.png','','','')
    extras.addDir('folder','Swedish','&genre=swedish','grab_addons','swedish.png','','','')
    extras.addDir('folder','Swiss','&genre=swiss','grab_addons','swiss.png','','','')
    extras.addDir('folder','Syrian','&genre=syrian','grab_addons','syrian.png','','','')
    extras.addDir('folder','Tamil','&genre=tamil','grab_addons','tamil.png','','','')
    extras.addDir('folder','Thai','&genre=thai','grab_addons','thai.png','','','')
    extras.addDir('folder','Turkish','&genre=turkish','grab_addons','turkish.png','','','')
    extras.addDir('folder','UK','&genre=uk','grab_addons','uk.png','','','')
    extras.addDir('folder','USA','&genre=usa','grab_addons','usa.png','','','')
    extras.addDir('folder','Vietnamese','&genre=vietnamese','grab_addons','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
#Build Genres Menu
def Addon_Genres():       
    extras.addDir('folder','Anime','&genre=anime','grab_addons','anime.png','','','')
    extras.addDir('folder','Audiobooks','&genre=audiobooks','grab_addons','audiobooks.png','','','')
    extras.addDir('folder','Comedy','&genre=comedy','grab_addons','comedy.png','','','')
    extras.addDir('folder','Comics','&genre=comics','grab_addons','comics.png','','','')
    extras.addDir('folder','Documentary','&genre=documentary','grab_addons','documentary.png','','','')
    extras.addDir('folder','Downloads','&genre=downloads','grab_addons','downloads.png','','','')
    extras.addDir('folder','Food','&genre=food','grab_addons','food.png','','','')
    extras.addDir('folder','Gaming','&genre=gaming','grab_addons','gaming.png','','','')
    extras.addDir('folder','Health','&genre=health','grab_addons','health.png','','','')
    extras.addDir('folder','How To...','&genre=howto','grab_addons','howto.png','','','')
    extras.addDir('folder','Kids','&genre=kids','grab_addons','kids.png','','','')
    extras.addDir('folder','Live TV','&genre=livetv','grab_addons','livetv.png','','','')
    extras.addDir('folder','Movies','&genre=movies','grab_addons','movies.png','','','')
    extras.addDir('folder','Music','&genre=music','grab_addons','music.png','','','')
    extras.addDir('folder','News','&genre=news','grab_addons','news.png','','','')
    extras.addDir('folder','Photos','&genre=photos','grab_addons','photos.png','','','')
    extras.addDir('folder','Podcasts','&genre=podcasts','grab_addons','podcasts.png','','','')
    extras.addDir('folder','Radio','&genre=radio','grab_addons','radio.png','','','')
    extras.addDir('folder','Religion','&genre=religion','grab_addons','religion.png','','','')
    extras.addDir('folder','Space','&genre=space','grab_addons','space.png','','','')
    extras.addDir('folder','Sports','&genre=sports','grab_addons','sports.png','','','')
    extras.addDir('folder','Technology','&genre=tech','grab_addons','tech.png','','','')
    extras.addDir('folder','Trailers','&genre=trailers','grab_addons','trailers.png','','','')
    extras.addDir('folder','TV Shows','&genre=tv','grab_addons','tv.png','','','')
    extras.addDir('folder','Misc.','&genre=other','grab_addons','other.png','','','')
    if ADDON.getSetting('adult') == 'true':
        extras.addDir('folder','XXX','&genre=adult','grab_addons','adult.png','','','')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Addon_Final_Menu(url):
    BaseURL='http://totalxbmc.com/totalrevolution/AddonPortal/addondetails.php?id=%s' % (url)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch = re.compile('name="(.+?)"').findall(link)
    UIDmatch = re.compile('UID="(.+?)"').findall(link)
    idmatch = re.compile('id="(.+?)"').findall(link)
    providernamematch = re.compile('provider_name="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    createdmatch = re.compile('created="(.+?)"').findall(link)
    contentmatch = re.compile('addon_types="(.+?)"').findall(link)
    updatedmatch = re.compile('updated="(.+?)"').findall(link)
    downloadsmatch = re.compile('downloads="(.+?)"').findall(link)
#    xboxmatch = re.compile('xbox_compatible="(.+?)"').findall(link)
    descriptionmatch = re.compile('description="(.+?)"').findall(link)
    devbrokenmatch = re.compile('devbroke="(.+?)"').findall(link)
    brokenmatch = re.compile('broken="(.+?)"').findall(link)
    deletedmatch = re.compile('deleted="(.+?)"').findall(link)
    notesmatch = re.compile('mainbranch_notes="(.+?)"').findall(link)
#    xboxnotesmatch = re.compile('xbox_notes="(.+?)"').findall(link)
    repourlmatch = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch = re.compile('zip_url="(.+?)"').findall(link)
    genresmatch = re.compile('genres="(.+?)"').findall(link)
    forummatch = re.compile('forum="(.+?)"').findall(link)
    repoidmatch = re.compile('repo_id="(.+?)"').findall(link)
    licensematch = re.compile('license="(.+?)"').findall(link)
    platformmatch = re.compile('platform="(.+?)"').findall(link)
    visiblematch = re.compile('visible="(.+?)"').findall(link)
    scriptmatch = re.compile('script="(.+?)"').findall(link)
    programpluginmatch = re.compile('program_plugin="(.+?)"').findall(link)
    scriptmodulematch = re.compile('script_module="(.+?)"').findall(link)
    videopluginmatch = re.compile('video_plugin="(.+?)"').findall(link)
    audiopluginmatch = re.compile('audio_plugin="(.+?)"').findall(link)
    imagepluginmatch = re.compile('image_plugin="(.+?)"').findall(link)
    repositorymatch = re.compile('repository="(.+?)"').findall(link)
    weatherservicematch = re.compile('weather_service="(.+?)"').findall(link)
    skinmatch = re.compile('skin="(.+?)"').findall(link)
    servicematch = re.compile('service="(.+?)"').findall(link)
    warningmatch = re.compile('warning="(.+?)"').findall(link)
    webinterfacematch = re.compile('web_interface="(.+?)"').findall(link)
    moviescrapermatch = re.compile('movie_scraper="(.+?)"').findall(link)
    tvscrapermatch = re.compile('tv_scraper="(.+?)"').findall(link)
    artistscrapermatch = re.compile('artist_scraper="(.+?)"').findall(link)
    musicvideoscrapermatch = re.compile('music_video_scraper="(.+?)"').findall(link)
    subtitlesmatch = re.compile('subtitles="(.+?)"').findall(link)
    requiresmatch = re.compile('requires="(.+?)"').findall(link)
    modulesmatch = re.compile('modules="(.+?)"').findall(link)
    iconmatch = re.compile('icon="(.+?)"').findall(link)
    videopreviewmatch = re.compile('video_preview="(.+?)"').findall(link)
    videoguidematch = re.compile('video_guide="(.+?)"').findall(link)
    videoguidematch1 = re.compile('video_guide1="(.+?)"').findall(link)
    videoguidematch2 = re.compile('video_guide2="(.+?)"').findall(link)
    videoguidematch3 = re.compile('video_guide3="(.+?)"').findall(link)
    videoguidematch4 = re.compile('video_guide4="(.+?)"').findall(link)
    videoguidematch5 = re.compile('video_guide5="(.+?)"').findall(link)
    videoguidematch6 = re.compile('video_guide6="(.+?)"').findall(link)
    videoguidematch7 = re.compile('video_guide7="(.+?)"').findall(link)
    videoguidematch8 = re.compile('video_guide8="(.+?)"').findall(link)
    videoguidematch9 = re.compile('video_guide9="(.+?)"').findall(link)
    videoguidematch10 = re.compile('video_guide10="(.+?)"').findall(link)
    videolabelmatch1 = re.compile('video_label1="(.+?)"').findall(link)
    videolabelmatch2 = re.compile('video_label2="(.+?)"').findall(link)
    videolabelmatch3 = re.compile('video_label3="(.+?)"').findall(link)
    videolabelmatch4 = re.compile('video_label4="(.+?)"').findall(link)
    videolabelmatch5 = re.compile('video_label5="(.+?)"').findall(link)
    videolabelmatch6 = re.compile('video_label6="(.+?)"').findall(link)
    videolabelmatch7 = re.compile('video_label7="(.+?)"').findall(link)
    videolabelmatch8 = re.compile('video_label8="(.+?)"').findall(link)
    videolabelmatch9 = re.compile('video_label9="(.+?)"').findall(link)
    videolabelmatch10 = re.compile('video_label10="(.+?)"').findall(link)

#Need to add if broken version > current version statement   
    name  = namematch[0] if (len(namematch) > 0) else ''
    UID  = UIDmatch[0] if (len(UIDmatch) > 0) else ''
    addon_id  = idmatch[0] if (len(idmatch) > 0) else ''
    provider_name  = providernamematch[0] if (len(providernamematch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
    created  = createdmatch[0] if (len(createdmatch) > 0) else ''
    content_types  = contentmatch[0] if (len(contentmatch) > 0) else ''
    updated  = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    downloads  = downloadsmatch[0] if (len(downloadsmatch) > 0) else ''
#    xbox  = xboxmatch[0] if (len(xboxmatch) > 0) else ''
    desc  = '[CR][CR][COLOR=dodgerblue]Description: [/COLOR]'+descriptionmatch[0] if (len(descriptionmatch) > 0) else ''
    devbroken  = devbrokenmatch[0] if (len(devbrokenmatch) > 0) else ''
    broken  = brokenmatch[0] if (len(brokenmatch) > 0) else ''
    deleted  = '[CR]'+deletedmatch[0] if (len(deletedmatch) > 0) else ''
    notes  = '[CR][CR][COLOR=dodgerblue]User Notes: [/COLOR]'+notesmatch[0] if (len(notesmatch) > 0) else ''
#    xbox_notes  = xboxnotesmatch[0] if (len(xboxnotesmatch) > 0) else ''
    repo_url  = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    data_url  = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zip_url  = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    genres  = genresmatch[0] if (len(genresmatch) > 0) else ''
    forum  = '[CR][CR][COLOR=dodgerblue]Support Forum: [/COLOR]'+forummatch[0] if (len(forummatch) > 0) else ''
    repo_id  = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    license  = licensematch[0] if (len(licensematch) > 0) else ''
    platform  = '[COLOR=gold]     Platform: [/COLOR]'+platformmatch[0] if (len(platformmatch) > 0) else ''
    visible  = visiblematch[0] if (len(visiblematch) > 0) else ''
    script  = scriptmatch[0] if (len(scriptmatch) > 0) else ''
    program_plugin  = programpluginmatch[0] if (len(programpluginmatch) > 0) else ''
    script_module  = scriptmodulematch[0] if (len(scriptmodulematch) > 0) else ''
    video_plugin  = videopluginmatch[0] if (len(videopluginmatch) > 0) else ''
    audio_plugin  = audiopluginmatch[0] if (len(audiopluginmatch) > 0) else ''
    image_plugin  = imagepluginmatch[0] if (len(imagepluginmatch) > 0) else ''
    repository  = repositorymatch[0] if (len(repositorymatch) > 0) else ''
    service  = servicematch[0] if (len(servicematch) > 0) else ''
    skin  = skinmatch[0] if (len(skinmatch) > 0) else ''
    warning  = warningmatch[0] if (len(warningmatch) > 0) else ''
    web_interface  = webinterfacematch[0] if (len(webinterfacematch) > 0) else ''
    weather_service  = weatherservicematch[0] if (len(weatherservicematch) > 0) else ''
    movie_scraper  = moviescrapermatch[0] if (len(moviescrapermatch) > 0) else ''
    tv_scraper  = tvscrapermatch[0] if (len(tvscrapermatch) > 0) else ''
    artist_scraper  = artistscrapermatch[0] if (len(artistscrapermatch) > 0) else ''
    music_video_scraper  = musicvideoscrapermatch[0] if (len(musicvideoscrapermatch) > 0) else ''
    subtitles  = subtitlesmatch[0] if (len(subtitlesmatch) > 0) else ''
    requires  = requiresmatch[0] if (len(requiresmatch) > 0) else ''
    modules  = modulesmatch[0] if (len(modulesmatch) > 0) else ''
    icon  = iconmatch[0] if (len(iconmatch) > 0) else ''
    videopreview  = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide  = videoguidematch[0] if (len(videoguidematch) > 0) else 'None'
    videoguide1  = videoguidematch1[0] if (len(videoguidematch1) > 0) else 'None'
    videoguide2  = videoguidematch2[0] if (len(videoguidematch2) > 0) else 'None'
    videoguide3  = videoguidematch3[0] if (len(videoguidematch3) > 0) else 'None'
    videoguide4  = videoguidematch4[0] if (len(videoguidematch4) > 0) else 'None'
    videoguide5  = videoguidematch5[0] if (len(videoguidematch5) > 0) else 'None'
    videoguide6  = videoguidematch6[0] if (len(videoguidematch6) > 0) else 'None'
    videoguide7  = videoguidematch7[0] if (len(videoguidematch7) > 0) else 'None'
    videoguide8  = videoguidematch8[0] if (len(videoguidematch8) > 0) else 'None'
    videoguide9  = videoguidematch9[0] if (len(videoguidematch9) > 0) else 'None'
    videoguide10  = videoguidematch10[0] if (len(videoguidematch10) > 0) else 'None'
    videolabel1  = videolabelmatch1[0] if (len(videolabelmatch1) > 0) else 'None'
    videolabel2  = videolabelmatch2[0] if (len(videolabelmatch2) > 0) else 'None'
    videolabel3  = videolabelmatch3[0] if (len(videolabelmatch3) > 0) else 'None'
    videolabel4  = videolabelmatch4[0] if (len(videolabelmatch4) > 0) else 'None'
    videolabel5  = videolabelmatch5[0] if (len(videolabelmatch5) > 0) else 'None'
    videolabel6  = videolabelmatch6[0] if (len(videolabelmatch6) > 0) else 'None'
    videolabel7  = videolabelmatch7[0] if (len(videolabelmatch7) > 0) else 'None'
    videolabel8  = videolabelmatch8[0] if (len(videolabelmatch8) > 0) else 'None'
    videolabel9  = videolabelmatch9[0] if (len(videolabelmatch9) > 0) else 'None'
    videolabel10  = videolabelmatch10[0] if (len(videolabelmatch10) > 0) else 'None'
    if deleted != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=red]This add-on is depreciated, it\'s no longer available.[/COLOR]'
    elif broken == '' and devbroken == '' and warning =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=lime]No reported problems[/COLOR]'
    elif broken == '' and devbroken == '' and warning !='' and deleted =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=orange]Although there have been no reported problems there may be issues with this add-on, see below.[/COLOR]'
    elif broken == '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by the add-on developer.[CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken
    elif broken != '' and devbroken == '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by a member of the community at [COLOR=lime]www.totalxbmc.tv[/COLOR][CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken
    elif broken != '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by both the add-on developer and a member of the community at [COLOR=lime]www.totalxbmc.tv[/COLOR][CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken+'[CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken
    description = str('[COLOR=gold]Name: [/COLOR]'+name+'[COLOR=gold]     Author(s): [/COLOR]'+provider_name+'[COLOR=gold][CR][CR]Version: [/COLOR]'+version+'[COLOR=gold]     Created: [/COLOR]'+created+'[COLOR=gold]     Updated: [/COLOR]'+updated+'[COLOR=gold][CR][CR]Repository: [/COLOR]'+repo_id+platform+'[COLOR=gold]     Add-on Type(s): [/COLOR]'+content_types+requires+brokenfinal+deleted+warning+forum+desc+notes)

    if (broken == '') and (devbroken =='') and (deleted =='') and (warning ==''):
        extras.addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=lime] No problems reported[/COLOR]',description,'text_guide',icon,'','',description)    
    if (broken != '' and deleted == '') or (devbroken != '' and deleted == '') or (warning != '' and deleted ==''):
        extras.addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=orange] Possbile problems reported[/COLOR]',description,'text_guide',icon,'','',description)            
    if deleted != '':
        extras.addDir('addon','[COLOR=yellow][FULL DETAILS][/COLOR][COLOR=red] Add-on now depreciated[/COLOR]',description,'text_guide',icon,'','',description)            
    if deleted =='':
        extras.Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name,name,'','addon_install','Install.png','','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forum,data_url)    
    if videopreview != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  Preview',videoguide1,'play_video','Video_Guide.png','','','')    
    if videoguide1 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','Video_Guide.png','','','')    
    if videoguide2 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','Video_Guide.png','','','')    
    if videoguide3 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','Video_Guide.png','','','')    
    if videoguide4 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','Video_Guide.png','','','')    
    if videoguide5 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','Video_Guide.png','','','')    
    if videoguide6 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel6,videoguide6,'play_video','Video_Guide.png','','','')    
    if videoguide7 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel7,videoguide7,'play_video','Video_Guide.png','','','')    
    if videoguide8 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel8,videoguide8,'play_video','Video_Guide.png','','','')    
    if videoguide9 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel9,videoguide9,'play_video','Video_Guide.png','','','')    
    if videoguide10 != 'None':
        extras.addDir('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel10,videoguide10,'play_video','Video_Guide.png','','','')    
#---------------------------------------------------------------------------------------------------
#Recursive loop for downloading files from web
def Recursive_Loop(recursive_location,remote_path):
    print"recursive_location: "+recursive_location
    print"remote_path: "+remote_path
    if not os.path.exists(recursive_location):
        os.makedirs(recursive_location)
    link = extras.Open_URL(remote_path).replace('\n','').replace('\r','')
    match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
    for href in match:
        print"href: "+href
        filepath=xbmc.translatePath(os.path.join(recursive_location,href)) #works
        if '/' not in href:
            try:
                dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                print"downloading: "+remote_path+href
                downloader.download(remote_path+href, filepath, dp)
            except: print"failed to install"+href
        if '/' in href and '..' not in href and 'http' not in href:
            remote_path2 = remote_path+href
            Recursive_Loop(filepath,remote_path2)
        else: pass
#---------------------------------------------------------------------------------------------------
#Step 1 of the addon install process (installs the actual addon)
def Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    print "############# ADDON INSTALL #################"
    print "repo_url: "+str(repo_link)
    print "zip_url: "+str(zip_link)
    print "repo_id: "+str(repo_id)
    print "name: "+name
    print "forum"+forum
    print "provider_name"+provider_name
    print "data_path: "+data_path
    repo_id=str(repo_id)
    status=1
    repostatus=1
    modulestatus=1
    addondownload=xbmc.translatePath(os.path.join(packages,name+'.zip'))
    addonlocation=xbmc.translatePath(os.path.join(ADDONS,addon_id))
    dp.create("Installing Addon","Please wait whilst your addon is installed",'', '')
    try:
        downloader.download(repo_link, addondownload, dp)
        extract.all(addondownload, addonfolder, dp)
    except:
        try:
            downloader.download(zip_link, addondownload, dp)
            extract.all(addondownload, addonfolder, dp)
        except:
            try:
                if not os.path.exists(addonlocation):
                    os.makedirs(addonlocation)
                link = extras.Open_URL(data_path).replace('\n','').replace('\r','')
                match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(addonlocation,href))
                    if addon_id not in href and '/' not in href:
                        try:
                            dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                            print"downloading: "+data_path+href
                            downloader.download(data_path+href, filepath, dp)
                        except: print"failed to install"+href
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = data_path+href
                        Recursive_Loop(filepath,remote_path)
            except:
                dialog.ok("Error downloading add-on", 'There was an error downloading [COLOR=yellow]'+name,'[/COLOR]Please consider updating the add-on portal with details','or report the error on the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')             
                status=0
    if status==1:
        time.sleep(1)
        dp.update(0,"[COLOR=yellow]"+name+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing repository')
        time.sleep(1)
        repopath = xbmc.translatePath(os.path.join(ADDONS, repo_id))
        if (repo_id != 'repository.xbmc.org') and not (os.path.exists(repopath)) and (repo_id != '') and ('superrepo' not in repo_id):
            Install_Repo(repo_id)
        incremental = 'http://totalxbmc.com/totalrevolution/AddonPortal/downloadcount.php?id=%s' % (addon_id)
        extras.Open_URL(incremental)
        Dependency_Install(name,addon_id)
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        if repostatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing the repository.','This will mean the add-on fails to update')
        if modulestatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing modules.','This could result in errors with the add-on.')
        if modulestatus != 0 and repostatus != 0 and forum != '':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]Support for this add-on can be found at [COLOR=yellow]'+forum,'[/COLOR][CR]Remember to visit [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] for all your Kodi needs.')
        if modulestatus != 0 and repostatus != 0 and forum == '':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]No details of forum support have been given but','we\'ll be happy to help at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')
#---------------------------------------------------------------------------------------------------
#Step 2 of the addon install process (installs the repo if one exists)
def Install_Repo(repo_id):
    repostatus=1
    BaseURL='http://totalxbmc.com/totalrevolution/AddonPortal/dependencyinstall.php?id=%s' % (repo_id)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch = re.compile('name="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    repourlmatch = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch = re.compile('zip_url="(.+?)"').findall(link)
    repoidmatch = re.compile('repo_id="(.+?)"').findall(link)  
    reponame  = namematch[0] if (len(namematch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
    repourl  = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    dataurl  = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zipurl   = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    repoid   = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    repozipname=xbmc.translatePath(os.path.join(packages,reponame+'.zip')) 
    repolocation=xbmc.translatePath(os.path.join(ADDONS,repoid))
    print"Repo_URL: "+repourl
    print"Repo_Data_URL: "+dataurl
    print"Repo_Zip_URL: "+zipurl
    try:
        downloader.download(repourl, repozipname, dp)
        extract.all(repozipname, addonfolder, dp)
    except:
        try:
            downloader.download(zipurl, repozipname, dp)
            extract.all(repozipname, addonfolder, dp)
        except:
            try:
                if not os.path.exists(repolocation):
                    os.makedirs(repolocation)
                link = extras.Open_URL(dataurl).replace('\n','').replace('\r','')
                match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(repolocation,href))
                    if addon_id not in href and '/' not in href:
                        try:
                            dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                            print"downloading: "+dataurl+href
                            downloader.download(dataurl+href, filepath, dp)
                        except: print"failed to install"+href
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = dataurl+href
                        Recursive_Loop(filepath,remote_path)
            except:
                dialog.ok("Error downloading repository", 'There was an error downloading the [COLOR=yellow]'+reponame,'[/COLOR]repository. Please consider updating the add-on portal with details','or report the error on the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')             
                repostatus=0
    if repostatus==1:
        time.sleep(1)
        dp.update(0,"[COLOR=yellow]"+reponame+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing dependencies')
        time.sleep(1)
        incremental = 'http://totalxbmc.com/totalrevolution/AddonPortal/downloadcount.php?id=%s' % (repo_id)
        extras.Open_URL(incremental)
#---------------------------------------------------------------------------------------------------
#Step 3 of the addon install process (installs the dependencies)
def Dependency_Install(name,addon_id):
    modulestatus=1
    status=1
    addonxml = xbmc.translatePath(os.path.join(ADDONS,addon_id,'addon.xml'))    
    addonsource = open(addonxml, mode = 'r')
    readxml = addonsource.read()
    addonsource.close()
    dmatch = re.compile('import addon="(.+?)"').findall(readxml)
    for requires in dmatch:
        if not 'xbmc.python' in requires:
            print 'Script Requires --- ' + requires
            dependencypath = xbmc.translatePath(os.path.join(ADDONS, requires))
            if not os.path.exists(dependencypath):
                BaseURL='http://totalxbmc.com/totalrevolution/AddonPortal/dependencyinstall.php?id=%s' % (requires)
                link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
                namematch = re.compile('name="(.+?)"').findall(link)
                versionmatch = re.compile('version="(.+?)"').findall(link)
                repourlmatch = re.compile('repo_url="(.+?)"').findall(link)
                dataurlmatch = re.compile('data_url="(.+?)"').findall(link)
                zipurlmatch = re.compile('zip_url="(.+?)"').findall(link)
                repoidmatch = re.compile('repo_id="(.+?)"').findall(link)  
                depname  = namematch[0] if (len(namematch) > 0) else ''
                version  = versionmatch[0] if (len(versionmatch) > 0) else ''
                repourl  = repourlmatch[0] if (len(repourlmatch) > 0) else ''
                dataurl  = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
                zipurl   = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
                repoid   = repoidmatch[0] if (len(repoidmatch) > 0) else ''
                dependencyname=xbmc.translatePath(os.path.join(packages,depname+'.zip')) 
                print"Dependency_URL: "+repourl
                print"Dependency_Data_URL: "+dataurl
                print"Dependency_Zip_URL: "+zipurl
                try:
                    downloader.download(repourl, dependencyname, dp)
                    extract.all(dependencyname, addonfolder, dp)
                except:
                    try:
                        downloader.download(zipurl, dependencyname, dp)
                        extract.all(dependencyname, addonfolder, dp)
                    except:
                        try:
                            if not os.path.exists(dependencypath):
                                os.makedirs(dependencypath)
                            link = extras.Open_URL(dataurl).replace('\n','').replace('\r','')
                            match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                            for href in match:
                                filepath=xbmc.translatePath(os.path.join(dependencypath,href))
                                if addon_id not in href and '/' not in href:
                                    try:
                                        dp.update(0,"Downloading [COLOR=yellow]"+href+'[/COLOR]','','Please wait...')
                                        print"downloading: "+dataurl+href
                                        downloader.download(dataurl+href, filepath, dp)
                                    except: print"failed to install"+href
                                if '/' in href and '..' not in href and 'http' not in href:
                                    remote_path = dataurl+href
                                    Recursive_Loop(filepath,remote_path)
                        except:
                            dialog.ok("Error downloading dependency", 'There was an error downloading [COLOR=yellow]'+depname,'[/COLOR]Please consider updating the add-on portal with details','or report the error on the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')             
                            status=0
                            modulestatus=0
                if status==1:
                    time.sleep(1)
                    dp.update(0,"[COLOR=yellow]"+depname+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Please wait...')
                    time.sleep(1)
                    incremental = 'http://totalxbmc.com/totalrevolution/AddonPortal/downloadcount.php?id=%s' % (requires)
                    extras.Open_URL(incremental)
    dp.close()
    time.sleep(1)
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Addons(url):
    if ADDON.getSetting('adult') == 'true':
        adult = 'yes'
    else:
        adult = 'no'
    buildsURL = 'http://totalxbmc.com/totalrevolution/AddonPortal/sortby.php?sortx=name&user=%s&pass=%s&adult=%s&%s' % (username, password, adult, url)
    link = extras.Open_URL(buildsURL).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)" <br> downloads="(.+?)" <br> icon="(.+?)" <br> UID="(.+?)" <br>', re.DOTALL).findall(link)
    extras.Sort_By(buildsURL,'addons')
    for name,downloads,icon,uid in match:
        extras.addDir('folder2',name+'[COLOR=lime] ['+downloads+' downloads][/COLOR]',uid,'addon_final_menu',icon,'','')        
#-----------------------------------------------------------------------------------------------------------------
#Search in description
def Search_Addons(url):
    vq = extras.Get_Keyboard( heading="Search for add-ons" )
    # if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0
    # we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Addons(url)
#-----------------------------------------------------------------------------------------------------------------
def Update_Repo():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.','','[COLOR=blue]For all your XBMC/Kodi support visit[/COLOR] [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')
    return
#-----------------------------------------------------------------------------------------------------------------
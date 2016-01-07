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

import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import urllib, urllib2, re, glob
import extras
import extract
import popularpacks
import addonfix
import speedtest
import addons
import communitybuilds
import yt
import CheckPath
import cache
import time
import news

ARTPATH      =  'http://totalxbmc.tv/totalrevolution/art/' + os.sep
ADDON        =  xbmcaddon.Addon(id='plugin.program.TotalRevolution')
AddonID      =  'plugin.program.TotalRevolution'
AddonTitle   =  "[COLOR=blue]T[/COLOR]otal[COLOR=dodgerblue]R[/COLOR]evolution"
zip          =  ADDON.getSetting('zip')
localcopy    =  ADDON.getSetting('localcopy')
privatebuilds=  ADDON.getSetting('private')
reseller     =  ADDON.getSetting('reseller')
resellername =  ADDON.getSetting('resellername')
resellerid   =  ADDON.getSetting('resellerid')
mastercopy   =  ADDON.getSetting('mastercopy')
username     =  ADDON.getSetting('username')
password     =  ADDON.getSetting('password')
login        =  ADDON.getSetting('login')
trcheck      =  ADDON.getSetting('trcheck')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
HOME         =  xbmc.translatePath('special://home/')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
THUMBNAILS   =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
FANART       =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'fanart.jpg'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
CBPATH       =  xbmc.translatePath(os.path.join(USB,'Community Builds',''))
cookiepath   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'cookiejar'))
startuppath  =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'startup.xml'))
tempfile     =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp.xml'))
idfile       =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'id.xml'))
idfiletemp   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'idtemp.xml'))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
GUINEW       =  xbmc.translatePath(os.path.join(userdatafolder,'guinew.xml'))
guitemp      =  xbmc.translatePath(os.path.join(userdatafolder,'guitemp',''))
tempdbpath   =  xbmc.translatePath(os.path.join(USB,'Database'))
urlbase      =  'None'

#-----------------------------------------------------------------------------------------------------------------
#Addon removal menu
def Addon_Removal_Menu():
    for file in glob.glob(os.path.join(ADDONS,'*')):
        name=str(file).replace(ADDONS,'[COLOR=red]REMOVE [/COLOR]').replace('plugin.','[COLOR=dodgerblue](PLUGIN) [/COLOR]').replace('audio.','').replace('video.','').replace('skin.','[COLOR=yellow](SKIN) [/COLOR]').replace('repository.','[COLOR=orange](REPOSITORY) [/COLOR]').replace('script.','[COLOR=cyan](SCRIPT) [/COLOR]').replace('metadata.','[COLOR=gold](METADATA) [/COLOR]').replace('service.','[COLOR=pink](SERVICE) [/COLOR]').replace('weather.','[COLOR=green](WEATHER) [/COLOR]').replace('module.','[COLOR=gold](MODULE) [/COLOR]')
        iconimage=(os.path.join(file,'icon.png'))
        fanart=(os.path.join(file,'fanart.jpg'))
        extras.addDir('',name,file,'remove_addons',iconimage,fanart,'','')
#-----------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
#Addon Maintenance Section
def Addon_Fixes():
    extras.addDir('','[COLOR=blue]T[/COLOR][COLOR=white]otal[/COLOR][COLOR=dodgerblue]R[/COLOR][COLOR=white]evolution[/COLOR] Storage Folder Check','url','check_storage','Check_Download.png','','','')
    extras.addDir('folder','Completely remove an add-on (inc. passwords)','plugin','addon_removal_menu', 'Remove_Addon.png','','','')
    extras.addDir('','Make Add-ons Gotham/Helix Compatible','none','gotham', 'Gotham_Compatible.png','','','')
    extras.addDir('','Make Skins Kodi (Helix) Compatible','none','helix', 'Kodi_Compatible.png','','','')
    extras.addDir('','Hide my add-on passwords','none','hide_passwords', 'Hide_Passwords.png','','','')
    if trcheck == 'true':
        extras.addDir('folder','OnTapp.TV / OSS Integration', 'none', 'addonfix', 'Addon_Fixes.png','','','')
    extras.addDir('folder','Test My Download Speed', 'none', 'speedtest_menu', 'Speed_Test.png','','','')
    extras.addDir('','Unhide my add-on passwords','none','unhide_passwords', 'Unhide_Passwords.png','','','')
    extras.addDir('','Update My Add-ons (Force Refresh)', 'none', 'update', 'Update_Addons.png','','','')
    extras.addDir('','Wipe All Add-on Settings (addon_data)','url','remove_addon_data','Delete_Addon_Data.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Addons section
def Addon_Menu():
    extras.addDir('folder','[COLOR=yellow][Manual Search][/COLOR] Search By Name','name=','search_addons','Search_Addons.png','','','')
    extras.addDir('folder','[COLOR=yellow][Manual Search][/COLOR] Search By Author','author=','search_addons','Search_Addons.png','','','')
    extras.addDir('folder','[COLOR=yellow][Manual Search][/COLOR] Search In Description','desc=','search_addons','Search_Addons.png','','','')
    extras.addDir('folder','[COLOR=lime][Filter Results][/COLOR] By Genres', '', 'addon_genres', 'Search_Genre.png','','','')
    extras.addDir('folder','[COLOR=lime][Filter Results][/COLOR] By Countries', '', 'addon_countries', 'Search_Country.png','','','')
    extras.addDir('folder','[COLOR=lime][Filter Results][/COLOR] By Kodi Categories', '', 'addon_categories', 'Search_Category.png','','','')
    if trcheck == 'true':
        extras.addDir('folder','[COLOR=dodgerblue]Install Popular Packs[/COLOR]', 'none', 'popular', 'Addon_Packs.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Backup/Restore root menu
def Backup_Restore():
    extras.addDir('folder','Backup My Content','none','backup_option','Backup.png','','','')
    extras.addDir('folder','Restore My Content','none','restore_option','Restore.png','','','')
#---------------------------------------------------------------------------------------------------
#Main category list
def Categories(localbuildcheck,localversioncheck,id,welcometext):
    sign = 0
    addonportal  =  ADDON.getSetting('addonportal')
    commbuilds   =  ADDON.getSetting('maintenance')
    hardware     =  ADDON.getSetting('hardwareportal')
    maintenance  =  ADDON.getSetting('maintenance')
    newsportal   =  ADDON.getSetting('latestnews')
    tutorials    =  ADDON.getSetting('tutorialportal')
    if (username in welcometext) and ('elc' in welcometext):
        sign=1
        extras.addDir('',welcometext,'show','user_info','TOTALXBMC.png','','','')
        if id != 'None':
            if id != 'Local':
                updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
                if updatecheck == True:
                    extras.addDir('','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','TOTALXBMC.png','','','')
                else:
                    extras.addDir('','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','TOTALXBMC.png','','','')
            else:
                if localbuildcheck == 'Incomplete':
                    extras.addDir('','[COLOR=lime]Your last restore is not yet completed[/COLOR]','url',communitybuilds.Check_Local_Install(),'TOTALXBMC.png','','','')
                else:
                    extras.addDir('','[COLOR=lime]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','TOTALXBMC.png','','','','','')
        extras.addDir('','[COLOR=gold]----------------------------------------------[/COLOR]','None','','TOTALXBMC.png','','','')
    if username != '' and password !='' and sign!=1 and trcheck=='true':
        extras.addDir('','[COLOR=lime]Unable to login, please check your details[/COLOR]','None','addon_settings','TOTALXBMC.png','','','')   
    if trcheck == 'true' and sign!=1:
        extras.addDir('',welcometext,'None','register','TOTALXBMC.png','','','')
    extras.addDir('','[COLOR=yellow]Settings[/COLOR]','settings','addon_settings','SETTINGS.png','','','')
    if addonportal == 'true':
        extras.addDir('folder','Add-on Portal','none','addonmenu', 'Search_Addons.png','','','')
    if (username in welcometext) and ('elc' in welcometext) and (commbuilds == 'true'):
        extras.addDir('folder','Community Builds', 'none', 'community', 'Community_Builds.png','','','')
    if hardware == 'true':
        extras.addDir('folder','Hardware Reviews', 'none', 'hardware_root_menu', 'hardware.png','','','')
    if newsportal == 'true':
        extras.addDir('folder','Latest News', 'none', 'news_root_menu', 'LatestNews.png','','','')
    if tutorials == 'true':
        extras.addDir('folder','Tutorials','', 'tutorial_root_menu', 'TotalXBMC_Guides.png','','','')
    if maintenance == 'true':
        extras.addDir('folder','Maintenance','none', 'tools', 'Additional_Tools.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Build the root search menu for installing community builds
def CB_Root_Menu():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if reseller=='true':
        Reseller_Check()
    if privatebuilds=='true':
        extras.addDir('folder','[COLOR=lime]Show My Private List[/COLOR]','&visibility=private','grab_builds','Private_builds.png','','','')        
    if version < 14:
        extras.addDir('folder','[COLOR=orange]Show All Gotham Compatible Builds[/COLOR]','&visibility=public','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    if version >= 14:
        extras.addDir('folder','[COLOR=orange]Show All Helix Compatible Builds[/COLOR]','&visibility=public','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')
    extras.addDir('folder','Restore a locally stored Community Build','url','restore_local_CB','Restore.png','','','Back Up Your Full System')
    extras.addDir('folder','Create My Own Community Build','url','community_backup','Backup.png','','','Back Up Your Full System')
#---------------------------------------------------------------------------------------------------
#Check to see if a new version of a build is available
def Check_For_Update(localbuildcheck,localversioncheck,id):
    BaseURL = 'http://totalxbmc.tv/totalrevolution/Community_Builds/buildupdate.php?id=%s' % (id)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    if  localversioncheck < versioncheck:
        return True
    else:
        return False
#---------------------------------------------------------------------------------------------------
#Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help', 'if you\'re encountering kick-outs during playback.','as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        cache.Wipe_Cache()
        Remove_Textures()
#---------------------------------------------------------------------------------------------------
#Build Countries Menu (First Filter)    
def Countries(url):
    extras.addDir('folder','African',str(url)+'&genre=african','grab_builds','african.png','','','')
    extras.addDir('folder','Arabic',str(url)+'&genre=arabic','grab_builds','arabic.png','','','')
    extras.addDir('folder','Asian',str(url)+'&genre=asian','grab_builds','asian.png','','','')
    extras.addDir('folder','Australian',str(url)+'&genre=australian','grab_builds','australian.png','','','')
    extras.addDir('folder','Austrian',str(url)+'&genre=austrian','grab_builds','austrian.png','','','')
    extras.addDir('folder','Belgian',str(url)+'&genre=belgian','grab_builds','belgian.png','','','')
    extras.addDir('folder','Brazilian',str(url)+'&genre=brazilian','grab_builds','brazilian.png','','','')
    extras.addDir('folder','Canadian',str(url)+'&genre=canadian','grab_builds','canadian.png','','','')
    extras.addDir('folder','Columbian',str(url)+'&genre=columbian','grab_builds','columbian.png','','','')
    extras.addDir('folder','Czech',str(url)+'&genre=czech','grab_builds','czech.png','','','')
    extras.addDir('folder','Danish',str(url)+'&genre=danish','grab_builds','danish.png','','','')
    extras.addDir('folder','Dominican',str(url)+'&genre=dominican','grab_builds','dominican.png','','','')
    extras.addDir('folder','Dutch',str(url)+'&genre=dutch','grab_builds','dutch.png','','','')
    extras.addDir('folder','Egyptian',str(url)+'&genre=egyptian','grab_builds','egyptian.png','','','')
    extras.addDir('folder','Filipino',str(url)+'&genre=filipino','grab_builds','filipino.png','','','')
    extras.addDir('folder','Finnish',str(url)+'&genre=finnish','grab_builds','finnish.png','','','')
    extras.addDir('folder','French',str(url)+'&genre=french','grab_builds','french.png','','','')
    extras.addDir('folder','German',str(url)+'&genre=german','grab_builds','german.png','','','')
    extras.addDir('folder','Greek',str(url)+'&genre=greek','grab_builds','greek.png','','','')
    extras.addDir('folder','Hebrew',str(url)+'&genre=hebrew','grab_builds','hebrew.png','','','')
    extras.addDir('folder','Hungarian',str(url)+'&genre=hungarian','grab_builds','hungarian.png','','','')
    extras.addDir('folder','Icelandic',str(url)+'&genre=icelandic','grab_builds','icelandic.png','','','')
    extras.addDir('folder','Indian',str(url)+'&genre=indian','grab_builds','indian.png','','','')
    extras.addDir('folder','Irish',str(url)+'&genre=irish','grab_builds','irish.png','','','')
    extras.addDir('folder','Italian',str(url)+'&genre=italian','grab_builds','italian.png','','','')
    extras.addDir('folder','Japanese',str(url)+'&genre=japanese','grab_builds','japanese.png','','','')
    extras.addDir('folder','Korean',str(url)+'&genre=korean','grab_builds','korean.png','','','')
    extras.addDir('folder','Lebanese',str(url)+'&genre=lebanese','grab_builds','lebanese.png','','','')
    extras.addDir('folder','Mongolian',str(url)+'&genre=mongolian','grab_builds','mongolian.png','','','')
    extras.addDir('folder','Nepali',str(url)+'&genre=nepali','grab_builds','nepali.png','','','')
    extras.addDir('folder','New Zealand',str(url)+'&genre=newzealand','grab_builds','newzealand.png','','','')
    extras.addDir('folder','Norwegian',str(url)+'&genre=norwegian','grab_builds','norwegian.png','','','')
    extras.addDir('folder','Pakistani',str(url)+'&genre=pakistani','grab_builds','pakistani.png','','','')
    extras.addDir('folder','Polish',str(url)+'&genre=polish','grab_builds','polish.png','','','')
    extras.addDir('folder','Portuguese',str(url)+'&genre=portuguese','grab_builds','portuguese.png','','','')
    extras.addDir('folder','Romanian',str(url)+'&genre=romanian','grab_builds','romanian.png','','','')
    extras.addDir('folder','Russian',str(url)+'&genre=russian','grab_builds','russian.png','','','')
    extras.addDir('folder','Singapore',str(url)+'&genre=singapore','grab_builds','singapore.png','','','')
    extras.addDir('folder','Spanish',str(url)+'&genre=spanish','grab_builds','spanish.png','','','')
    extras.addDir('folder','Swedish',str(url)+'&genre=swedish','grab_builds','swedish.png','','','')
    extras.addDir('folder','Swiss',str(url)+'&genre=swiss','grab_builds','swiss.png','','','')
    extras.addDir('folder','Syrian',str(url)+'&genre=syrian','grab_builds','syrian.png','','','')
    extras.addDir('folder','Tamil',str(url)+'&genre=tamil','grab_builds','tamil.png','','','')
    extras.addDir('folder','Thai',str(url)+'&genre=thai','grab_builds','thai.png','','','')
    extras.addDir('folder','Turkish',str(url)+'&genre=turkish','grab_builds','turkish.png','','','')
    extras.addDir('folder','UK',str(url)+'&genre=uk','grab_builds','uk.png','','','')
    extras.addDir('folder','USA',str(url)+'&genre=usa','grab_builds','usa.png','','','')
    extras.addDir('folder','Vietnamese',str(url)+'&genre=vietnamese','grab_builds','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
#Build Genres Menu (First Filter)
def Genres(url):       
    extras.addDir('folder','Anime',str(url)+'&genre=anime','grab_builds','anime.png','','','')
    extras.addDir('folder','Audiobooks',str(url)+'&genre=audiobooks','grab_builds','audiobooks.png','','','')
    extras.addDir('folder','Comedy',str(url)+'&genre=comedy','grab_builds','comedy.png','','','')
    extras.addDir('folder','Comics',str(url)+'&genre=comics','grab_builds','comics.png','','','')
    extras.addDir('folder','Documentary',str(url)+'&genre=documentary','grab_builds','documentary.png','','','')
    extras.addDir('folder','Downloads',str(url)+'&genre=downloads','grab_builds','downloads.png','','','')
    extras.addDir('folder','Food',str(url)+'&genre=food','grab_builds','food.png','','','')
    extras.addDir('folder','Gaming',str(url)+'&genre=gaming','grab_builds','gaming.png','','','')
    extras.addDir('folder','Health',str(url)+'&genre=health','grab_builds','health.png','','','')
    extras.addDir('folder','How To...',str(url)+'&genre=howto','grab_builds','howto.png','','','')
    extras.addDir('folder','Kids',str(url)+'&genre=kids','grab_builds','kids.png','','','')
    extras.addDir('folder','Live TV',str(url)+'&genre=livetv','grab_builds','livetv.png','','','')
    extras.addDir('folder','Movies',str(url)+'&genre=movies','grab_builds','movies.png','','','')
    extras.addDir('folder','Music',str(url)+'&genre=music','grab_builds','music.png','','','')
    extras.addDir('folder','News',str(url)+'&genre=news','grab_builds','news.png','','','')
    extras.addDir('folder','Photos',str(url)+'&genre=photos','grab_builds','photos.png','','','')
    extras.addDir('folder','Podcasts',str(url)+'&genre=podcasts','grab_builds','podcasts.png','','','')
    extras.addDir('folder','Radio',str(url)+'&genre=radio','grab_builds','radio.png','','','')
    extras.addDir('folder','Religion',str(url)+'&genre=religion','grab_builds','religion.png','','','')
    extras.addDir('folder','Space',str(url)+'&genre=space','grab_builds','space.png','','','')
    extras.addDir('folder','Sports',str(url)+'&genre=sports','grab_builds','sports.png','','','')
    extras.addDir('folder','Technology',str(url)+'&genre=tech','grab_builds','tech.png','','','')
    extras.addDir('folder','Trailers',str(url)+'&genre=trailers','grab_builds','trailers.png','','','')
    extras.addDir('folder','TV Shows',str(url)+'&genre=tv','grab_builds','tv.png','','','')
    extras.addDir('folder','Misc.',str(url)+'&genre=other','grab_builds','other.png','','','')
    if ADDON.getSetting('adult') == 'true':
        extras.addDir('folder','XXX',str(url)+'&genre=adult','grab_builds','adult.png','','','')
#---------------------------------------------------------------------------------------------------
#Get params and clean up into string or integer
def Get_Params():
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
#---------------------------------------------------------------------------------------------------
#Hardware Root menu listings
def Hardware_Root_Menu():
    extras.addDir('folder','[COLOR=yellow]Manual Search[/COLOR]', 'hardware', 'manual_search', 'Manual_Search.png','','','')
    extras.addDir('folder','[COLOR=lime]All Devices[/COLOR]', '', 'grab_hardware', 'All.png','','','')
    extras.addDir('folder','[COLOR=orange][Hardware][/COLOR] Game Consoles', 'device=Console', 'grab_hardware', 'Consoles.png','','','')
    extras.addDir('folder','[COLOR=orange][Hardware][/COLOR] HTPC', 'device=HTPC', 'grab_hardware', 'HTPC.png','','','')
    extras.addDir('folder','[COLOR=orange][Hardware][/COLOR] Phones', 'device=Phone', 'grab_hardware', 'Phones.png','','','')
    extras.addDir('folder','[COLOR=orange][Hardware][/COLOR] Set Top Boxes', 'device=STB', 'grab_hardware', 'STB.png','','','')
    extras.addDir('folder','[COLOR=orange][Hardware][/COLOR] Tablets', 'device=Tablet', 'grab_hardware', 'Tablets.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Accessories][/COLOR] Remotes/Keyboards', 'device=Remote', 'grab_hardware', 'Remotes.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Accessories][/COLOR] Gaming Controllers', 'device=Controller', 'grab_hardware', 'Controllers.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Accessories][/COLOR] Dongles', 'device=Dongle', 'grab_hardware', 'Dongles.png','','','')
#---------------------------------------------------------------------------------------------------
#CPU Root menu listings
def Hardware_Filter_Menu(url):
    extras.addDir('folder','[COLOR=yellow][CPU][/COLOR] Allwinner Devices', str(url)+'&chip=Allwinner', 'grab_hardware', 'Allwinner.png','','','')
    extras.addDir('folder','[COLOR=yellow][CPU][/COLOR] AMLogic Devices', str(url)+'&chip=AMLogic', 'grab_hardware', 'AMLogic.png','','','')
    extras.addDir('folder','[COLOR=yellow][CPU][/COLOR] Intel Devices', str(url)+'&chip=Intel', 'grab_hardware', 'Intel.png','','','')
    extras.addDir('folder','[COLOR=yellow][CPU][/COLOR] Rockchip Devices', str(url)+'&chip=Rockchip', 'grab_hardware', 'Rockchip.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] Android', str(url)+'&platform=Android', 'grab_hardware', 'Android.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] iOS', str(url)+'&platform=iOS', 'grab_hardware', 'iOS.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] Linux', str(url)+'&platform=Linux', 'grab_hardware', 'Linux.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] OpenELEC', str(url)+'&platform=OpenELEC', 'grab_hardware', 'OpenELEC.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] OSX', str(url)+'&platform=OSX', 'grab_hardware', 'OSX.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] Pure Linux', str(url)+'&platform=Custom_Linux', 'grab_hardware', 'Custom_Linux.png','','','')
    extras.addDir('folder','[COLOR=lime][Platform][/COLOR] Windows', str(url)+'&platform=Windows', 'grab_hardware', 'Windows.png','','','')
    extras.addDir('folder','[COLOR=orange][Flash Storage][/COLOR] 4GB', str(url)+'&flash=4GB', 'grab_hardware', 'Flash.png','','','')
    extras.addDir('folder','[COLOR=orange][Flash Storage][/COLOR] 8GB', str(url)+'&flash=8GB', 'grab_hardware', 'Flash.png','','','')
    extras.addDir('folder','[COLOR=orange][Flash Storage][/COLOR] 16GB', str(url)+'&flash=16GB', 'grab_hardware', 'Flash.png','','','')
    extras.addDir('folder','[COLOR=orange][Flash Storage][/COLOR] 32GB', str(url)+'&flash=32GB', 'grab_hardware', 'Flash.png','','','')
    extras.addDir('folder','[COLOR=orange][Flash Storage][/COLOR] 64GB', str(url)+'&flash=64GB', 'grab_hardware', 'Flash.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][RAM][/COLOR] 1GB', str(url)+'&ram=1GB', 'grab_hardware', 'RAM.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][RAM][/COLOR] 2GB', str(url)+'&ram=2GB', 'grab_hardware', 'RAM.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][RAM][/COLOR] 4GB', str(url)+'&ram=4GB', 'grab_hardware', 'RAM.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Create How To (instructions) menu
def Instructions():
    extras.addDir('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  What is Community Builds?','url','instructions_3','How_To.png','','','')
    extras.addDir('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Creating a Community Build','url','instructions_1','How_To.png','','','')
    extras.addDir('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Installing a Community Build','url','instructions_2','How_To.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Add Your Own Guides @ [COLOR=lime]TotalXBMC.tv[/COLOR]','K0XIxEodUhc','play_video','How_To.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Community Builds FULL GUIDE',"ewuxVfKZ3Fs",'play_video','howto.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  IMPORTANT initial settings',"1vXniHsEMEg",'play_video','howto.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Install a Community Build',"kLsVOapuM1A",'play_video','howto.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Fixing a half installed build (guisettings.xml fix)',"X8QYLziFzQU",'play_video','howto.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 1)',"3rMScZF2h_U",'play_video','howto.png','','','')
    extras.addDir('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=yellow](OLD METHOD)[/COLOR]Create a Community Build (part 2)',"C2IPhn0OSSw",'play_video','howto.png','','','')
#---------------------------------------------------------------------------------------------------
#(Instructions) Create a community backup
def Instructions_1():
    extras.Text_Boxes('Creating A Community Backup', 
    '[COLOR=yellow]NEW METHOD[/COLOR][CR][COLOR=blue][B]Step 1:[/COLOR] Remove any sensitive data[/B][CR]Make sure you\'ve removed any sensitive data such as passwords and usernames in your addon_data folder.'
    '[CR][CR][COLOR=blue][B]Step 2:[/COLOR] Backup your system[/B][CR]Choose the backup option from the main menu, in there you\'ll find the option to create a Full Backup and this will create two zip files that you need to upload to a server.'
    '[CR][CR][COLOR=blue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip files to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - Dropbox and archive.org are two good examples.'
    '[CR][CR][COLOR=blue][B]Step 4:[/COLOR] Submit build at TotalXBMC[/B]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B].[CR]Full details can be found on there of the template you should use when posting, once you\'ve created your support thread (NOT BEFORE) you can request to become a member of the Community Builder group and you\'ll then have access to the web form for adding your builds to the portal.'
    '[CR][CR][COLOR=yellow]OLD METHOD[/COLOR][CR][COLOR=blue][B]Step 1: Backup your system[/B][/COLOR][CR]Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder. If you decide to choose this option [COLOR=yellow][B]make sure[/COLOR][/B] you already have a full backup of your system as it will completely wipe your addon settings (any stored settings such as passwords or any other changes you\'ve made to addons since they were first installed). If sharing a build with the community it\'s highly advised that you wipe your addon_data but if you\'ve made changes or installed extra data packages (e.g. skin artwork packs) then backup the whole build and then manually delete these on your PC and zip back up again (more on this later).'
    '[CR][CR][COLOR=blue][B]Step 2: Edit zip file on your PC[/B][/COLOR][CR]Copy your backup.zip file to your PC, extract it and delete all the addons and addon_data that isn\'t required.'
    '[CR][COLOR=blue]What to delete:[/COLOR][CR][COLOR=lime]/addons/packages[/COLOR] This folder contains zip files of EVERY addon you\'ve ever installed - it\'s not needed.'
    '[CR][COLOR=lime]/addons/<skin.xxx>[/COLOR] Delete any skins that aren\'t used, these can be very big files.'
    '[CR][COLOR=lime]/addons/<addon_id>[/COLOR] Delete any other addons that aren\'t used, it\'s easy to forget you\'ve got things installed that are no longer needed.'
    '[CR][COLOR=lime]/userdata/addon_data/<addon_id>[/COLOR] Delete any folders that don\'t contain important changes to addons. If you delete these the associated addons will just reset to their default values.'
    '[CR][COLOR=lime]/userdata/<all other folders>[/COLOR] Delete all other folders in here such as keymaps. If you\'ve setup profiles make sure you [COLOR=yellow][B]keep the profiles directory[/COLOR][/B].'
    '[CR][COLOR=lime]/userdata/Thumbnails/[/COLOR] Delete this folder, it contains all cached artwork. You can safely delete this but must also delete the file listed below.'
    '[CR][COLOR=lime]/userdata/Database/Textures13.db[/COLOR] Delete this and it will tell XBMC to regenerate your thumbnails - must do this if delting thumbnails folder.'
    '[CR][COLOR=lime]/xbmc.log (or Kodi.log)[/COLOR] Delete your log files, this includes any crashlog files you may have.'
    '[CR][CR][COLOR=blue][B]Step 3: Compress and upload[/B][/COLOR][CR]Use a program like 7zip to create a zip file of your remaining folders and upload to a file sharing site like dropbox.'
    '[CR][CR][COLOR=blue][B]Step 4: Submit build at TotalXBMC[/B][/COLOR]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B].[CR]Full details can be found on there of the template you should use when posting.')
#---------------------------------------------------------------------------------------------------
#(Instructions) Install a community build   
def Instructions_2():
    extras.Text_Boxes('Installing a community build', '[COLOR=blue][B]Step 1 (Optional): Backup your system[/B][/COLOR][CR]We highly recommend creating a backup of your system in case you don\'t like the build and want to revert back. Choose the backup option from the main menu, you will be asked whether you would like to delete your addon_data folder, select no unless you want to lose all your settings. If you ever need your backup it\'s stored in the location you\'ve selected in the addon settings.'
    '[CR][CR][COLOR=blue][B]Step 2: Browse the Community Builds[/B][/COLOR][CR]Find a community build you like the look of and make sure you read the description as it could contain unsuitable content or have specific install instructions. Once you\'ve found the build you want to install click on the install option and you\'ll have the option of a fresh install or a merge . The merge option will leave all your existing addons and userdata in place and just add the contents of the new build whereas the fresh (wipe) option will completely wipe your existing data and replace with content on the new build. Once you make your choice the download and extraction process will begin.'
    '[CR][CR][COLOR=blue][B]Step 3: [/COLOR][COLOR=red]VERY IMPORTANT[/COLOR][/B][CR]For the install to complete properly you MUST change the skin to the relevant skin used for that build. You will see a dialog box telling you which skin to switch to and then you\'ll be taken to the appearance settings where you can switch skins.'
    '[CR][CR][COLOR=blue][B]Step 4:[/B][/COLOR] Now go back to the Community Builds addon and in the same section wehre you clicked on step 1 of the install process you now need to select step 2 so it can install the guisettings.xml. This is extremely important, if you don\'t do this step then you\'ll end up with a real mish-mash hybrid install!'
    '[CR][CR][COLOR=blue][B]Step 5:[/B][/COLOR] You will now need to restart Kodi so the settings stick, just quit and it should all be fine. If for any reason the settings did not stick and it still doesn\'t look quite right just do step 2 of the install process again (guisettings.xml fix)')
#---------------------------------------------------------------------------------------------------
#(Instructions) What is a community build
def Instructions_3():
    extras.Text_Boxes('What is a community build', 'Community Builds are pre-configured builds of XBMC/Kodi based on different users setups. Have you ever watched youtube videos or seen screenshots of Kodi in action and thought "wow I wish I could do that"? Well now you can have a brilliant setup at the click of a button, completely pre-configured by users on the [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] forum. If you\'d like to get involved yourself and share your build with the community it\'s very simple to do, just go to the forum where you\'ll find full details or you can follow the guide in this addon.')
#-----------------------------------------------------------------------------------------------------------------
#News Menu
def News_Root_Menu(url):
    extras.addDir('folder','[COLOR=yellow]Manual Search[/COLOR]', 'news', 'manual_search', 'Manual_Search.png','','','')
    extras.addDir('folder','[COLOR=lime][All News][/COLOR] From all sites', str(url)+'', 'grab_news', 'Latest.png','','','')
    extras.addDir('folder','Official Kodi.tv News', str(url)+'&author=Official%20Kodi', 'grab_news', 'XBMC.png','','','')
    extras.addDir('folder','OpenELEC News', str(url)+'&author=OpenELEC', 'grab_news', 'OpenELEC.png','','','')
    extras.addDir('folder','Raspbmc News', str(url)+'&author=Raspbmc', 'grab_news', 'Raspbmc.png','','','')
    extras.addDir('folder','TotalXBMC News', str(url)+'&author=TotalXBMC', 'grab_news', 'TOTALXBMC.png','','','')
    extras.addDir('folder','XBMC4Xbox News', str(url)+'&author=XBMC4Xbox', 'grab_news', 'XBMC4Xbox.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Platform tutorial menu
def Platform_Menu(url):
    extras.addDir('folder','[COLOR=yellow]1. Install:[/COLOR]  Installation tutorials (e.g. flashing a new OS)', str(url)+'&thirdparty=InstallTools', 'grab_tutorials', 'Install.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Add-on Tools:[/COLOR]  Add-on maintenance and coding tutorials', str(url)+'&thirdparty=AddonTools', 'grab_tutorials', 'ADDONTOOLS.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Audio Tools:[/COLOR]  Audio related tutorials', str(url)+'&thirdparty=AudioTools', 'grab_tutorials', 'AUDIOTOOLS.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Gaming Tools:[/COLOR]  Integrate a gaming section into your setup', str(url)+'&thirdparty=GamingTools', 'grab_tutorials', 'gaming_portal.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Image Tools:[/COLOR]  Tutorials to assist with your pictures/photos', str(url)+'&thirdparty=ImageTools', 'grab_tutorials', 'IMAGETOOLS.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Library Tools:[/COLOR]  Music and Video Library Tutorials', str(url)+'&thirdparty=LibraryTools', 'grab_tutorials', 'LIBRARYTOOLS.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Skinning Tools:[/COLOR]  All your skinning advice', str(url)+'&thirdparty=SkinningTools', 'grab_tutorials', 'SKINNINGTOOLS.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Video Tools:[/COLOR]  All video related tools', str(url)+'&thirdparty=VideoTools', 'grab_tutorials', 'VIDEOTOOLS.png','','','')
#---------------------------------------------------------------------------------------------------
#Dialog to tell users how to register
def Register():
    dialog.ok("Register to unlock features", "To get the most out of this addon please register at", "the TotalXBMC forum where the addon is developed.","Visit [COLOR=lime]www.totalxbmc.tv/new-forum[/COLOR] for more details.")
#---------------------------------------------------------------------------------------------------
#Function to clear the addon_data
def Remove_Addon_Data():
    choice = xbmcgui.Dialog().yesno('Delete Addon_Data Folder?', 'This will free up space by deleting your addon_data', 'folder. This contains all addon related settings', 'including username and password info.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Userdata()
        dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are', 'log files generated when Kodi crashes and are','only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Logs()
        dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder?', 'This will free up space by deleting the zip install', 'files of your addons. The only downside is you\'ll no', 'longer be able to rollback to older versions.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        extras.Delete_Packages()
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Textures():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove', 'your Thumbnails folder. These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        cache.Remove_Textures()
        extras.Destroy_Path(THUMBNAILS)
        choice = xbmcgui.Dialog().yesno('Quit Kodi Now?', 'Cache has been successfully deleted.', 'You must now restart Kodi, would you like to quit now?','', nolabel='I\'ll restart later',yeslabel='Yes, quit')
        if choice == 1:
            extras.Kill_XBMC()
#---------------------------------------------------------------------------------------------------
#check what directories to add to root CB menu
def Reseller_Check():
    BaseURL='http://totalxbmc.com/totalrevolution/Community_Builds/reseller?reseller=%s&token=%s' % (resellername, resellerid)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    pathmatch = re.compile('path="(.+?)"').findall(link)
    resellerdirmatch = re.compile('reseller="(.+?)"').findall(link)
    premiumdirmatch = re.compile('premium="(.+?)"').findall(link)
    resellerdir = resellerdirmatch[0] if (len(resellerdirmatch) > 0) else 'None'
    premiumdir  = premiumdirmatch[0] if (len(premiumdirmatch) > 0) else 'None'
    exec resellerdir
    exec premiumdir
#---------------------------------------------------------------------------------------------------
#Instructions for the speed test
def Speed_Instructions():
    extras.Text_Boxes('Speed Test Instructions', '[COLOR=blue][B]What file should I use: [/B][/COLOR][CR]This function will download a file and will work out your speed based on how long it took to download. You will then be notified of '
    'what quality streams you can expect to stream without buffering. You can choose to download a 10MB, 16MB, 32MB, 64MB or 128MB file to use with the test. Using the larger files will give you a better '
    'indication of how reliable your speeds are but obviously if you have a limited amount of bandwidth allowance you may want to opt for a smaller file.'
    '[CR][CR][COLOR=blue][B]How accurate is this speed test:[/B][/COLOR][CR]Not very accurate at all! As this test is based on downloading a file from a server it\'s reliant on the server not having a go-slow day '
    'but the servers used should be pretty reliable. The 10MB file is hosted on a different server to the others so if you\'re not getting the results expected please try another file. If you have a fast fiber '
    'connection the chances are your speed will show as considerably slower than your real download speed due to the server not being able to send the file as fast as your download speed allows. Essentially the '
    'test results will be limited by the speed of the server but you will at least be able to see if it\'s your connection that\'s causing buffering or if it\'s the host you\'re trying to stream from'
    '[CR][CR][COLOR=blue][B]What is the differnce between Live Streams and Online Video:[/COLOR][/B][CR]When you run the test you\'ll see results based on your speeds and these let you know the quality you should expect to '
    'be able stream with your connection. Live Streams as the title suggests are like traditional TV channels, they are being streamed live so for example if you wanted to watch CNN this would fall into this category. '
    'Online Videos relates to movies, tv shows, youtube clips etc. Basically anything that isn\'t live - if you\'re new to the world of streaming then think of it as On Demand content, this is content that\'s been recorded and stored on the web.'
    '[CR][CR][COLOR=blue][B]Why am I still getting buffering:[/COLOR][/B][CR]The results you get from this test are strictly based on your download speed, there are many other factors that can cause buffering and contrary to popular belief '
    'having a massively fast internet connection will not make any difference to your buffering issues if the server you\'re trying to get the content from is unable to send it fast enough. This can often happen and is usually '
    'down to heavy traffic (too many users accessing the same server). A 10 Mb/s connection should be plenty fast enough for almost all content as it\'s very rare a server can send it any quicker than that.'
    '[CR][CR][COLOR=blue][B]What\'s the difference between MB/s and Mb/s:[/COLOR][/B][CR]A lot of people think the speed they see advertised by their ISP is Megabytes (MB/S) per second - this is not true. Speeds are usually shown as Mb/s '
    'which is Megabit per second - there are 8 of these to a megabyte so if you want to work out how many megabytes per second you\'re getting you need to divide the speed by 8. It may sound sneaky but really it\'s just the unit that has always been used.'
    '[CR][CR]Visit the forum at [COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B] for more information. A direct link to the buffering thread explaining what you can do to improve your viewing experience can be found at [COLOR=yellow]http://bit.ly/bufferingfix[/COLOR]'
    '[CR][CR]Hope to see you on the forum soon - [COLOR=dodgerblue]whufclee[/COLOR]')
#-----------------------------------------------------------------------------------------------------------------
def Speed_Test_Menu():
    extras.addDir('','[COLOR=blue]Instructions - Read me first[/COLOR]', 'none', 'speed_instructions', 'howto.png','','','')
    extras.addDir('','Download 16MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/16MB.txt', 'runtest', 'Download16.png','','','')
    extras.addDir('','Download 32MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/32MB.txt', 'runtest', 'Download32.png','','','')
    extras.addDir('','Download 64MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/64MB.txt', 'runtest', 'Download64.png','','','')
    extras.addDir('','Download 128MB file - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/128MB.txt', 'runtest', 'Download128.png','','','')
    extras.addDir('','Download 10MB file   - [COLOR=yellow]Server 2[/COLOR]', 'http://www.wswd.net/testdownloadfiles/10MB.zip', 'runtest', 'Download10.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Maintenance section
def Tools():
    extras.addDir('folder','[COLOR=yellow]Add-on Maintenance/Fixes[/COLOR]', 'none', 'addonfixes', 'Addon_Fixes.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue]Backup/Restore My Content[/COLOR]','none','backup_restore','Backup.png','','','')
    extras.addDir('folder','[COLOR=orange]Clean/Wipe Options[/COLOR]', 'none', 'wipetools', 'Addon_Fixes.png','','','')
    extras.addDir('','Check My IP Address', 'none', 'ipcheck', 'Check_IP.png','','','')
    extras.addDir('','Check XBMC/Kodi Version', 'none', 'xbmcversion', 'Version_Check.png','','','')
    extras.addDir('','Convert Physical Paths To Special',HOME,'fix_special','Special_Paths.png','','','')
    extras.addDir('','Force Close Kodi','url','kill_xbmc','Kill_XBMC.png','','','')
    extras.addDir('folder','Test My Download Speed', 'none', 'speedtest_menu', 'Speed_Test.png','','','')
    extras.addDir('','Upload Log','none','uploadlog', 'Log_File.png','','','')
    extras.addDir('','View My Log','none','log', 'View_Log.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Addon Menu
def Tutorials_Addon_Menu(url):
    extras.addDir('folder','[COLOR=yellow]1. Add-on Maintenance[/COLOR]', str(url)+'&type=Maintenance', 'grab_tutorials', 'Maintenance.png','','','')
    extras.addDir('folder','Audio Add-ons', str(url)+'&type=Audio', 'grab_tutorials', 'Audio.png','','','')
    extras.addDir('folder','Picture Add-ons', str(url)+'&type=Pictures', 'grab_tutorials', 'Pictures.png','','','')
    extras.addDir('folder','Program Add-ons', str(url)+'&type=Programs', 'grab_tutorials', 'Programs.png','','','')
    extras.addDir('folder','Video Add-ons', str(url)+'&type=Video', 'grab_tutorials', 'Video.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Root menu listings
def Tutorial_Root_Menu():
    extras.addDir('folder','[COLOR=yellow]Manual Search[/COLOR]', 'tutorials', 'manual_search', 'Manual_Search.png','','','')
    extras.addDir('folder','[COLOR=lime]All Guides[/COLOR] Everything in one place', '', 'grab_tutorials', 'All.png','','','')
    extras.addDir('folder','[COLOR=lime]XBMC / Kodi[/COLOR] Specific', '', 'xbmc_menu', 'XBMC.png','','','')
    extras.addDir('folder','[COLOR=lime]XBMC4Xbox[/COLOR] Specific', '&platform=XBMC4Xbox', 'xbmc_menu', 'XBMC4Xbox.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Android', '&platform=Android', 'platform_menu', 'Android.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Apple TV', '&platform=ATV', 'platform_menu', 'ATV.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] ATV2 & iOS', '&platform=iOS', 'platform_menu', 'iOS.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Linux', '&platform=Linux', 'platform_menu', 'Linux.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Pure Linux', '&platform=Custom_Linux', 'platform_menu', 'Custom_Linux.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] OpenELEC', '&platform=OpenELEC', 'platform_menu', 'OpenELEC.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] OSMC', '&platform=OSMC', 'platform_menu', 'OSMC.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] OSX', '&platform=OSX', 'platform_menu', 'OSX.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Raspbmc', '&platform=Raspbmc', 'platform_menu', 'Raspbmc.png','','','')
    extras.addDir('folder','[COLOR=orange][Platform][/COLOR] Windows', '&platform=Windows', 'platform_menu', 'Windows.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Allwinner Devices', '&hardware=Allwinner', 'platform_menu', 'Allwinner.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Amazon Fire TV', '&hardware=AFTV', 'platform_menu', 'AFTV.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] AMLogic Devices', '&hardware=AMLogic', 'platform_menu', 'AMLogic.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Boxee', '&hardware=Boxee', 'platform_menu', 'Boxee.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Intel Devices', '&hardware=Intel', 'platform_menu', 'Intel.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Raspberry Pi', '&hardware=RaspberryPi', 'platform_menu', 'RaspberryPi.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Rockchip Devices', '&hardware=Rockchip', 'platform_menu', 'Rockchip.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][Hardware][/COLOR] Xbox', '&hardware=Xbox', 'platform_menu', 'Xbox_Original.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Grab User Info
def User_Info(localbuildcheck,localversioncheck,localidcheck):
    BaseURL = 'http://totalxbmc.com/totalrevolution/login/login_details.php?user=%s&pass=%s' % (username, password)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    welcomematch = re.compile('login_msg="(.+?)"').findall(link)
    welcometext  = welcomematch[0] if (len(welcomematch) > 0) else ''
    Categories(localbuildcheck,localversioncheck,localidcheck,welcometext)
#-----------------------------------------------------------------------------------------------------------------
#Show User Info dialog
def Show_User_Info():
    BaseURL = 'http://totalxbmc.com/totalrevolution/login/login_details.php?user=%s&pass=%s' % (username, password)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    postsmatch = re.compile('posts="(.+?)"').findall(link)
    messagesmatch = re.compile('messages="(.+?)"').findall(link)
    unreadmatch = re.compile('unread="(.+?)"').findall(link)
    dobmatch = re.compile('DOB="(.+?)"').findall(link)
    emailmatch = re.compile('email="(.+?)"').findall(link)
    messages  = messagesmatch[0] if (len(messagesmatch) > 0) else ''
    unread  = unreadmatch[0] if (len(unreadmatch) > 0) else ''
    DOB  = dobmatch[0] if (len(dobmatch) > 0) else ''
    email  = emailmatch[0] if (len(emailmatch) > 0) else ''
    posts  = postsmatch[0] if (len(postsmatch) > 0) else ''
    dialog.ok('TotalXBMC Details for '+username,'DOB: '+DOB+'[CR]Email: '+email,'Unread Messages: '+unread+'/'+messages,'Posts: '+posts)
#-----------------------------------------------------------------------------------------------------------------
#Initial online check for new video
def Video_Check():
    vidcheckoption = ADDON.getSetting('startupvideo')
    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)
    if not os.path.exists(startuppath):
        localfile = open(startuppath, mode='w+')
        localfile.write('date="01011001"\nversion="0.0"')
        localfile.close()
    if not os.path.exists(idfile):
        localfile = open(idfile, mode='w+')
        localfile.write('id="None"\nname="None"')
        localfile.close()
    if trcheck == 'true':
        BaseURL='http://totalxbmc.com/totalrevolution/unlocked.txt'
    else:
        BaseURL='http://totalxbmc.com/totalrevolution/vanilla.txt'
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    datecheckmatch = re.compile('date="(.+?)"').findall(link)
    videomatch = re.compile('video="https://www.youtube.com/watch\?v=(.+?)"').findall(link)
    datecheck  = datecheckmatch[0] if (len(datecheckmatch) > 0) else ''
    videocheck  = videomatch[0] if (len(videomatch) > 0) else ''

    localfile = open(startuppath, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    localdatecheckmatch = re.compile('date="(.+?)"').findall(content)
    localdatecheck  = localdatecheckmatch[0] if (len(localdatecheckmatch) > 0) else ''
    localversionmatch = re.compile('version="(.+?)"').findall(content)
    localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
    localfile2 = open(idfile, mode='r')
    content2 = file.read(localfile2)
    file.close(localfile2)
    localidmatch = re.compile('id="(.+?)"').findall(content2)
    localidcheck  = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localbuildmatch = re.compile('name="(.+?)"').findall(content2)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    if  int(localdatecheck) < int(datecheck) and vidcheckoption == 'true':
        replacefile = content.replace(localdatecheck,datecheck)
        writefile = open(startuppath, mode='w')
        writefile.write(str(replacefile))
        writefile.close()
        yt.PlayVideo(videocheck, forcePlayer=True)
        xbmc.sleep(500)
        while xbmc.Player().isPlaying():
            xbmc.sleep(500)
    User_Info(localbuildcheck,localversioncheck,localidcheck)
#-----------------------------------------------------------------------------------------------------------------    
#Function to clear the addon_data
def Wipe_Kodi():
    mybackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds'))
    choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
    if choice == 1:
        if skin!= "skin.confluence":
            dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Please switch to the default Confluence skin','before performing a wipe.','')
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            return
        else:
            choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='No', nolabel='Yes')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = extras.Get_Keyboard( heading="Enter a name for this backup" )
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.TotalRevolution']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                communitybuilds.Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            choice = xbmcgui.Dialog().yesno("Remove TotalRevolution?", 'Do you also want to remove the TotalRevolution', 'add-on and have a complete fresh start or would you', 'prefer to keep this on your system?', yeslabel='Remove',nolabel='Keep')
            if choice == 0:
                cache.Remove_Textures()
                trpath = xbmc.translatePath(os.path.join(ADDONS,AddonID,''))
                trtemp = xbmc.translatePath(os.path.join(HOME,'..','totalrevolution.zip'))
                communitybuilds.Archive_File(trpath, trtemp)
                deppath = xbmc.translatePath(os.path.join(ADDONS,'script.module.addon.common',''))
                deptemp = xbmc.translatePath(os.path.join(HOME,'..','totalrevolutiondep.zip'))
                communitybuilds.Archive_File(deppath, deptemp)
                extras.Destroy_Path(HOME)
                if not os.path.exists(trpath):
                    os.makedirs(trpath)
                if not os.path.exists(deppath):
                    os.makedirs(deppath)
                time.sleep(1)
                communitybuilds.Read_Zip(trtemp)
                dp.create("[COLOR=blue]T[/COLOR][COLOR=white]otal[/COLOR][COLOR=dodgerblue]R[/COLOR][COLOR=white]evolutoin[/COLOR]","Checking ",'', 'Please Wait')
                dp.update(0,"", "Extracting Zip Please Wait")
                extract.all(trtemp,trpath,dp)
                communitybuilds.Read_Zip(deptemp)
                extract.all(deptemp,deppath,dp)
                dp.update(0,"", "Extracting Zip Please Wait")
                dp.close()
                time.sleep(1)
                extras.Kill_XBMC()
            elif choice == 1:
                cache.Remove_Textures()
                extras.Destroy_Path(HOME)
                dp.close()
                extras.Kill_XBMC()
            else: return
#-----------------------------------------------------------------------------------------------------------------    
#Maintenance section
def Wipe_Tools():
    extras.addDir('','Clear Cache','url','clear_cache','Clear_Cache.png','','','')
    extras.addDir('','Clear My Cached Artwork', 'none', 'remove_textures', 'Delete_Cached_Artwork.png','','','')
    extras.addDir('','Delete Addon_Data','url','remove_addon_data','Delete_Addon_Data.png','','','')
    extras.addDir('','Delete Old Builds/Zips From Device','url','remove_build','Delete_Builds.png','','','')
    extras.addDir('','Delete Old Crash Logs','url','remove_crash_logs','Delete_Crash_Logs.png','','','')
    extras.addDir('','Delete Packages Folder','url','remove_packages','Delete_Packages.png','','','')
    extras.addDir('','Wipe My Install (Fresh Start)', 'none', 'wipe_xbmc', 'Fresh_Start.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#XBMC/Kodi/XBMC4Xbox tutorials menu2
def XBMC_Menu(url):
    extras.addDir('folder','[COLOR=yellow]1. Install[/COLOR]', str(url)+'&tags=Install&XBMC=1', 'grab_tutorials', 'Install.png','','','')
    extras.addDir('folder','[COLOR=lime]2. Settings[/COLOR]', str(url)+'&tags=Settings', 'grab_tutorials', 'Settings.png','','','')
    extras.addDir('folder','[COLOR=orange]3. Add-ons[/COLOR]', str(url), 'tutorial_addon_menu', 'Addons.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Audio', str(url)+'&tags=Audio', 'grab_tutorials', 'Audio.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Errors', str(url)+'&tags=Errors', 'grab_tutorials', 'Errors.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Gaming', str(url)+'&tags=Gaming', 'grab_tutorials', 'gaming_portal.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  LiveTV', str(url)+'&tags=LiveTV', 'grab_tutorials', 'LiveTV.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Maintenance', str(url)+'&tags=Maintenance', 'grab_tutorials', 'Maintenance.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Pictures', str(url)+'&tags=Pictures', 'grab_tutorials', 'Pictures.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Profiles', str(url)+'&tags=Profiles', 'grab_tutorials', 'Profiles.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Skins', str(url)+'&tags=Skins', 'grab_tutorials', 'Skin.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Video', str(url)+'&tags=Video', 'grab_tutorials', 'Video.png','','','')
    extras.addDir('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Weather', str(url)+'&tags=Weather', 'grab_tutorials', 'Weather.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Addon starts here
params=Get_Params()
addon_id=None
audioaddons=None
author=None
buildname=None
data_path=None
description=None
DOB=None
email=None
fanart=None
forum=None
iconimage=None
link=None
local=None
messages=None
mode=None
name=None
posts=None
programaddons=None
provider_name=None
repo_id=None
repo_link=None
skins=None
sources=None
updated=None
unread=None
url=None
version=None
video=None
videoaddons=None
welcometext=None
zip_link=None

try:    addon_id=urllib.unquote_plus(params["addon_id"])
except: pass
try:    adult=urllib.unquote_plus(params["adult"])
except: pass
try:    audioaddons=urllib.unquote_plus(params["audioaddons"])
except: pass
try:    author=urllib.unquote_plus(params["author"])
except: pass
try:    buildname=urllib.unquote_plus(params["buildname"])
except: pass
try:    data_path=urllib.unquote_plus(params["data_path"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    DOB=urllib.unquote_plus(params["DOB"])
except: pass
try:    email=urllib.unquote_plus(params["email"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    forum=urllib.unquote_plus(params["forum"])
except: pass
try:    guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    link=urllib.unquote_plus(params["link"])
except: pass
try:    local=urllib.unquote_plus(params["local"])
except: pass
try:    messages=urllib.unquote_plus(params["messages"])
except: pass
try:    mode=str(params["mode"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except: pass
try:    posts=urllib.unquote_plus(params["posts"])
except: pass
try:    programaddons=urllib.unquote_plus(params["programaddons"])
except: pass
try:    provider_name=urllib.unquote_plus(params["provider_name"])
except: pass
try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: pass
try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: pass
try:    skins=urllib.unquote_plus(params["skins"])
except: pass
try:    sources=urllib.unquote_plus(params["sources"])
except: pass
try:    updated=urllib.unquote_plus(params["updated"])
except: pass
try:    unread=urllib.unquote_plus(params["unread"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    version=urllib.unquote_plus(params["version"])
except: pass
try:    video=urllib.unquote_plus(params["video"])
except: pass
try:    videoaddons=urllib.unquote_plus(params["videoaddons"])
except: pass
try:    welcometext=urllib.unquote_plus(params["welcometext"])
except: pass
try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: pass

if mode == None and trcheck == 'true': Video_Check()
elif mode == None                 : Categories('','','','')
elif mode == 'addon_final_menu'   : addons.Addon_Final_Menu(url)
elif mode == 'addon_categories'   : addons.Addon_Categories()
elif mode == 'addon_countries'    : addons.Addon_Countries()
elif mode == 'addon_genres'       : addons.Addon_Genres()
elif mode == 'addon_install'      : addons.Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
elif mode == 'addonfix'           : addonfix.fixes()
elif mode == 'addonfixes'         : Addon_Fixes()
elif mode == 'addonmenu'          : Addon_Menu()
elif mode == 'addon_settings'     : Addon_Settings()
elif mode == 'backup'             : BACKUP()
elif mode == 'backup_option'      : communitybuilds.Backup_Option()
elif mode == 'backup_restore'     : Backup_Restore()
elif mode == 'categories'         : Categories()
elif mode == 'check_storage'      : CheckPath.CheckPath()
elif mode == 'clear_cache'        : Clear_Cache()
elif mode == 'community'          : CB_Root_Menu()
elif mode == 'community_backup'   : communitybuilds.Community_Backup()
elif mode == 'community_menu'     : communitybuilds.Community_Menu(url,video)        
elif mode == 'countries'          : Countries(url)
elif mode == 'description'        : communitybuilds.Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
elif mode == 'fix_special'        : communitybuilds.Fix_Special(url)
elif mode == 'genres'             : Genres(url)
elif mode == 'gotham'             : extras.Gotham_Confirm()
elif mode == 'grab_addons'        : addons.Grab_Addons(url)
elif mode == 'grab_builds'        : communitybuilds.Grab_Builds(url)
elif mode == 'grab_builds_premium': communitybuilds.Grab_Builds_Premium(url)
elif mode == 'grab_hardware'      : news.Grab_Hardware(url)
elif mode == 'grab_news'          : news.Grab_News(url)
elif mode == 'grab_tutorials'     : news.Grab_Tutorials(url)
elif mode == 'guisettingsfix'     : communitybuilds.GUI_Settings_Fix(url,local)
elif mode == 'hardware_filter_menu': Hardware_Filter_Menu(url)
elif mode == 'hardware_final_menu': news.Hardware_Menu(url)        
elif mode == 'hardware_root_menu' : Hardware_Root_Menu()       
elif mode == 'helix'              : extras.Helix_Confirm()
elif mode == 'hide_passwords'     : extras.Hide_Passwords()
elif mode == 'ipcheck'            : extras.IP_Check()
elif mode == 'instructions'       : Instructions()
elif mode == 'instructions_1'     : Instructions_1()
elif mode == 'instructions_2'     : Instructions_2()
elif mode == 'instructions_3'     : Instructions_3()
elif mode == 'instructions_4'     : Instructions_4()
elif mode == 'instructions_5'     : Instructions_5()
elif mode == 'instructions_6'     : Instructions_6()
elif mode == 'LocalGUIDialog'     : communitybuilds.Local_GUI_Dialog()
elif mode == 'log'                : extras.Log_Viewer()
elif mode == 'manual_search'      : extras.Manual_Search(url)
elif mode == 'manual_search_builds': extras.Manual_Search_Builds()
elif mode == 'news_root_menu'     : News_Root_Menu(url)
elif mode == 'news_menu'          : news.News_Menu(url)
elif mode == 'play_video'         : yt.PlayVideo(url)
elif mode == 'platform_menu'      : Platform_Menu(url)
elif mode == 'popular'            : popularpacks.Popular()
elif mode == 'register'           : Register()
elif mode == 'remove_addon_data'  : Remove_Addon_Data()
elif mode == 'remove_addons'      : extras.Remove_Addons(url)
elif mode == 'remove_build'       : extras.Remove_Build()
elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
elif mode == 'remove_packages'    : Remove_Packages()
elif mode == 'remove_textures'    : Remove_Textures()
elif mode == 'restore'            : extras.RESTORE()
elif mode == 'restore_backup'     : communitybuilds.Restore_Backup_XML(name,url,description)
elif mode == 'restore_local_CB'   : communitybuilds.Restore_Local_Community()
elif mode == 'restore_local_gui'  : communitybuilds.Restore_Local_GUI()
elif mode == 'restore_option'     : communitybuilds.Restore_Option()
elif mode == 'restore_zip'        : communitybuilds.Restore_Zip_File(url)         
elif mode == 'restore_community'  : communitybuilds.Restore_Community(name,url,video,description,skins,guisettingslink)        
elif mode == 'runtest'            : speedtest.runtest(url)
elif mode == 'search_addons'      : addons.Search_Addons(url)
elif mode == 'search_builds'      : communitybuilds.Search_Builds(url)
elif mode == 'Search_Private'     : Private_Search(url)
elif mode == 'showinfo'           : communitybuilds.Show_Info(url)
elif mode == 'SortBy'             : extras.Sort_By(BuildURL,type)
elif mode == 'speed_instructions' : Speed_Instructions()
elif mode == 'speedtest_menu'     : Speed_Test_Menu()
elif mode == 'text_guide'         : news.Text_Guide(name,url)
elif mode == 'tools'              : Tools()
elif mode == 'tutorial_final_menu': news.Tutorial_Menu(url)        
elif mode == 'tutorial_addon_menu': Tutorials_Addon_Menu(url)        
elif mode == 'tutorial_root_menu' : Tutorial_Root_Menu()        
elif mode == 'unhide_passwords'   : extras.Unhide_Passwords()
elif mode == 'update'             : addons.Update_Repo()
elif mode == 'uploadlog'          : extras.Upload_Log()
elif mode == 'user_info'          : Show_User_Info()
elif mode == 'wipetools'          : Wipe_Tools()
elif mode == 'xbmc_menu'          : XBMC_Menu(url)
elif mode == 'xbmcversion'        : extras.XBMC_Version(url)
elif mode == 'wipe_xbmc'          : Wipe_Kodi()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
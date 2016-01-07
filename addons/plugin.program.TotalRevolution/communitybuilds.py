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
import extras
import shutil
import urllib2,urllib
import re
import extract
import time
import CheckPath
import downloader
import zipfile
import ntpath

ARTPATH      =  'http://totalxbmc.com/totalrevolution/art/' + os.sep
ADDON        =  xbmcaddon.Addon(id='plugin.program.TotalRevolution')
AddonID      =  'plugin.program.TotalRevolution'
AddonTitle   =  "[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]"
zip          =  ADDON.getSetting('zip')
localcopy    =  ADDON.getSetting('localcopy')
privatebuilds=  ADDON.getSetting('private')
reseller     =  ADDON.getSetting('reseller')
resellername =  ADDON.getSetting('resellername')
resellerid   =  ADDON.getSetting('resellerid')
mastercopy   =  ADDON.getSetting('mastercopy')
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
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
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
startuppath  =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'startup.xml'))
tempfile     =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'temp.xml'))
idfile       =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'id.xml'))
idfiletemp   =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'idtemp.xml'))
skin         =  xbmc.getSkinDir()
username     =  ADDON.getSetting('username')
password     =  ADDON.getSetting('password')
login        =  ADDON.getSetting('login')
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
GUINEW       =  xbmc.translatePath(os.path.join(userdatafolder,'guinew.xml'))
guitemp      =  xbmc.translatePath(os.path.join(userdatafolder,'guitemp',''))
tempdbpath   =  xbmc.translatePath(os.path.join(USB,'Database'))
urlbase      =  'None'

#---------------------------------------------------------------------------------------------------
#Main addDirectory function - xbmcplugin.addDirectoryItem()
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------
#Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
def Add_Build_Dir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)+"&skins="+urllib.quote_plus(skins)+"&guisettingslink="+urllib.quote_plus(guisettingslink)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
#---------------------------------------------------------------------------------------------------
#Add a directory for the description, this requires multiple string to be called from previous menu
def Add_Desc_Dir(name,url,mode,iconimage,fanart,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
        iconimage = ARTPATH + iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&author="+urllib.quote_plus(author)+"&description="+urllib.quote_plus(description)+"&version="+urllib.quote_plus(version)+"&buildname="+urllib.quote_plus(buildname)+"&updated="+urllib.quote_plus(updated)+"&skins="+urllib.quote_plus(skins)+"&videoaddons="+urllib.quote_plus(videoaddons)+"&audioaddons="+urllib.quote_plus(audioaddons)+"&buildname="+urllib.quote_plus(buildname)+"&programaddons="+urllib.quote_plus(programaddons)+"&pictureaddons="+urllib.quote_plus(pictureaddons)+"&sources="+urllib.quote_plus(sources)+"&adult="+urllib.quote_plus(adult)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
#---------------------------------------------------------------------------------------------------
#Zip up tree
def Archive_Tree(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.TotalRevolution' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
#Zip up tree
def Archive_File(sourcefile, destfile):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Archiving...",'', 'Please Wait')
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.TotalRevolution' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
#Create backup menu
def Backup_Option():
    extras.addDir('','[COLOR=lime]Full Backup[/COLOR]','url','community_backup','Backup.png','','','Back Up Your Full System')
    extras.addDir('','Backup Just Your Addons','addons','restore_zip','Backup.png','','','Back Up Your Addons')
    extras.addDir('','Backup Just Your Addon UserData','addon_data','restore_zip','Backup.png','','','Back Up Your Addon Userdata')
    extras.addDir('','Backup Guisettings.xml',GUI,'restore_backup','Backup.png','','','Back Up Your guisettings.xml')
    if os.path.exists(FAVS):
        extras.addDir('','Backup Favourites.xml',FAVS,'restore_backup','Backup.png','','','Back Up Your favourites.xml')
    if os.path.exists(SOURCE):
        extras.addDir('','Backup Source.xml',SOURCE,'restore_backup','Backup.png','','','Back Up Your sources.xml')
    if os.path.exists(ADVANCED):
        extras.addDir('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','Backup.png','','','Back Up Your advancedsettings.xml')
    if os.path.exists(KEYMAPS):
        extras.addDir('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','Backup.png','','','Back Up Your keyboard.xml')
    if os.path.exists(RSS):
        extras.addDir('','Backup RssFeeds.xml',RSS,'restore_backup','Backup.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def Check_Download_Path():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    if not os.path.exists(zip):
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','The download location you have stored does not exist .\nPlease update the addon settings and try again.','','')        
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
#Create restore menu
def Check_Local_Install():
    localfile = open(idfile, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    localbuildmatch = re.compile('name="(.+?)"').findall(content)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    if localbuildcheck == "Incomplete":
        choice = xbmcgui.Dialog().yesno("Finish Restore Process", 'If you\'re certain the correct skin has now been set click OK', 'to finish the install process, once complete XBMC/Kodi will', ' then close. Do you want to finish the install process?', yeslabel='Yes',nolabel='No')
        if choice == 1:
            Finish_Local_Restore()
        elif choice ==0:
            return
#---------------------------------------------------------------------------------------------------
#Check whether or not the guisettings fix has been done, loops on a timer.
def Check_GUI_Temp(url):
    time.sleep(120)
    if os.path.exists(guitemp):
        choice = xbmcgui.Dialog().yesno('Run step 2 of install', 'You still haven\'t completed step 2 of the', 'install. Would you like to complete it now?', '', nolabel='No, not yet',yeslabel='Yes, complete setup')
        if choice == 0:
            Check_GUI_Temp(url)
        elif choice == 1:
            try: xbmc.executebuiltin("PlayerControl(Stop)")       
            except: pass
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            GUI_Merge(url)
#---------------------------------------------------------------------------------------------------
#Create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def Community_Backup():
    guisuccess=1
    Check_Download_Path()
    fullbackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds',''))
    myfullbackup = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds','my_full_backup.zip'))
    myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds','my_full_backup_GUI_Settings.zip'))
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    vq = extras.Get_Keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full =  ['plugin.program.TotalRevolution']
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
    exclude_dirs =  ['plugin.program.TotalRevolution', 'plugin.program.community.builds','cache', 'system', 'Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml']
    message_header = "Creating full backup of existing build"
    message_header2 = "Creating Community Build"
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    if mastercopy=='true':
        Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords.', 'If you\'re intending on sharing this with others we stongly', 'recommend against this unless all data has been manually removed.', yeslabel='Yes',nolabel='No')
    if choice == 0:
        DeleteAddonData()
    elif choice == 1:
        pass
    Fix_Special(HOME)
    Delete_Packages()
    Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
    zf = zipfile.ZipFile(GUIname, mode='w')
    try:
        zf.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    except: guisuccess=0
    try:
        zf.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except: pass
    zf.close()
    if mastercopy=='true':
        zfgui = zipfile.ZipFile(myfullbackupGUI, mode='w')
        try:
            zfgui.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
        except: guisuccess=0

        try:
            zfgui.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
        except: pass
        zfgui.close()
    if guisuccess == 0:
        dialog.ok("FAILED!", 'The guisettings.xml file could not be found on your', 'system, please reboot and try again.', '')
    else:
        dialog.ok("SUCCESS!", 'You Are Now Backed Up. If you\'d like to share this build with', 'the community please post details on the forum at', '[COLOR=lime][B]www.totalxbmc.tv[/COLOR][/B]')
        dialog.ok("Build Locations", 'Full Backup (only used to restore on this device): [COLOR=yellow]'+myfullbackup, '[/COLOR]Universal Backup (can be used on any device): [COLOR=yellow]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Community_Menu(url,video):
    check1=0
    BaseURL='http://totalxbmc.com/totalrevolution/Community_Builds/community_builds_premium.php?id=%s' % (url)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    pathmatch = re.compile('path="(.+?)"').findall(link)
    artpathmatch = re.compile('myart="(.+?)"').findall(link)
    videopreviewmatch = re.compile('videopreview="(.+?)"').findall(link)
    videoguide1match = re.compile('videoguide1="(.+?)"').findall(link)
    videoguide2match = re.compile('videoguide2="(.+?)"').findall(link)
    videoguide3match = re.compile('videoguide3="(.+?)"').findall(link)
    videoguide4match = re.compile('videoguide4="(.+?)"').findall(link)
    videoguide5match = re.compile('videoguide5="(.+?)"').findall(link)
    videolabel1match = re.compile('videolabel1="(.+?)"').findall(link)
    videolabel2match = re.compile('videolabel2="(.+?)"').findall(link)
    videolabel3match = re.compile('videolabel3="(.+?)"').findall(link)
    videolabel4match = re.compile('videolabel4="(.+?)"').findall(link)
    videolabel5match = re.compile('videolabel5="(.+?)"').findall(link)
    namematch = re.compile('name="(.+?)"').findall(link)
    authormatch = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    descmatch = re.compile('description="(.+?)"').findall(link)
    downloadmatch = re.compile('DownloadURL="(.+?)"').findall(link)
    updatedmatch = re.compile('updated="(.+?)"').findall(link)
    defaultskinmatch = re.compile('defaultskin="(.+?)"').findall(link)
    skinsmatch = re.compile('skins="(.+?)"').findall(link)
    videoaddonsmatch = re.compile('videoaddons="(.+?)"').findall(link)
    audioaddonsmatch = re.compile('audioaddons="(.+?)"').findall(link)
    programaddonsmatch = re.compile('programaddons="(.+?)"').findall(link)
    pictureaddonsmatch = re.compile('pictureaddons="(.+?)"').findall(link)
    sourcesmatch = re.compile('sources="(.+?)"').findall(link)
    adultmatch = re.compile('adult="(.+?)"').findall(link)
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
   
    artpath  = artpathmatch[0] if (len(artpathmatch) > 0) else ''
    path  = pathmatch[0] if (len(pathmatch) > 0) else ''
    name  = namematch[0] if (len(namematch) > 0) else ''
    author  = authormatch[0] if (len(authormatch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
    description  = descmatch[0] if (len(descmatch) > 0) else 'No information available'
    updated = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    defaultskin = defaultskinmatch[0] if (len(defaultskinmatch) > 0) else ''
    skins = skinsmatch[0] if (len(skinsmatch) > 0) else ''
    videoaddons = videoaddonsmatch[0] if (len(videoaddonsmatch) > 0) else ''
    audioaddons = audioaddonsmatch[0] if (len(audioaddonsmatch) > 0) else ''
    programaddons = programaddonsmatch[0] if (len(programaddonsmatch) > 0) else ''
    pictureaddons = pictureaddonsmatch[0] if (len(pictureaddonsmatch) > 0) else ''
    sources = sourcesmatch[0] if (len(sourcesmatch) > 0) else ''
    adult = adultmatch[0] if (len(adultmatch) > 0) else ''
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    downloadURL  = downloadmatch[0] if (len(downloadmatch) > 0) else 'None'
    videopreview  = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide1  = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2  = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3  = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4  = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5  = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1  = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2  = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3  = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4  = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5  = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    localfile = open(tempfile, mode='w+')
    localfile.write('id="'+str(video)+'"\nname="'+name+'"\nversion="'+version+'"')
    localfile.close()
    Add_Desc_Dir('Full description','None','description','BUILDDETAILS.png',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    if videopreview != 'None':
        extras.addDir('','Watch Preview Video',videopreview,'play_video','Video_Preview.png',fanart,'','')
    if videoguide1 != 'None':
        extras.addDir('','(VIDEO) '+videolabel1,videoguide1,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide2 != 'None':
        extras.addDir('','(VIDEO) '+videolabel2,videoguide2,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide3 != 'None':
        extras.addDir('','(VIDEO) '+videolabel3,videoguide3,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide4 != 'None':
        extras.addDir('','(VIDEO) '+videolabel4,videoguide4,'play_video','Video_Guide.png',fanart,'','')    
    if videoguide5 != 'None':
        extras.addDir('','(VIDEO) '+videolabel5,videoguide5,'play_video','Video_Guide.png',fanart,'','')    
    if downloadURL=='None':
        Add_Build_Dir('[COLOR=gold]Sorry this build is currently unavailable[/COLOR]','','','','','','','','')
    if BaseURL.endswith("visibility=premium") or BaseURL.endswith("visibility=reseller_private"):
        if (path!='') and (path!='fail') and (os.path.exists(path)):
            Add_Build_Dir('[COLOR=lime]Install Part 1: Download '+name+'[/COLOR]',downloadURL,'restore_community',iconimage,fanart,artpath,name,defaultskin,guisettingslink)
        if ((path!='') and not os.path.exists(path) and (path!='fail')):
            check1=1
            dialog.ok("Security check failed, contact box seller", 'This box cannot be identified as an official', '[COLOR=lime]'+resellername+'[/COLOR] product. Please contact the', 'seller you purchased this device from for more details.')
        if path=='fail':
            check1=1
            dialog.ok("Subscription not paid", 'The box seller has either opted out of the premium', 'plan or has unpaid debts to the Community Builders.', 'Please contact the seller you purchased this device from for more details.')
        if path=='':
            Add_Build_Dir('[COLOR=lime]Install Part 1: Download '+name+'[/COLOR]',downloadURL,'restore_community',iconimage,fanart,path,name,defaultskin,guisettingslink)
    else:
        Add_Build_Dir('[COLOR=lime]Install Part 1: Download '+name+'[/COLOR]',downloadURL,'restore_community',iconimage,fanart,'',name,defaultskin,guisettingslink)
    if check1==0:
        if guisettingslink=='None':
            pass
        else:
            extras.addDir('','[COLOR=dodgerblue]Install Part 2: Apply guisettings.xml fix[/COLOR]',guisettingslink,'guisettingsfix','FixMy_Build.png',fanart,'','')
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def DeleteAddonData():
    print '############################################################       DELETING USERDATA             ###############################################################'
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
    # Count files and give option to delete
        if file_count >= 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#---------------------------------------------------------------------------------------------------
#Delete Packages Folder
def Delete_Packages():
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
    # Count files and give option to delete
        if file_count > 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
#Show full description of build
def Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
    extras.Text_Boxes(buildname+'     v.'+version, '[COLOR=yellow][B]Author:   [/B][/COLOR]'+author+'[COLOR=yellow][B]               Last Updated:   [/B][/COLOR]'+updated+'[COLOR=yellow][B]               Adult Content:   [/B][/COLOR]'+adult+'[CR][CR][COLOR=yellow][B]Description:[CR][/B][/COLOR]'+description+
    '[CR][CR][COLOR=blue][B]Skins:   [/B][/COLOR]'+skins+'[CR][CR][COLOR=blue][B]Video Addons:   [/B][/COLOR]'+videoaddons+'[CR][CR][COLOR=blue][B]Audio Addons:   [/B][/COLOR]'+audioaddons+
    '[CR][CR][COLOR=blue][B]Program Addons:   [/B][/COLOR]'+programaddons+'[CR][CR][COLOR=blue][B]Picture Addons:   [/B][/COLOR]'+pictureaddons+'[CR][CR][COLOR=blue][B]Sources:   [/B][/COLOR]'+sources+
    '[CR][CR][COLOR=gold]Disclaimer: [/COLOR]These are community builds and they may overwrite some of your existing settings, '
    'TotalXBMC take no responsibility over what content is included in these builds, it\'s up to the individual who uploads the build to state what\'s included and then the users decision to decide whether or not that content is suitable for them.')
#---------------------------------------------------------------------------------------------------
def Finish_Local_Restore():
    os.remove(idfile)
    os.rename(idfiletemp,idfile)
    xbmc.executebuiltin('UnloadSkin')    
    xbmc.executebuiltin("ReloadSkin")
    dialog.ok("Local Restore Complete", 'XBMC/Kodi will now close.', '', '')
    xbmc.executebuiltin("Quit")      
#---------------------------------------------------------------------------------------------------
#Convert physical paths to special paths
def Fix_Special(url):
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(USERDATA, 'special://profile/').replace(ADDONS,'special://home/addons/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Builds(url):
    if zip == '':
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        xbmcversion = 'gotham'
    else:
        xbmcversion = 'helix'

    if ADDON.getSetting('adult') == 'true':
        adult = ''
    else:
        adult = 'no'
    buildsURL = 'http://totalxbmc.com/totalrevolution/Community_Builds/sortby.php?sortx=name&orderx=ASC&xbmc=%s&adult=%s&%s' % (xbmcversion, adult, url)
    link = extras.Open_URL(buildsURL).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)" <br> id="(.+?)" <br> Thumbnail="(.+?)" <br> Fanart="(.+?)" <br> downloads="(.+?)" <br> <br>', re.DOTALL).findall(link)
    extras.Sort_By(url,'communitybuilds')
    for name,id,Thumbnail,Fanart,downloads in match:
        Add_Build_Dir(name+'[COLOR=lime] ('+downloads+' downloads)[/COLOR]',id+url,'community_menu',Thumbnail,Fanart,id,'','','')
#---------------------------------------------------------------------------------------------------
#Option to download guisettings fix that merges with existing settings.
def GUI_Settings_Fix(url,local):
    Check_Download_Path()
    choice = xbmcgui.Dialog().yesno(name, 'This will over-write your existing guisettings.xml.', 'Are you sure this is the build you have installed?', '', nolabel='No, Cancel',yeslabel='Yes, Fix')
    if choice == 0:
        return
    elif choice == 1:
        GUI_Merge(url,local)
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def GUI_Merge(url,local):
    profiles_included=0
    keep_profiles=1
    if os.path.exists(GUINEW):
        os.remove(GUINEW)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if os.path.exists(PROFILES):
        os.remove(PROFILES)
    if not os.path.exists(guitemp):
        os.makedirs(guitemp)
    dp.create("Community Builds","Downloading guisettings.xml",'', 'Please Wait')
    shutil.copyfile(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    if local!=1:
        lib=os.path.join(USB, 'guifix.zip')
        downloader.download(url, lib, dp) #Download guisettings from the build
    else:
        lib=xbmc.translatePath(url)
    Read_Zip(lib)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,guitemp,dp)
    try:
        readfile = open(guitemp+'profiles.xml', mode='r')
        default_contents = readfile.read()
        readfile.close()
        if os.path.exists(guitemp+'profiles.xml'):
            choice = xbmcgui.Dialog().yesno("PROFILES DETECTED", 'This build has profiles included, would you like to overwrite', 'your existing profiles or keep the ones you have?', '', nolabel='Keep my profiles',yeslabel='Use new profiles')
            if choice == 0:
                pass
            elif choice == 1:
                writefile = open(PROFILES, mode='w')
                time.sleep(1)
                writefile.write(default_contents)
                time.sleep(1)
                writefile.close()
                keep_profiles=0
    except: print"no profiles.xml file"
    os.rename(guitemp+'guisettings.xml',GUIFIX) #Copy to addon_data folder so profiles can be dealt with
 # had to move elsewhere in case a profiles.xml is included  os.rename(GUI,GUIFIX) 
    time.sleep(1)
    localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    content = file.read(localfile)
    file.close(localfile)
    skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
    skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
    skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
    skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
    lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
    lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
    localfile2 = open(GUIFIX, mode='r')
    content2 = file.read(localfile2)
    file.close(localfile2)
    skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
    skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
    skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
    skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
    lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
    lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
    replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
    writefile = open(GUINEW, mode='w+')
    writefile.write(str(replacefile))
    writefile.close()
    if os.path.exists(GUI):
        try:
            os.remove(GUI)
            success=True
        except:
            dialog.ok("Oops we have a problem", 'There was an error trying to complete this process.', 'Please try this step again, if it still fails you may', 'need to restart Kodi and try again.')
            success=False
    try:
        os.rename(GUINEW,GUI)
        os.remove(GUIFIX)
    except:
        pass
    if success==True:
        try:
            localfile = open(tempfile, mode='r')
            content = file.read(localfile)
            file.close(localfile)
            temp = re.compile('id="(.+?)"').findall(content)
            tempcheck  = temp[0] if (len(temp) > 0) else ''
            tempname = re.compile('name="(.+?)"').findall(content)
            namecheck  = tempname[0] if (len(tempname) > 0) else ''
            tempversion = re.compile('version="(.+?)"').findall(content)
            versioncheck  = tempversion[0] if (len(tempversion) > 0) else ''
            writefile = open(idfile, mode='w+')
            writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"')
            writefile.close()
            localfile = open(startuppath, mode='r')
            content = file.read(localfile)
            file.close(localfile)
            localversionmatch = re.compile('version="(.+?)"').findall(content)
            localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
            replacefile = content.replace(localversioncheck,versioncheck)
            writefile = open(startuppath, mode='w')
            writefile.write(str(replacefile))
            writefile.close()
            os.remove(tempfile)
        except:
            writefile = open(idfile, mode='w+')
            writefile.write('id="None"\nname="Unknown"\nversion="Unknown"')
            writefile.close()                
    if os.path.exists(guitemp+'profiles.xml'):
        os.remove(guitemp+'profiles.xml')
    if keep_profiles==0:
        dialog.ok("PROFILES DETECTED", 'Unfortunately the only way to get the new profiles to stick is', 'to force close kodi. Either do this via the task manager,', 'terminal or system settings. DO NOT use the quit/exit options in Kodi.')
        extras.Kill_XBMC()
    else:
        if success==True:
            dialog.ok("guisettings.xml fix complete", 'Please restart Kodi. If the skin doesn\'t look', 'quite right on the next boot you may need to', 'force close Kodi.')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def INSTALL_PART2(url):
    BaseURL='http://totalxbmc.com/totalrevolution/Community_Builds/guisettings.php?id=%s' % (url)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    GUI_Merge(guisettingslink,local)
#---------------------------------------------------------------------------------------------------
#Installs special art for premium.
def Install_Art(path):
    background_art = xbmc.translatePath(os.path.join(USERDATA,'background_art',''))
    if not os.path.exists(background_art):
        os.makedirs(background_art)
    try:
        dp.create("Installing Artwork","Downloading artwork pack",'', 'Please Wait')
        artpack=os.path.join(USB, resellername+'_artpack.zip')
        downloader.download(path, artpack, dp)
        time.sleep(1)
#        Read_Zip(artpack)
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(artpack,background_art,dp)
    except: pass
#---------------------------------------------------------------------------------------------------
# Dialog to warn users about local guisettings fix.
def Local_GUI_Dialog():
    dialog.ok("Restore local guisettings fix", "You should [COLOR=lime]ONLY[/COLOR] use this option if the guisettings fix", "is failing to download via the addon. Installing via this","method means you do not receive notifications of updates")
    Restore_Local_GUI()
#---------------------------------------------------------------------------------------------------
#Read a zip file and extract the relevant data
def Read_Zip(url):
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():
        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match=re.compile(r).findall(a)
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))
        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()
        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()
        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()
        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()
        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()                              
#---------------------------------------------------------------------------------------------------
#Function to restore a backup xml file (guisettings, sources, RSS)
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    else:
        if 'guisettings.xml' in description:
            a = open(os.path.join(USB,description.split('Your ')[1])).read()
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match=re.compile(r).findall(a)
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        else:    
            TO_WRITE   = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  
    dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "", 'All Done !','')
#---------------------------------------------------------------------------------------------------
#Function to restore a community build
def Restore_Community(name,url,video,description,skins,guisettingslink):
    choice4=1
    Check_Download_Path()
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if not os.path.exists(tempfile): #Function for debugging, creates a file that was created in previous call and subsequently deleted when run
        localfile = open(tempfile, mode='w+')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    try: os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return
    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before', 'installing any community builds.', 'Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        mybackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds'))
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
        Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database', 'files or overwrite? Overwriting will wipe any', 'existing library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
    if choice3 == 0: pass
    elif choice3 == 1:
        if os.path.exists(tempdbpath):
            shutil.rmtree(tempdbpath)
        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases.', 'Continuing may wipe your existing library. Do you', 'wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            if choice4 == 1: pass
            if choice4 == 0: return
        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    if choice4 == 0: return
    time.sleep(1)
    dp.create("Community Builds","Downloading "+description +" build.",'', 'Please Wait')
    lib=os.path.join(CBPATH, description+'.zip')
    if not os.path.exists(CBPATH):
        os.makedirs(CBPATH)
    downloader.download(url, lib, dp)
    readfile = open(CBADDONPATH, mode='r')
    default_contents = readfile.read()
    readfile.close()
    Read_Zip(lib)
    dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,HOME,dp)
    time.sleep(1)
    artpath=str(video)
    if video!='':
        Install_Art(artpath)
    localfile = open(tempfile, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    temp = re.compile('id="(.+?)"').findall(content)
    tempcheck  = temp[0] if (len(temp) > 0) else ''
    tempname = re.compile('name="(.+?)"').findall(content)
    namecheck  = tempname[0] if (len(tempname) > 0) else ''
    tempversion = re.compile('version="(.+?)"').findall(content)
    versioncheck  = tempversion[0] if (len(tempversion) > 0) else ''
    writefile = open(idfile, mode='w+')
    writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="'+versioncheck+'"')
    writefile.close()
    incremental = 'http://totalxbmc.com/totalrevolution/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
    extras.Open_URL(incremental)
    localfile = open(startuppath, mode='r')
    content = file.read(localfile)
    file.close(localfile)
    localversionmatch = re.compile('version="(.+?)"').findall(content)
    localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
    replacefile = content.replace(localversioncheck,versioncheck)
    writefile = open(startuppath, mode='w')
    writefile.write(str(replacefile))
    writefile.close()
    os.remove(tempfile)
    if localcopy == 'false':
        os.remove(lib)
    cbdefaultpy = open(CBADDONPATH, mode='w+')
    cbdefaultpy.write(default_contents)
    cbdefaultpy.close()
    try:
        os.rename(GUI,GUIFIX)
    except:
        print"NO GUISETTINGS DOWNLOADED"
    time.sleep(1)
    localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    content = file.read(localfile)
    file.close(localfile)
    skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
    skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
    skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
    skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
    lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
    lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
    try:
        localfile2 = open(GUIFIX, mode='r')
        content2 = file.read(localfile2)
        file.close(localfile2)
        skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
        skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
        skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
        skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
        lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
        lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
        replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
        writefile = open(GUINEW, mode='w+')
        writefile.write(str(replacefile))
        writefile.close()
    except:
        print"NO GUISETTINGS DOWNLOADED"
    if os.path.exists(GUI):
        os.remove(GUI)
    os.rename(GUINEW,GUI)
    try:
        os.remove(GUIFIX)
    except:
        pass
    if choice3 == 1:
        extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
        if choice4 !=1:
            shutil.rmtree(tempdbpath)
    #    os.remove(backup_zip)
    dp.close()
    os.makedirs(guitemp)
    time.sleep(1)
    xbmc.executebuiltin('UnloadSkin()') 
    time.sleep(1)
    xbmc.executebuiltin('ReloadSkin()')
    time.sleep(1)
    xbmc.executebuiltin("ActivateWindow(appearancesettings)")
    while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
        xbmc.sleep(500)
    try: xbmc.executebuiltin("LoadProfile(Master user)")
    except: pass
    dialog.ok('Step 1 complete','Change the skin to: [COLOR=lime]'+skins,'[/COLOR]Once done come back and choose install step 2 which will','re-install the guisettings.xml - this file contains all custom skin settings.')
    xbmc.executebuiltin("ActivateWindow(appearancesettings)")
    Check_GUI_Temp(guisettingslink)
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of a CB file
#### THIS CODE BLOCK SHOULD BE MERGED INTO THE RESTORE_COMMUNITY FUNCTION BUT I RAN OUT OF TIME TO DO IT CLEANLY ###
def Restore_Local_Community():
    exitfunction=0
    choice4=0
    extras.pop()
    Check_Download_Path()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
    if filename == '':
        return
    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    if not os.path.exists(tempfile): #Function for debugging, creates a file that was created in previous call and subsequently deleted when run
        localfile = open(tempfile, mode='w+')
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    try: os.rename(GUI,GUINEW) #Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return
    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before', 'installing any builds.', 'Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        mybackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds'))
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
        Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database', 'files or overwrite? Overwriting will wipe any', 'existing music or video library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
    if choice3 == 0: pass
    elif choice3 == 1:
        if os.path.exists(tempdbpath):
            shutil.rmtree(tempdbpath)
        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases.', 'Continuing may wipe your existing library. Do you', 'wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            if choice4 == 1: pass
            if choice4 == 0: exitfunction=1;return
        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    if exitfunction == 1:
        return
    else:
        time.sleep(1)
        readfile = open(CBADDONPATH, mode='r')
        default_contents = readfile.read()
        readfile.close()
        Read_Zip(filename)
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(filename,HOME,dp)
        time.sleep(1)
        clean_title = ntpath.basename(filename)
        writefile = open(idfile, mode='w+')
        writefile.write('id="none"\nname="'+clean_title+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="none"')
        writefile.close()
        cbdefaultpy = open(CBADDONPATH, mode='w+')
        cbdefaultpy.write(default_contents)
        cbdefaultpy.close()
        try:
            os.rename(GUI,GUIFIX)
        except:
            print"NO GUISETTINGS DOWNLOADED"
        time.sleep(1)
        localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
        content = file.read(localfile)
        file.close(localfile)
        skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''
        try:
            localfile2 = open(GUIFIX, mode='r')
            content2 = file.read(localfile2)
            file.close(localfile2)
            skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
            skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
            skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
            skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
            lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
            lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
            replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
            writefile = open(GUINEW, mode='w+')
            writefile.write(str(replacefile))
            writefile.close()
        except:
            print"NO GUISETTINGS DOWNLOADED"
        if os.path.exists(GUI):
            os.remove(GUI)
        os.rename(GUINEW,GUI)
        try:
            os.remove(GUIFIX)
        except:
            pass
        if choice3 == 1:
            extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
            if choice4 !=1:
                shutil.rmtree(tempdbpath)
        os.makedirs(guitemp)
        time.sleep(1)
        xbmc.executebuiltin('UnloadSkin()') 
        time.sleep(1)
        xbmc.executebuiltin('ReloadSkin()')
        time.sleep(1)
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        while xbmc.executebuiltin("Window.IsActive(appearancesettings)"):
            xbmc.sleep(500)
        try: xbmc.executebuiltin("LoadProfile(Master user)")
        except: pass
        dialog.ok('[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]','Step 1 complete. Now please change the skin to','the one this build was designed for. Once done come back','to this addon and restore the guisettings_fix.zip')        
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of guisettings_fix
def Restore_Local_GUI():
    import time
    Check_Download_Path()
    guifilename = xbmcgui.Dialog().browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)
    if guifilename == '':
        return
    else:
        local=1
        GUI_Settings_Fix(guifilename,local)  
#---------------------------------------------------------------------------------------------------
#Create restore menu
def Restore_Option():
    if trcheck == 'true':
        Check_Local_Install()
    extras.addDir('','[COLOR=lime]RESTORE LOCAL BUILD[/COLOR]','url','restore_local_CB','Restore.png','','','Back Up Your Full System')
    extras.addDir('','[COLOR=dodgerblue]Restore Local guisettings file[/COLOR]','url','LocalGUIDialog','Restore.png','','','Back Up Your Full System')
    
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        extras.addDir('','Restore Your Addons','addons','restore_zip','Restore.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        extras.addDir('','Restore Your Addon UserData','addon_data','restore_zip','Restore.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        extras.addDir('','Restore Guisettings.xml',GUI,'resore_backup','Restore.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        extras.addDir('','Restore Favourites.xml',FAVS,'resore_backup','Restore.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        extras.addDir('','Restore Source.xml',SOURCE,'resore_backup','Restore.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        extras.addDir('','Restore Advancedsettings.xml',ADVANCED,'resore_backup','Restore.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        extras.addDir('','Restore Advancedsettings.xml',KEYMAPS,'resore_backup','Restore.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        extras.addDir('','Restore RssFeeds.xml',RSS,'resore_backup','Restore.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
#Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR = ADDONS
        to_backup = ADDONS
        backup_zip = xbmc.translatePath(os.path.join(USB,'addons.zip'))
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA
    if 'Backup' in name:
        Delete_Packages() 
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Backing Up",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.program.TotalRevolution' in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "You Are Now Backed Up", '','')   
    else:
        dp.create("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        
        if 'Backup' in name:
            extras.Kill_XBMC()
            dialog.ok("Community Builds - Install Complete", 'To ensure the skin settings are set correctly XBMC will now', 'close. If XBMC doesn\'t close please force close (pull power', 'or force close in your OS - [COLOR=lime]DO NOT exit via XBMC menu[/COLOR])')
        else:
            dialog.ok("[COLOR=blue][B]T[/COLOR][COLOR=dodgerblue]R[/COLOR] [COLOR=white]Community Builds[/COLOR][/B]", "You Are Now Restored", '','')        
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info(url):
    BaseURL='http://totalxbmc.com/totalrevolution/Community_Builds/community_builds.php?id=%s' % (url)
    link = extras.Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch = re.compile('name="(.+?)"').findall(link)
    authormatch = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
#    updatedmatch = re.compile('updated="(.+?)"').findall(link)
    name  = namematch[0] if (len(namematch) > 0) else ''
    author  = authormatch[0] if (len(authormatch) > 0) else ''
    version  = versionmatch[0] if (len(versionmatch) > 0) else ''
#    updated  = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    dialog.ok(name,'Author: '+author,'Latest Version: '+version,'')
    return
#---------------------------------------------------------------------------------------------------
#Search in description
def Search_Builds(url):
    vq = extras.Get_Keyboard( heading="Search for content" )
    # if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0
    # we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Builds(url)
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
# Addon starts here
params=Get_Params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass
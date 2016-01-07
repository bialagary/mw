# -*- coding: utf-8 -*-
import urllib, urllib2
import sys, re, os
import xbmc, xbmcplugin, xbmcaddon, xbmcgui

__scriptname__ = 'SportseBooksEU'
__scriptID__ = 'plugin.video.sportsebooks.eu'
__author__ = 'sportsebooks.eu'
__url__ = 'http://api.sportsebooks.eu'
__credits__ = 'sportsebooks.eu'
__addon__ = xbmcaddon.Addon(__scriptID__)
__language__ = __addon__.getLocalizedString
t = __language__

BASE_RESOURCE_PATH = os.path.join( __addon__.getAddonInfo('path'), 'resources' )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, 'lib' ) )

import main

if main.login != '' and main.password != '':
    MENU = {
        1: [ t(56001).encode('utf-8'), '1.png', 1, False, False ],
        2: [ t(56100).encode('utf-8'), 'settings.png', 200, False, False ]
    }
else:
    MENU = {1: [ t(56100).encode('utf-8'), 'settings.png', 200, False, False ]}

 
# Show daily text 
def showWeekProgram():

    response = urllib2.urlopen(main.scheduleUrl)
    html = response.read()
    dialog = WeekProgram()
    dialog.customInit(html);
    dialog.doModal();
    del dialog

    xbmc.executebuiltin('Action("back")')

# Window showing daily text
class WeekProgram(xbmcgui.WindowDialog):

    def customInit(self, text):
        
        border = 30; # px relative to 1280/720 fixed grid resolution

        # width is always 1280, height is always 720.
        # getWidth() and getHeight() instead read the REAL screen resolution
        bg_image =  os.path.join( __addon__.getAddonInfo('path'), 'images/' ) + "background.png"
        self.ctrlBackgound = xbmcgui.ControlImage(
            0,0, 
            1280, 720, 
            bg_image
        )
        self.ctrlText= xbmcgui.ControlTextBox(
            border, border, 
            1280 - border *2, 720 - border, 
            'font15', "0xFFFFFFFF"
        )
        
        self.addControl (self.ctrlBackgound)
        self.addControl (self.ctrlText)

        self.ctrlText.setText( self.getProgram(text) );

    def onAction(self, action):
        #Every key will close the windo
        self.close()
        return

    # Grep today's textual date
    def getProgram(self, text):
        text =  re.sub("<b>", "[B]", text)
        text =  re.sub("</b>", "[/B]", text)
        clean = text
        spaced = clean
        return spaced
class Start:
    def __init__(self):
        self.showListOptions()
    
    def addDir(self, name, mode, icon, autoplay, isPlayable = True):
        u = '%s?mode=%d' % (sys.argv[0], mode)
        icon = os.path.join( __addon__.getAddonInfo('path'), 'images/' ) + icon
        if autoplay or icon == '':
            icon = 'DefaultVideo.png'
        liz = xbmcgui.ListItem(name, iconImage = icon, thumbnailImage = icon)
        if autoplay and isPlayable:
            liz.setProperty('IsPlayable', 'true')
        liz.setInfo( type = 'Video', infoLabels = { 'Title': name } )
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = not autoplay)
    
    def showListOptions(self):
        handler = main.Handler()
        parser = main.UrlParser()
        params = parser.getParams()
        mode = parser.getIntParam(params, 'mode')
        s = main.Settings()
        if mode == None or mode == '':
            s.setViewMode('general')
            for n, v in MENU.items():
                self.addDir(v[0], v[2], v[1], v[3], v[4])
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif mode == 1:
            handler.run(1)
            s.setViewMode('other')
        elif mode == 2:
            handler.run(2)
            s.setViewMode('other')
        elif mode == 3:
            handler.run(3)
            s.setViewMode('other')
        elif mode == 4:
            handler.run(4)
            s.setViewMode('other')
        elif mode == 5:
            handler.run(5)
            s.setViewMode('other')
        elif mode == 6:
            s.setViewMode('general')
            msg = main.Messages()
            msg.Warning(t(57023).encode('utf-8'), t(57024).encode('utf-8'))
        elif mode == 7:
            s.setViewMode('general')
            ip = main.InitPlayer()
            ip = ip.checkVersion()
            msg = main.Messages()
            if ip['status'] == 2:
                msg.Warning(t(57023).encode('utf-8'), t(57049).encode('utf-8'))
            elif ip['status'] == 3:
                msg.Warning(t(57023).encode('utf-8'), t(57050).encode('utf-8'), t(57048).encode('utf-8'))
            elif ip['status'] == 4:
                msg.Warning(t(57023).encode('utf-8'), t(57051).encode('utf-8'), t(57048).encode('utf-8'))
            elif ip['status'] == 5:
                msg.Warning(t(57023).encode('utf-8'), t(57052).encode('utf-8'), t(57048).encode('utf-8'))
            else:
                msg.Warning(t(57023).encode('utf-8'), t(57053).encode('utf-8'), t(57054).encode('utf-8'))
        elif mode == 200:
            s.setViewMode('general')
            s.showSettings()
        elif mode == 300:
            rr = showWeekProgram()


init = Start()

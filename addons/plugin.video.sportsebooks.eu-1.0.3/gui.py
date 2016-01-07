# -*- coding: utf-8 -*-
import sys, re, os
import xbmc, xbmcplugin, xbmcaddon, xbmcgui
import main

__scriptname__  = sys.modules[ '__main__' ].__scriptname__
__scriptID__   = sys.modules[ '__main__' ].__scriptID__
__addon__ = sys.modules[ '__main__' ].__addon__
t = sys.modules[ '__main__' ].__language__

os.path.join( __addon__.getAddonInfo('path'), 'resources' )

MESSAGE_ACTION_OK = 110
MESSAGE_EXIT = 111
MESSAGE_TITLE = 101
MESSAGE_LINE1 = 102
MESSAGE_LINE2 = 103
MESSAGE_LINE3 = 104

INFO_CANAL_NAME = 11
INFO_PHOTO_DIFFUSE = 12
INFO_PHOTO = 17
INFO_BROADCAST = 13
INFO_PLATFORM = 15
INFO_DESCRIPTION = 16
INFO_PLAY = 18
INFO_CANCEL = 19

class MessageDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, strXMLname, strFallbackPath, strDefaultName, forceFallback = True):
        pass
    
    def setTableText(self, tab):
        self.tabText = tab
    
    def getTableText(self):
        return self.tabText
    
    def onInit(self):
        self.loadTexts()
    
    def onAction(self, action):
        if action == 1010:
            self.close()
    
    def onClick(self, controlID):
        if controlID == MESSAGE_ACTION_OK or controlID == MESSAGE_EXIT:
            self.onAction(1010)
    
    def onFocus(self, controlID):
        pass

    def loadTexts(self):
        self.getControl(MESSAGE_TITLE).setLabel(str(self.getTableText()['title']))
        self.getControl(MESSAGE_LINE1).setLabel(str(self.getTableText()['text1']))
        self.getControl(MESSAGE_LINE2).setLabel(str(self.getTableText()['text2']))
        self.getControl(MESSAGE_LINE3).setLabel(str(self.getTableText()['text3']))

class InfoDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, strXMLname, strFallbackPath, strDefaultName, forceFallback = True):
        jsn = main.ShowList()
        set = main.Settings()
        self.channelsTab =  jsn.getJsonFromAPI(set.getJsonUrl)
    
    def setChannel(self, channel):
        self.channel = channel
    
    def getChannel(self):
        return self.channel
    
    def onInit(self):
        chanInfo = self.getChannelInfoFromJSON(self.getChannel())
        self.getControl(INFO_CANAL_NAME).setLabel(chanInfo['title'])
        self.getControl(INFO_BROADCAST).setLabel(chanInfo['user'])
        self.getControl(INFO_PHOTO).setImage(chanInfo['image'])
        self.getControl(INFO_PHOTO_DIFFUSE).setImage(chanInfo['image'])
        self.getControl(INFO_PLATFORM).setLabel(__scriptname__)
        self.getControl(INFO_DESCRIPTION).setText(chanInfo['desc'])
    
    def onAction(self, action):
        if action == 1010:
            self.close()
        elif action == 1011:
            p = main.Handler()
            p.setIsPlay('True')
            self.close()
    
    def onClick(self, controlID):
        if controlID == INFO_CANCEL:
            self.onAction(1010)
        elif controlID == INFO_PLAY:
            self.onAction(1011)
    
    def getChannelInfoFromJSON(self, channel):
        dataInfo = { 'title': '', 'image': '', 'user': '', 'tags': '', 'desc': '' }
        try:
            for v,k in self.channelsTab.items():
                if channel == int(k['cid']):
                    cid = k['cid']
                    title = k['channel_title']
                    user = k['name']
                    tags = k['channel_tags'] 
                    desc = k['channel_description']
                    image = k['channel_logo_url']
                    dataInfo = { 'title': title, 'image': image, 'user': user, 'tags': tags, 'desc': desc }
                    break
        except TypeError, typerr:
            print typerr
        return dataInfo

class Windows:
    def __init__(self):
        pass
    
    def Warning(self, title, text1, text2, text3):
        msg = MessageDialog('DialogWarning.xml', __addon__.getAddonInfo('path'), 'Default')
        tabText = { 'title': title, 'text1': text1, 'text2': text2, 'text3': text3 }
        msg.setTableText(tabText)
        msg.doModal()
        del msg
    
    def Error(self, title, text1, text2, text3):
        msg = MessageDialog('DialogError.xml', __addon__.getAddonInfo('path'), 'Default')
        tabText = { 'title': title, 'text1': text1, 'text2': text2, 'text3': text3 }
        msg.setTableText(tabText)
        msg.doModal()
        del msg
    
    def Info(self, channel):
        info = InfoDialog('DialogInfo.xml', __addon__.getAddonInfo('path'), 'Default')
        info.setChannel(channel)
        info.doModal()
        del info

    def Other(self, channel):
        info = MessageDialog('DialogSchedule.xml', __addon__.getAddonInfo('path'), 'Default')
        msg.setTableText('111')
        msg.doModal()
        del info

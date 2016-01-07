
import xbmc
import xbmcgui
import os
import re
import urllib2

def getPath():
    path = xbmc.translatePath('special://home/addons')
    path = os.path.join(path, 'Navi-X')
    return path


def installed():
    return os.path.exists(getPath())


def getVersion():
    path = getPath()
    file = os.path.join(path, 'addon.xml')    
    
    if not os.path.exists(file):  
        return 0

    file = open(file , 'r')
    text = file.read()
    file.close()

    try:
        v = re.compile('version="(.+?)"').findall(text)[1]
        return int(v.replace('.', ''))
    except:
        pass

    return 0


def restore():
    filename = os.path.join(getPath(), 'src', 'navix.py')
    bak      = os.path.join(getPath(), 'src', 'navix.py.hub_bak')

    if not os.path.exists(bak):
        return False

    try:
        os.remove(filename)  
    except:
        pass

    os.rename(bak, filename)

    return True



def addJDownloader(base):
    version = getVersion()
    
    file = None
    
    if version == 376:
        file = 'navix376.py'

    elif version == 377:
        file = 'navix377.py'

    if not file:
        dialog = xbmcgui.Dialog()
        dialog.ok('TEAM MIKEY', "Navi-X Version Unknown", "Nothing changed!")
        return

    url = base + 'tweaks/' + file

    filename = os.path.join(getPath(), 'src', 'navix.py')
    bak      = os.path.join(getPath(), 'src', 'navix.py.hub_bak')

    try:
        if not os.path.exists(bak):
            os.rename(filename, bak)
    except:
        pass

    try:
        os.remove(filename)  
    except:
        pass

    patch = urllib2.urlopen(url).read()

    f = open(filename, mode='w')
    f.write(patch)
    f.close()
    
    dialog = xbmcgui.Dialog()
    dialog.ok('TEAM MIKEY', 'All Done Thank You', 'Brought To You By TEAM MIKEY', 'Ensure JDownloader is installed and configured correctly')
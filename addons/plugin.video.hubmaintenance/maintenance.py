import xbmc
import os
import xbmcaddon
import glob
import re
import datetime
import xbmc
import xbmcgui
import urllib

from sqlite3 import dbapi2 as sqlite3

ADDON = xbmcaddon.Addon(id = 'plugin.video.hubmaintenance')



def downloadnewrepo(): 
    import time
    addonfolder = xbmc.translatePath(os.path.join('special://home/addons', ''))
    mikeyold=os.path.join(addonfolder, 'repository.mikey1234-repo')
    mikeynew=os.path.join(addonfolder, 'repository.mikey1234')
    if os.path.exists(mikeynew)==True: 
        for root, dirs, files in os.walk(mikeyold):
           for f in files:
                os.unlink(os.path.join(root, f))
           for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        try:
            os.rmdir(mikeyold)
        except:
            pass
            
            
def doMaintenance(version = 0):  
    downloadnewrepo()
    try:
        if ADDON.getSetting('thumbnails') == 'true':  
            RemoveOldTextures()        

    except Exception, e:
        #print str(e)
        pass

    #set script to run again in 1440 minutes (24 hours)
    addonPath = ADDON.getAddonInfo('path')
    name      = 'Maintenance'
    script    = os.path.join(addonPath, 'maintenance.py')
    args      = str(version)
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 1440)

    xbmc.executebuiltin(cmd)


def RemoveOldTextures():    
    path   = xbmc.translatePath('special://home/userdata/Database')
    files  = glob.glob(os.path.join(path, 'Textures*.db'))
    ver    = 0
    dbPath = ''

    for f in files:
        v = int(re.compile('extures(.+?).db').findall(f)[0])
        if ver < v:
            ver     = v
            dbPath  = f

    db   = xbmc.translatePath(dbPath)
    conn = sqlite3.connect(db, timeout = 10, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    cull     = datetime.datetime.today() - datetime.timedelta(days = 28)
    useCount = 10

    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (useCount, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])

    print "%d Stale Textures Removed" % len(images)

    #clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    #delete files
    root = xbmc.translatePath('special://home/userdata/Thumbnails')
    for image in images:
        path = os.path.join(root, image)
        try:
            os.remove(path)
        except:
            pass

                                    

if __name__ == '__main__':  
    doMaintenance(sys.argv[1])

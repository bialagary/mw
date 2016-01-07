VERSION = '1.0.12'

#Version 24/04/13 1.0.12 Moved Java back to box due to executable issues on USB
#Version 24/04/13 1.0.11 Added progress to unzipping
#Version 24/04/13 1.0.10 Use zipfile to extract Java, added cleanUp
#Version 23/04/13 1.0.9  Increased delay before extracting java
#Version 23/04/13 1.0.8  Bug fix in Java extract routine
#Version 23/04/13 1.0.7  Bug fix in Java extract folder
#Version 23/04/13 1.0.6  Bug fix in setting JAVAPATH
#Version 23/04/13 1.0.5  Change Java download folder to linux_download
#Version 23/04/13 1.0.4  Bug fix in setting JAVAPATH
#Version 23/04/13 1.0.3  Changed to use linux_download for Java download
#Version 23/04/13 1.0.2  Added removal of old addonpath image
#Version 23/04/13 1.0.1  Changed to use linux_download for all output image stuff
#Version 22/04/13 1.0.0  Initial version

import xbmc
import xbmcaddon
import xbmcgui 

import os
import shutil
import stat

import zipfile

import time

ADDON     = xbmcaddon.Addon(id='plugin.video.hubmaintenance')
BASE      = 'http://dl.dropbox.com/u/129714017/hubmaintenance/'
ADDONPATH = ADDON.getAddonInfo('path')
LINUXPATH = ADDON.getSetting('download_linux')
JAVAPATH  = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('profile'), 'java'))
JAVABIN   = os.path.join(JAVAPATH, 'java', 'bin')

TITLE = 'TEAM MIKEY'
LINE1 = '[COLOR yellow]Please Wait While I Sign Your Image[/COLOR]'


def cleanFolder(folder):
    try:
        for root, dirs, files in os.walk(folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(folder)
    except:
        pass


def cleanUp(original, ret, DEBUG):
    javaZIP    = os.path.join(LINUXPATH, 'java.zip')
    oldImgPath = os.path.join(ADDONPATH, 'temp.img')
    newImgPath = os.path.join(LINUXPATH, 'temp.img')

    try:
        os.remove(oldImgPath)
    except:
        pass      

    try:
        os.remove(newImgPath)
    except:
        pass      

    try:
        os.remove(javaZIP)
    except:
        pass 

    cleanFolder(os.path.join(ADDONPATH, 'META-INF'))
    cleanFolder(os.path.join(LINUXPATH, 'META-INF'))

    if not DEBUG:
        try:
            os.remove(original)
        except:
            pass
     
    return ret


def checkFile(file):
    print "**** checkFile: %s" % file
    try:
        if not os.access(file, os.F_OK):
            print "NOEXISTS"
            return False

        if(os.access(file, os.R_OK)):
            print "READ"

        if(os.access(file, os.W_OK)):
           print "WRITE"

        if (os.access(file, os.X_OK)):
            print "EXECUTE"
            return True

    except Exception, e:
        print str(e)

    return False


def makeExec(file):
    st = os.stat(file)
    print "**** makeExec"
    print "Mode before %d" % st.st_mode
    os.chmod(file, st.st_mode | stat.S_IEXEC)
    print "Mode after %d" % os.stat(file).st_mode
    return checkFile(file)


def checkJava(dp):
    print "**** checkJava: JAVAPATH"
    print JAVAPATH

    if checkFile(os.path.join(JAVABIN, 'java')):
        return True

    dialog = xbmcgui.Dialog()
    dialog.ok("XBMCHUB TEAM", "You Dont Have Java Installed We Need To Download", "You Will Only Need To Do This Once")

    url  = BASE + 'java.zip'
    path = LINUXPATH
    lib  = os.path.join(path, 'java.zip')

    import downloader
    try:
        dp.update(0, TITLE, LINE1, 'Downloading Java')
        if not os.path.exists(lib):
            downloader.download(url, lib, dp)
    except Exception, e:
        print "**** checkJava: exception during download"
        print str(e)
        return False

    print "**** checkJava: EXTRACTING JAVA - STARTED"

    import extract
    dp.update(0, TITLE, LINE1, 'Extracting Java')
    if not extract.all(lib, JAVAPATH, dp):
        print "**** remove: ERROR OPENING/EXTRACTING JAVA ZIP"
        cleanFolder(JAVAPATH)
        dialog.ok('TEAM MIKEY','There was a problem reading the Java file','','')
        return False

    print "**** checkJava: EXTRACTING JAVA - FINISHED"

    try:
        makeExec(os.path.join(JAVABIN, 'java'))
    except Exception, e:
        print "**** checkJava: exception setting permissions"
        print str(e)
        return False
        
    return True


def removeProps(script):
    #remove checks for xios
    sp = script.split('\n', 2)

    if 'xios' not in sp[0]:
        return None

    newScript  = ''

    if ('xiosm3' not in sp[0]) and ('xiosm1' not in sp[0]):
        newScript += sp[0] + '\n'

    if ('xiosm3' not in sp[1]) and ('xiosm1' not in sp[1]):
        newScript += sp[1] + '\n'

    newScript += sp[2]
    return newScript
        

def remove(filename, DEBUG = False):
    print '***************** STARTING REMOVE CALL v%s **********************' % VERSION
    
    d  = xbmcgui.Dialog()
    dp = xbmcgui.DialogProgress()
    dp.create(TITLE, LINE1)

    metainf    = os.path.join(LINUXPATH, 'META-INF')
    imgPath    = os.path.join(LINUXPATH, filename)
    scriptName = 'updater-script'
    scriptPath = 'META-INF/com/google/android/%s' % scriptName
    dest       = os.path.join(LINUXPATH, 'update.img')

    print '**** remove: PATHS'
    print LINUXPATH
    print metainf
    print imgPath
    print scriptPath
    print dest
    print JAVABIN

    cleanUp('', True, DEBUG)

    try:
        if not makeExec(os.path.join(ADDONPATH, 'signer', 'testkey.pk8')):
            d.ok('TEAM MIKEY','There was a problem setting permissions', 'on testkey.pk8','')
            return False
    except Exception, e:
        print "***********ERROR SETTING PERMISSIONS ON JAVA FILES*******"
        print str(e)
        return cleanUp(imgPath, False, DEBUG)

    
    dp.update(5, TITLE, LINE1,'Extracting Build Script')

    try:
        zin = zipfile.ZipFile(imgPath, 'r')
    except Exception, e:
        print "**** remove: ERROR OPENING ORIGINAL IMAGE"
        print str(e)
        d.ok('TEAM MIKEY','There was a problem reading the file','','')
        return cleanUp(imgPath, False, DEBUG)


    zinfo         = zin.getinfo(scriptPath)
    compress_type = zinfo.compress_type

    zin.extract(scriptPath, LINUXPATH)

    extractedPath = os.path.join(LINUXPATH, scriptPath)
    tempPath      = os.path.join(LINUXPATH, 'temp.img')

    f = open(extractedPath, mode='r')
    t = f.read()
    f.close()

    dp.update(10, TITLE, LINE1,'Removing Checks')

    newScript  = removeProps(t)
    if not newScript:
        print "**** remove: NO CHECKS NECESSARY"
        d.ok('TEAM MIKEY','There were no checks to remove','','')
        zin.close()
        try:
            os.remove(dest)
        except:
            pass
        os.rename(imgPath, dest)
        return cleanUp(imgPath, True, DEBUG)


    dp.update(15, TITLE, LINE1,'Rebuilding Image (this may take a couple of minutes)')
    
    zout = zipfile.ZipFile(tempPath, 'w')

    print "**** remove: CREATING NEW IMAGE - STARTED"

    try:

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename == scriptPath:
                #add modified script
                zout.writestr(zinfo, newScript)   
            else:
                zout.writestr(item, buffer)   
    except Exception, e:
        print "**** remove: CREATING NEW IMAGE - ERROR"
        print str(e)
        return cleanUp(imgPath, False, DEBUG)

    zout.close()
    zin.close()

    print "**** remove: CREATING NEW IMAGE - FINISHED"

    dp.update(40, TITLE, LINE1,'Image Rebuilt, Now Checking For Java')

    if not checkJava(dp):
        print "**** remove: NO JAVA"    
        return cleanUp(imgPath, False, DEBUG)

    print "**** remove: JAVA Confirmed"    

    dp.update(60, TITLE, LINE1,'Resigning Image (this may take over 5 minutes)')
    print "**** remove: 5 minute warning" 
    time.sleep(1)
    
    #sign new image
    cmd  = '"' + os.path.join(JAVABIN, 'java') + '"'
    cmd += ' '
    cmd += '-Xmx1024m '
    cmd += '-jar '
    cmd += '"' + os.path.join(ADDONPATH, 'signer', 'signapk.jar') + '" '
    cmd += '-w '
    cmd += '"' + os.path.join(ADDONPATH, 'signer', 'testkey.x509.pem') + '" '
    cmd += '"' + os.path.join(ADDONPATH, 'signer', 'testkey.pk8') + '" '
    cmd += '"' + tempPath + '" '
    cmd += '"' + dest + '"'

    print "**** remove: COMMAND LINE"
    print cmd

    print "**** remove: DESTINATION FILE"
    print dest

    try:
        #remove current update.img file
        os.remove(dest)
    except:
        pass
        
    os.system(cmd)
    good = os.path.exists(dest)

    if good: 
        print "**** remove: YIPPEE SIGNED FILE EXISTS"
        d.ok('TEAM MIKEY', 'Signed file created sucessfully', '', '')
    else:
        print "**** remove: CRAP SIGNED FILE DOES NOT EXISTS"
        d.ok('TEAM MIKEY','Failed to sign file', 'Check Logs', '')
   
    cleanUp(imgPath, True, DEBUG)

    dp.update(100, TITLE, LINE1,'')
    dp.close()

    return good

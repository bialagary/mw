# -*- coding: utf-8 -*-
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import plugintools
import xbmc

REMOTE_VERSION_FILE = "http://"+plugintools.get_setting("server")+"/ruyaserver/version-xbmc.txt"
LOCAL_VERSION_FILE = os.path.join( plugintools.get_runtime_path() , "version.txt")

def check_for_updates():
    plugintools.log("ruyaiptv.updater checkforupdates")

    # Descarga el fichero con la versión en la web
    try:
        plugintools.log("ruyaiptv.updater remote_version_file="+REMOTE_VERSION_FILE)
        data = plugintools.read( REMOTE_VERSION_FILE )

        versiondescargada = data.splitlines()[0]
        urldescarga = data.splitlines()[1]
        plugintools.log("ruyaiptv.updater version descargada="+versiondescargada)
        
        # Lee el fichero con la versión instalada
        plugintools.log("ruyaiptv.updater local_version_file="+LOCAL_VERSION_FILE)
        infile = open( LOCAL_VERSION_FILE )
        data = infile.read()
        infile.close();

        versionlocal = data.splitlines()[0]
        plugintools.log("ruyaiptv.updater version local="+versionlocal)

        if int(versiondescargada)>int(versionlocal):
            plugintools.log("ruyaiptv.updater update found")
            
            yes_pressed = plugintools.message_yes_no("RuYa IPTV","An update is available!","Do you want to install it now?")

            if yes_pressed:
                try:
                    plugintools.log("ruyaiptv.updater Download file...")
                    local_file_name = os.path.join( plugintools.get_data_path() , "update.zip" )
                    urllib.urlretrieve(urldescarga, local_file_name )
            
                    # Lo descomprime
                    plugintools.log("ruyaiptv.updater Unzip file...")

                    import ziptools
                    unzipper = ziptools.ziptools()
                    destpathname = xbmc.translatePath( "special://home/addons")
                    plugintools.log("ruyaiptv.updater destpathname=%s" % destpathname)
                    unzipper.extract( local_file_name , destpathname )
                    
                    # Borra el zip descargado
                    plugintools.log("ruyaiptv.updater borra fichero...")
                    os.remove(local_file_name)
                    plugintools.log("ruyaiptv.updater ...fichero borrado")

                    xbmc.executebuiltin((u'XBMC.Notification("Updated", "The add-on has been updated", 2000)'))
                    xbmc.executebuiltin( "Container.Refresh" )
                except:
                    xbmc.executebuiltin((u'XBMC.Notification("Not updated", "An error causes the update to fail", 2000)'))

    except:
        import traceback
        plugintools.log(traceback.format_exc())

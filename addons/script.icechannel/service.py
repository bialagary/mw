# load lib directory
# begin
import xbmc
import re
xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
if xbmc_version:
    xbmc_version = int(xbmc_version.group(1))
else:
    xbmc_version = 1
print xbmc_version
if xbmc_version >= 14:
    addon_id = 'script.icechannel'
    lib_addon_dir_name = "lib"
    import xbmcaddon
    import os
    from os.path import join, basename
    import sys
    addon = xbmcaddon.Addon(id=addon_id)
    addon_path = addon.getAddonInfo('path')
    sys.path.append(addon_path)
    lib_addon_dir_path = os.path.join( addon_path, lib_addon_dir_name)
    sys.path.append(lib_addon_dir_path)
    for dirpath, dirnames, files in os.walk(lib_addon_dir_path):
        sys.path.append(dirpath)
# end

from entertainment import common
import os

common._update_settings_xml()

services_path = os.path.join(common.addon_path, 'services')

sti=1

for dirpath, dirnames, files in os.walk(services_path):
    for f in files:
        if f.endswith('.py'):
            service_py = os.path.join(dirpath, f)
            #cmd = 'RunScript(%s,%s)' % (service_py, '1')
            #xbmc.executebuiltin(cmd)
            common.SetScriptOnAlarm(f[:-3], service_py, duration=sti)
            sti = sti + 1

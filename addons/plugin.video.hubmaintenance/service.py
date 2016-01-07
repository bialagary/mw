
import xbmcaddon
import os

try:  
    addonPath = xbmcaddon.Addon(id = 'plugin.video.hubmaintenance').getAddonInfo('path')
    name      = 'Maintenance'
    script    = os.path.join(addonPath, 'maintenance.py')
    version   = 1
    args      = str(version)
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name.encode('utf-8', 'replace'), script.encode('utf-8', 'replace'), args.encode('utf-8', 'replace'), 0)     

    xbmc.executebuiltin(cmd)

except Exception:
    pass


# -*- coding: cp1254 -*-

import sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

addon_id = 'script.module.xbmctr'
__settings__ = xbmcaddon.Addon(id=addon_id)
##home = __settings__.getAddonInfo('path')
##folders = xbmc.translatePath(os.path.join(Addon.getAddonInfo('path'), 'resources', 'lib'))
##sys.path.append(folders)


def run():
    import araclar
    return True

if __name__ == "__main__":
    if settings.getSetting("autostart") == "true":
        run()

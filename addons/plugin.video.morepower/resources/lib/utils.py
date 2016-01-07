import os
import re
import sys
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcgui

from addon.common.net import Net
from addon.common.addon import Addon

net = Net()

addon_id = 'plugin.video.morepower'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()


try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)
               


def MESSAGE(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('description=(.*?)/description', html, re.I|re.DOTALL)
    for text in r:
        final = text
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)

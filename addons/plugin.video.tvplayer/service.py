import urllib2,xbmc,xbmcaddon,re

PLUGIN='plugin.video.tvplayer'
ADDON = xbmcaddon.Addon(id=PLUGIN)


try :
 DATA_URL='http://xty.me/xunitytalk/addons/plugin.video.tvplayer/config.txt'
 request = urllib2.Request(DATA_URL)
 link = urllib2.urlopen(request).read()
 token=re.compile('token="(.+?)"').findall(link)[0]
 expiry=re.compile('expiry="(.+?)"').findall(link)[0]
 referer=re.compile('referer="(.+?)"').findall(link)[0]
 ADDON.setSetting('token',token)
 ADDON.setSetting('expiry',expiry)
 ADDON.setSetting('referer',referer)
except : pass



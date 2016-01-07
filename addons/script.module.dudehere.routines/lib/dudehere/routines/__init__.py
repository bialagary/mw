import sys
import os
import xbmc
import xbmcaddon
import os
import unicodedata

from addon.common.addon import Addon

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	forward = dict((key, value) for key, value in enums.iteritems())
	reverse = dict((value, key) for key, value in enums.iteritems())
	enums['f_map'] = forward
	enums['r_map'] = reverse
	return type('Enum', (), enums)

def has_item(obj, key):
	if key in obj: return True
	for k, v in obj.items():
		if isinstance(v,dict):
			item = has_item(v, key)
			if item is not None:
				return True
	return False

class MyAddon(Addon):
	def log(self, msg, level=0):
		if level==1 or self.get_setting('log_level')=="1":
			if isinstance (msg,str):
				msg = msg.decode("utf-8")
			msg = u'%s' %  msg
			msg = msg.encode('utf-8')
			xbmc.log('%s v%s: %s' % (self.get_name(), self.get_version(), msg))
	def str2bool(self, v):
		if not v: return False
		return v.lower() in ("yes", "true", "t", "1")
	def get_bool_setting(self, k):
		return(self.str2bool(self.get_setting(k)))
	def raise_notify(self, title, message, timeout=3000):
		image = os.path.join(xbmc.translatePath( self.get_path() ), 'icon.png')
		cmd = "XBMC.Notification(%s, %s, %s, %s)" % (title, message, timeout, image)
		xbmc.executebuiltin(cmd)

ARGV = sys.argv
try:
	int(ARGV[1])
except:
	ARGV.insert(1, -1)
try: 
	str(ARGV[2])
except:
	ARGV.insert(2, "?/fake")
PLATFORM = sys.platform
HANDLE_ID = int(ARGV[1])
ADDON_URL = ARGV[0]
PLUGIN_URL = ARGV[0] + ARGV[2]	
ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
ADDON_NAME =  xbmcaddon.Addon().getAddonInfo('name')
ADDON = MyAddon(ADDON_ID,ARGV)
ADDON_NAME = ADDON.get_name()
VERSION = ADDON.get_version()
ROOT_PATH = ADDON.get_path()
DATA_PATH = ADDON.get_profile()
ARTWORK = ROOT_PATH + '/resources/artwork/'
QUALITY = enum(LOCAL=9, HD1080=8, HD720=7, HD=6, HIGH=5, SD480=4, UNKNOWN=3, LOW=2, POOR=1)
LOG_LEVEL = enum(STANDARD=0, VERBOSE=1)

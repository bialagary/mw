import urllib2,xbmc,xbmcaddon,os

PLUGIN='plugin.video.streamtvbox'
ADDON = xbmcaddon.Addon(id=PLUGIN)
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
paki=os.path.join(datapath, "paki")
pak=os.path.join(datapath, "pak")
if os.path.exists(datapath) == False:
        os.makedirs(datapath)



try :
 import base64
 import time
 TIME = time.time()
 second= str(TIME).split('.')[0]
 first =int(second)+69296929
 token=base64.b64encode('%s@2nd2@%s' % (str(first),second))
 DATA_URL='https://app.dynns.com/app_panelnew/output.php/playlist?type=xml&deviceSn=pakindia4&token=%s'  %token
 request = urllib2.Request(DATA_URL)
 base64string = 'YWRtaW46QWxsYWgxQA=='
 request.add_header("Authorization", "Basic %s" % base64string)   
 i1iIIII = urllib2.urlopen(request).read()
 I1 = open ( paki , mode = 'w' )
 I1 . write ( i1iIIII )
except : pass


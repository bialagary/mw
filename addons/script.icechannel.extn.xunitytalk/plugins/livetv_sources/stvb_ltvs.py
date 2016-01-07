'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import CustomSettings

class stvb(LiveTVSource,CustomSettings):
    implements = [LiveTVSource,CustomSettings]
    
    display_name = "STREAMTVBOX"
    
    name = 'STREAMTVBOX'
    
    
    source_enabled_by_default = 'false'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="STVB Account">\n'
        xml += '<setting id="tv_user" type="text" label="Username" default="" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
        
        
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
            import xbmc,os,re
            #OSS = xbmcaddon.Addon(id='plugin.video.offside')
            
            datapath = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.streamtvbox')
            
            
            channeljs=os.path.join(datapath,'cookies', "channel.js")
            
            if os.path.exists(channeljs)==False:
                return
            clean_id= id.replace('_','').lower()
            
            channel_js=open(channeljs).read()
            
            link = channel_js.split('"title"')
            
            for p in link:
                
                if clean_id in p.lower().replace(' ',''):
                    
                    match = re.findall(': "(.+?)".+?"file": "(.+?)",.+?": "rtmp"',p,re.M|re.DOTALL)
                    
                
                    for name,url in match:
                        if 'HD' in name:
                            res='HD'
                        else:
                            res='SD'
                        self.AddLiveLink( list, name, url, host='STREAMTVBOX',quality=res)
   
        

    def Resolve(self, url):
        import re
        
        from entertainment.net import Net
        net = Net()
        loginurl = 'http://streamtvbox.com/site/wp-login.php'
        username = self.Settings().get_setting('tv_user')
        password = self.Settings().get_setting('tv_pwd')
        site='http://streamtvbox.com/site/live-tv/'
        data     = {'pwd': password,
                                                'log': username,
                                                'wp-submit': 'Log In','redirect_to':'http://streamtvbox.com/site','testcookie':'1'}
        headers  = {'Host':'streamtvbox.com',
                                                'Origin':'http://streamtvbox.com',
                                                'Referer':'http://streamtvbox.com/site/wp-login.php',
                                                        'X-Requested-With':'XMLHttpRequest'}
        html = net.http_POST(loginurl, data, headers).content

        
        auth  = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)[0]
        stream_url = '%s swfUrl=http://p.jwpcdn.com/6/8/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s swfVfy=true live=true timeout=15' % (url.replace('" + urlkey1 + "', auth), auth, site)
        return stream_url
        
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)
        

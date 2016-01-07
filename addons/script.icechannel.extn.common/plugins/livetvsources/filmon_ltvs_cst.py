'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class filmon(LiveTVSource,CustomSettings):
    implements = [LiveTVSource,CustomSettings]
    
    display_name = "FILMON.COM"
    
    name = 'FILMON.COM'
    
    source_enabled_by_default = 'true'
    
    base_url = 'http://filmon.com/tv/live'
    
    api_url = 'http://www.filmon.com/api/'
    
    import os
    cookie_file = os.path.join(common.cookies_path, 'filmon.lwp')
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="user" type="text" label="Email" default="" />\n'
        xml += '<setting id="pwd" type="text" option="hidden" label="Password" default="" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):

        search_term = id
        
        from entertainment.net import Net
        net = Net(cached=False)
                
        user = self.Settings().get_setting('user')
        pwd = self.Settings().get_setting('pwd')
        if user and pwd:
            
            content = net.http_POST('http://www.filmon.com/user/login', {'login':user, 'password':pwd, 'remember':'1'}, 
                headers={'Referer':self.base_url}).content
                
            net.save_cookies(self.cookie_file)

        
        content = net.http_GET(self.base_url).content.encode("utf-8")
        link = content.split('{"id":')
        import re
        for p in link:            
            if '"filmon_' in p: 
                title=p.split('"title":"')[1]
                ITEM_TITLE=title.split('"')[0]
                p_id = common.CreateIdFromString( common.CleanTextForSearch(ITEM_TITLE, strip=True) )
                if id == p_id or p_id in other_names :
                    channel_id=p.split(',')[0]
                    res=['SD','HD']
                    for quality in res:
                        channel_id_with_quality=channel_id + '__' + quality
                        self.AddLiveLink( list, ITEM_TITLE, channel_id_with_quality, language = language.title(),host='FILMON',quality=quality)
                    break

    def GET_SESSION_ID(self):
    
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        content = net.http_GET(self.api_url + 'init/').content.encode("utf-8")
        match= re.compile('"session_key":"(.+?)"').findall (content)
        sess=match[0]

        return sess            
    
    def Resolve(self, url):
        resolved_media_url = ''

        quality=url.split('__')[1]
        url=url.split('__')[0]

        
        from entertainment.net import Net
        net = Net(cached=False)
        
        sess = self.GET_SESSION_ID()
        
        net.set_cookies(self.cookie_file)
        
        r='http://www.filmon.com/api/channel/%s?session_key=%s' % (url,sess)
        print r
        content = net.http_GET(r).content
        import json
        data = json.loads(content)
        
        channels= data['streams']
        for stream in channels:
            if stream['quality'] == 'low':        
                import re
                foregex= stream['url']+'<'
                playpath=stream['name']
                name=stream['quality']
                if re.search('mp4',playpath ,re.IGNORECASE):
                    regex = re.compile('rtmp://(.+?)/(.+?)/(.+?)/<')
                    match1 = regex.search(foregex)
                    app = '%s/%s/' %(match1.group(2), match1.group(3))
                    swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                    url=stream['url']+playpath
                if re.search('m4v',playpath ,re.IGNORECASE):
                    app = 'vodlast'
                    swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                    url= stream['url']+'/'+playpath
                else:
                    try:
                            regex = re.compile('rtmp://(.+?)/live/(.+?)id=(.+?)<')
                            match = regex.search(foregex)
                            app = 'live/%sid=%s' %(match.group(2),match.group(3))
                            url= stream['url']
                            swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                    except:
                            pass
                    try:
                            regex = re.compile('rtmp://(.+?)/(.+?)id=(.+?)"')
                            match1 = regex.search(foregex)
                            app = '%sid=%s' %(match1.group(2), match1.group(3))
                            swfUrl='http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
                    except:
                            pass
                    try:
                            regex = re.compile('rtmp://(.+?)/(.+?)/<')
                            match = regex.search(foregex)
                            app = '%s/' %(match.group(2))
                            url= stream['url']+'/'+playpath
                            swfUrl= 'http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf'
                    except:
                            pass
                tcUrl=stream['url']
                pageUrl = 'http://www.filmon.com/'
                resolved_media_url= str(url)+' playpath='+str(playpath)+' app='+str(app)+' swfUrl='+str(swfUrl)+' tcUrl='+str(tcUrl)+' pageurl='+str(pageUrl)+' live=true'
                if quality=='HD':
                    return resolved_media_url.replace('low','high')
                else:
                    return resolved_media_url

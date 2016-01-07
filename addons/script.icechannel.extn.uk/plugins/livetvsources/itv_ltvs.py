'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class itv(LiveTVSource):
    implements = [LiveTVSource]
    
    display_name = "ITV PLAYER"
    
    name = 'ITV PLAYER'
    
    source_enabled_by_default = 'true'


    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):

        quality_dict = {'1200':'HD', '800':'SD', '600':'LOW'}
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        
        if not 'itv' in id: return
        
        if '2' in id or '3' in id:

            id=id.split('itv')[1]           
            name='ITV '+id
            
            SoapMessage=self.TEMPLATE('sim'+id,'itv'+id)
            
            headers={'Content-Length':'%d'%len(SoapMessage),'Content-Type':'text/xml; charset=utf-8','Host':'mercury.itv.com','Origin':'http://www.itv.com','Referer':'http://www.itv.com/Mercury/Mercury_VideoPlayer.swf?v=null','SOAPAction':"http://tempuri.org/PlaylistService/GetPlaylist",'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}

            response = net.http_POST("http://mercury.itv.com/PlaylistService.svc",SoapMessage, headers=headers).content
            
            response = response.split('VideoEntries')[1]
        
        
            

        if id =='itv1':
            name='ITV 1'
            url='http://www.itv.com/mediaplayer/xml/channels.itv1.xml'
            response = net.http_GET(url).content
    
            
        if id =='itv4':
            name='ITV 4'
            url='http://www.itv.com/mediaplayer/xml/channels.itv4.xml'



            response = net.http_GET(url).content

        

        rtmp=re.compile('<MediaFiles base="(.+?)"').findall(response)[0]
        match=re.compile('CDATA\[(.+?)\]').findall(response)
        for playpath in match:
            print playpath
            res=playpath.split('_')[1]
            res=res.split('@')[0]
            
            resolved_media_url=rtmp+' playpath='+playpath+' swfUrl=http://www.itv.com/mediaplayer/ITVMediaPlayer.swf?v=12.18.4 live=true timeout=10 swfvfy=true'
        
            
            self.AddLiveLink( list, name, resolved_media_url, language='English',host='ITV PLAYER',quality=quality_dict.get(res, 'NA') )

    def TEMPLATE(self,sim,channel):
            SM_TEMPLATE='''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                      <SOAP-ENV:Body>
                        <tem:GetPlaylist xmlns:tem="http://tempuri.org/" xmlns:itv="http://schemas.datacontract.org/2004/07/Itv.BB.Mercury.Common.Types" xmlns:com="http://schemas.itv.com/2009/05/Common">
                          <tem:request>
                            <itv:RequestGuid>BF0B9A3C-4F65-C45D-4BC4-3F639208946F</itv:RequestGuid>
                            <itv:Vodcrid>
                              <com:Id>%s</com:Id>
                              <com:Partition>itv.com</com:Partition>
                            </itv:Vodcrid>
                          </tem:request>
                          <tem:userInfo>
                            <itv:Broadcaster>Itv</itv:Broadcaster>
                            <itv:GeoLocationToken>
                              <itv:Token/>
                            </itv:GeoLocationToken>
                            <itv:RevenueScienceValue/>
                          </tem:userInfo>
                          <tem:siteInfo>
                            <itv:AdvertisingRestriction>None</itv:AdvertisingRestriction>
                            <itv:AdvertisingSite>ITV</itv:AdvertisingSite>
                            <itv:Area>channels.%s</itv:Area>
                            <itv:Platform>DotCom</itv:Platform>
                            <itv:Site>ItvCom</itv:Site>
                          </tem:siteInfo>
                          <tem:deviceInfo>
                            <itv:ScreenSize>Big</itv:ScreenSize>
                          </tem:deviceInfo>
                        </tem:GetPlaylist>
                      </SOAP-ENV:Body>
                    </SOAP-ENV:Envelope>
                    '''
            return SM_TEMPLATE%(sim,channel)
            
     
    def Resolve(self, url):
        

        return url

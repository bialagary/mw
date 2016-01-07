'''
    http://afdah.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common




class sezonlukdizi(TVShowSource):
    implements = [TVShowSource]
    
    name = "sezonlukdizi"
    display_name = "Sezonlukdizi"
    search_url = 'http://sezonlukdizi.com/service/search?q=%s&_=%s'
    videourl='http://sezonlukdizi.com/service/get_video_part'
    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue,season,episode,showname):

        import re
        from entertainment.net import Net
        
        net = Net(cached=False,user_agent='Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')
                  
        new_url = url

        r='%s-sezon-%s' % (season,episode)
  
        content= net.http_GET(new_url,headers={'X-Requested-With': 'XMLHttpRequest'}).content
        match=re.compile('img alt="(.+?)".+?class="seep" href="(.+?)"',re.DOTALL).findall(content)
        for title , url in match:
       

            if showname.lower() in title.lower():
                
                if r in url:
                    page = net.http_GET(url,headers={'X-Requested-With': 'XMLHttpRequest'}).content
                    video_id = re.compile('var video_id.+?"(.+?)"').findall(page)[0]
                    part_name = re.compile('var part_name.+?"(.+?)"').findall(page)[0]
                    videourl='http://sezonlukdizi.com/service/get_video_part'

                    data = {'video_id': video_id, 'part_name': part_name,'page':'0'}
                    html=  net.http_POST(videourl,data,headers={'X-Requested-With': 'XMLHttpRequest'}).content
                    print html
                    import json

                    link= json.loads(html)
          
                    scriptpage=re.compile('src="(.+?)"').findall(str(link))[0]
                    contents= net.http_GET(scriptpage,headers={'X-Requested-With': 'XMLHttpRequest'}).content
                    contented=contents.split('{')
                    for p in contented:
                        try:
                            source =re.compile('file.+?"(.+?)"').findall(p)[0]
                            res =re.compile('label.+?"(.+?)"').findall(p)[0]
                            if res.endswith('p'):
                                self.AddFileHost(list, res.upper(), source+'|'+scriptpage,host='GOOGLEVIDEO.COM')
                        except:pass       
                        
            
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re,time,json

        net = Net(cached=False,user_agent='Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')
        name = self.CleanTextForSearch(name)

        search_term = name.lower()
        helper_term = ''
        ttl_extrctr = ''
        new_url=self.search_url % (search_term.replace(' ','+'),(str(int(time.time() * 1000))))
        content= net.http_GET(new_url,headers={'X-Requested-With': 'XMLHttpRequest'}).content
        link = json.loads(content)
        for field in link:
            TITLE = field['name']
            URL = field['url']
            if name.lower() in TITLE.lower():

                    self.GetFileHosts(URL, list, lock, message_queue,season,episode,TITLE.lower())



    def Resolve(self, url):

      
        import requests
        import re,urllib
        s = requests.Session()

        ref=url.split('|')[1]
        url=url.split('|')[0]
        
            
        r = s.get(url, headers={'Referer':str(ref), 'User-Agent':'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko','x-requested-with':'XMLHttpRequest'},
                         allow_redirects=False)

        print r.headers
        return r.headers['location']+'|User-Agent=Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'+'&Referer=%s' % (urllib.quote(ref))    


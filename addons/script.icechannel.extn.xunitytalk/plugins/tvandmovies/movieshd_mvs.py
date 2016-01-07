'''
    Ice Channel
    MoviesHD
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class MoviesHD(MovieSource):

    implements = [MovieSource]
    
    name = "MoviesHDeu"
    display_name = "Movies HD"
    

    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue):
        
      from entertainment.net import Net
      import re  
      net = Net()

      content=net.http_GET(url).content
      
      if 'openload' in content: 
          olurl=re.compile('<iframe src="(.+?)"').findall(content)[0] 

        
          self.AddFileHost(list, '720P', olurl)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        
        net = Net()        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_term = name.replace(' ','+')
        
        import re
        url='http://movieshd.eu/?s='+search_term
        link=net.http_GET(url).content
        match = re.compile('title="(.+?)"/>\n<a href="(.+?)"').findall(link)

        for title , movie_url  in match:
            if name in title:
                if year in title: 
                    self.GetFileHosts(movie_url, list, lock, message_queue)
                

        
    def Resolve(self, url):
        
        from entertainment.net import Net

        import re ,json,urllib,time,os
        profile_path = common.profile_path
        puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % self.name       
        net = Net(user_agent='Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')
       
       

      
        id = re.compile('//.+?/(?:embed|f)/([0-9a-zA-Z-_]+)').findall(url)[0]

        url = 'https://api.openload.io/1/file/dlticket?file=%s' % id

        result = net.http_GET(url).content
        result = json.loads(result)
        print result
        if 'bandwidth usage too high' in str(result):
            return ''
        else:
            cap = result['result']['captcha_url']
            
            import xbmcgui
            img = xbmcgui.ControlImage(550,15,300,57,cap)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            import xbmc
            kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
            kb.doModal()
            capcode = kb.getText()
            if (kb.isConfirmed()):
                userInput = kb.getText()        

            time.sleep(result['result']['wait_time'])

            url = 'https://api.openload.io/1/file/dl?file=%s&ticket=%s' % (id, result['result']['ticket'])

            if not cap == None:
                url += '&captcha_response=%s' % urllib.quote(userInput)

            result = net.http_GET(url).content
            result = json.loads(result)

            url = result['result']['url'] + '?mime=true'
            return url
     
